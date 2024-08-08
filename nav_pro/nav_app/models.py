from django.db import models
from .utils import calculate_distance_with_waypoints

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)
    X = models.FloatField()
    y = models.FloatField()
    image = models.ImageField(upload_to='location_images/', blank=True, null=True)  # Add image field if needed
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    open_status = models.CharField(max_length=100, blank=True, null=True)
    reviews = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Path(models.Model):
    start_location = models.ForeignKey(Location, related_name='start_paths', on_delete=models.CASCADE)
    end_location = models.ForeignKey(Location, related_name='end_paths', on_delete=models.CASCADE)
    distance = models.FloatField()
    waypoints = models.JSONField(default=list)  # List of waypoints as [(x1, y1), (x2, y2), ...]

    def __str__(self):
        return f"{self.start_location} to {self.end_location}"
    
    @classmethod
    def create_path_with_waypoints(cls, start_location, end_location, waypoints):
        distance = calculate_distance_with_waypoints(waypoints)
        return cls.objects.create(start_location=start_location, end_location=end_location, distance=distance, waypoints=waypoints)
    

class Room(models.Model):   
    number = models.JSONField()  # JSONField to store room numbers
    floor = models.IntegerField()
    building = models.ForeignKey(Location, related_name='rooms', on_delete=models.CASCADE)

    def __str__(self):
        return f"Rooms {self.number} on Floor {self.floor} in {self.building}"