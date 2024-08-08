from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name='man'
urlpatterns = [
     path('path/', views.calculate_and_save_path_distance),
     path('path/<int:path_id>/', views.display_path, name='display_path'),
    #=====================================================================
     path('fetch_live_location/', views.fetch_live_location, name='fetch_live_location'),
    #=====================================================================
     path('select/',views.select_path,name='route'),
     path('',views.home,name='home'),
     path('college-map/', views.map_view, name='cmap'),  # College Map
     path('seaclsroom/', views.search_room, name='searom'),
     path('search/', views.find_room, name='find_room'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


