from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    
    #Adding custom Bootstrap classess to the form
    def __init__(self, *args, **kwargs):
        #Calling parent's constructor to initialize the form
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class']='form-control'
        self.fields['email'].widget.attrs['placeholder']='Email'
        self.fields['username'].widget.attrs['placeholder']='Username'
        self.fields['password1'].widget.attrs['placeholder']='Password'
        self.fields['password2'].widget.attrs['placeholder']='Confirm Password'

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
    error_messages = {
        'invalid_login': (
            "Either username or password is not correct. Please try again."
        )
    }

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Name'}))
    email = forms.CharField(validators=[EmailValidator()],widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Message','rows' :'6'}))
    
    
    