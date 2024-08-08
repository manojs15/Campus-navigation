# views.py

from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Location, Path, Room
from .utils import calculate_distance_with_waypoints
import json
from .forms import RoomSearchForm, PathForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from decimal import Decimal
#===================================================================
def calculate_and_save_path_distance(request):
    # Fetch or create Location instances (start and end locations)
    gate = Location.objects.get(name="girls hostel")
    canteen = Location.objects.get(name="ISE/CIVIL building")
    # Define waypoints (list of tuples)
    waypoints = [
        (12.3658236,76.6858773),
        (12.3656482,76.6858962),
        (12.3656704,76.6861621),
        (12.3657073,76.6866081),
        (12.3657387,76.6872684),
        (12.3657733,76.6876326),
        (12.3658486,76.68799),
        (12.3659304,76.6882147),
        (12.3659089,76.6884429),
        (12.366,76.6886113),
        (12.36608689,76.68872601),
        (12.36631135, 76.68872774),
        (12.36646166,76.68871191),
        (12.366447,76.688845),
        (12.366758, 76.688871),
        (12.36673,76.689134),
        (12.366719, 76.689361),
        (12.366425,76.68938)



    ]
    # Calculate distance based on waypoints
    distance = calculate_distance_with_waypoints(waypoints)
    # Create and save a Path instance
    path_instance = Path.objects.create(
        start_location=gate,
        end_location=canteen,
        distance=distance,
        waypoints=waypoints
    )
    # Optionally, you can return a response or render a template
    return render(request, 'calc.html', {'distance': distance})



#===================================================================================
def display_path(request, path_id):
    try:
        path_instance = Path.objects.get(id=path_id)
        waypoints = path_instance.waypoints
        waypoints_json = json.dumps(waypoints)
        return render(request, 'path_display.html', {'waypoints_json': waypoints_json})
    except Path.DoesNotExist:
        return HttpResponse("Path not found.")
#--------------------------------------------------------------------------

def select_path(request):
    if request.method == 'POST':
        form = PathForm(request.POST)
        if form.is_valid():
            start_location = form.cleaned_data['start_location']
            end_location = form.cleaned_data['end_location']           
            # Query for routes in both directions
            possible_routes = Path.objects.filter(
                Q(start_location=start_location, end_location=end_location) |
                Q(start_location=end_location, end_location=start_location)
            )
            if not possible_routes.exists():
                return render(request, 'no_path_found.html')
            # Find the shortest route based on distance
            shortest_route = possible_routes.order_by('distance').first()
            # Prepare waypoints data for JSON (assuming waypoints are stored as JSONField in Path model)
            waypoints = shortest_route.waypoints  # Assuming waypoints is a list of coordinates
             # If the route is in reverse, reverse the waypoints for correct display
            if shortest_route.start_location != start_location:
                waypoints = waypoints[::-1]       
            # Pass context to the template for displaying the path
            context = {
                'start_location': start_location,
                'end_location': end_location,
                'waypoints': waypoints,
            }
            return render(request, 'path_display2.html', context)
    else:
        form = PathForm()   
    return render(request, 'select_path.html', {'form': form})

#-----------------------------------------------------------------------
@csrf_exempt
def fetch_live_location(request):
    if request.method == 'POST':
        # Ensure that the data is sent in a format that Django can handle (JSON in this case)
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            # Perform any additional processing or validation here if needed
            return JsonResponse({'latitude': latitude, 'longitude': longitude})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
#============================================================================
def home(request):
        return render(request, 'home.html')
   
def map_view(request):
    locations = Location.objects.all()
    location_data = []
    for location in locations:
        location_data.append({
            'name': location.name,
            'coords': [location.X, location.y],
            'image': f"{location.image.url}" if location.image else None,  # Use image URL
            'rating': location.rating,
            'open_status': location.open_status,
            'reviews': location.reviews,
        })
    context = {
        'locations': json.dumps(location_data, cls=DecimalEncoder),
    }
    return render(request, 'map.html', context)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def search_room(request):
    if request.method == 'POST':
        form = RoomSearchForm(request.POST)
        if form.is_valid():
            room_number = form.cleaned_data['room_number']
            start_location = form.cleaned_data['start_location']
            # Find the room by number within the JSONField
            room = Room.objects.filter(Q(number__icontains=room_number)).first()
            if not room:
                return render(request, 'room_search_result.html', {
                    'error': f"No room found with number {room_number}"
                })
            building = room.building
            # Find the path from start_location to the room's building
            path = Path.objects.filter(start_location=start_location, end_location=building).first()
            return render(request, 'room_search_result.html', {
                'room': room,
                'path': path
            })
    else:
        form = RoomSearchForm()

    return render(request, 'search_room.html', {'form': form})


def find_room(request):
    if request.method == 'POST':
        search_query = request.POST.get('room_number', '').strip()
        # Fetch room details and location names from the database
        rooms = Room.objects.filter(
            number__icontains=search_query
        ).values(
            'number', 'floor', 'building__name', 'building__X', 'building__y'
        )
        # Fetch location details if search query matches location names
        locations = Location.objects.filter(
            name__icontains=search_query
        ).values(
            'name', 'X', 'y', 'image', 'rating', 'open_status', 'reviews'
        )
        # Convert querysets to lists of dictionaries
        rooms_list = list(rooms)
        locations_list = list(locations)
        # Render the result in the room_result.html template
        return render(request, 'room_result.html', {
            'loca': json.dumps(locations_list),
            'roo': json.dumps(rooms_list)
        })
    else:
        return render(request, 'home.html')
