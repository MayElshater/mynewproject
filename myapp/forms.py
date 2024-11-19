from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Chatbot, Document

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ChatbotForm(forms.ModelForm):
    class Meta:
        model = Chatbot
        fields = ['name', 'description']

class ChatbotPersonalityForm(forms.ModelForm):
    personality = forms.CharField(widget=forms.Textarea, help_text="Define your chatbot's personality.")
    
    class Meta:
        model = Chatbot
        fields = ['personality']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Validate file size
            max_size = 5 * 1024 * 1024  # 5MB
            if file.size > max_size:
                raise forms.ValidationError("File size exceeds 5MB.")
            
            # Optionally, check file type (e.g., only allow PDFs, etc.)
            if not file.name.endswith('.pdf'):  # Example of allowed file extension
                raise forms.ValidationError("Only PDF files are allowed.")
        return file


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
