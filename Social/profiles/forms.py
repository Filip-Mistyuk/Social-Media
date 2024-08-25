from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Follow

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        
class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['from_user', 'to_user', 'status']
        
class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search Users', max_length=100)