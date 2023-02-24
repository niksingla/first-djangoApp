from django import forms
from .models import UserProfile
from django_countries.widgets import CountrySelectWidget
from django.db import models  
from django.forms import fields  



"""class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','location']
        labels= {

            'bio':'',
            'location':'',
        }    

        widgets = {
            
            'bio':forms.Textarea(attrs={ 'class':'form-control mb-3','placeholder':"Description(Optional)", 'id':"floatingTextarea2", 'style':"height: 100px" }),
            'location': CountrySelectWidget(attrs= {'class':"form-select"})
        
        }    """

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']
        labels={
            'profile_pic':''
        }
        widgets = {
            'profile_pic':forms.FileInput(attrs={'class':'form-control', 'onchange':'changePic(event);', 'type':'file', 'name':'pic', 'id':'formFile'})
        }


#<input class="form-control" type="file" name="pic" id="formFile">