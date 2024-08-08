from django import forms
from .models import Location

class PathForm(forms.Form):
    start_location = forms.ModelChoiceField(queryset=Location.objects.all(), label="Start Location")
    end_location = forms.ModelChoiceField(queryset=Location.objects.all(), label="End Location")


class RoomSearchForm(forms.Form):
    room_number = forms.CharField(max_length=10, label="Room Number")
    start_location = forms.ModelChoiceField(queryset=Location.objects.all(), label="Start Location")