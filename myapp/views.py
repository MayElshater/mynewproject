from django.shortcuts import render, redirect
from .models import Chatbot, Document, DocumentChunk
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .chroma_utils import preprocess_document
import os
from django.contrib.auth.models import User
from .forms import ChatbotForm, DocumentUploadForm, ChatbotPersonalityForm, RegistrationForm,LoginForm
from django.contrib import messages
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  # Redirect to the login page
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


# Define Step 1
def create_chatbot_step1(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        chatbot = Chatbot.objects.create(user=request.user, name=name, description=description)
        return redirect('create_chatbot_step2', chatbot_id=chatbot.id)  # Redirect to step 2
    return render(request, 'create_chatbot_step1.html')

# Define Step 2
def create_chatbot_step2(request, chatbot_id):
    chatbot = Chatbot.objects.get(id=chatbot_id)

    if request.method == 'POST':
        tone = request.POST.get('tone')
        behavior = request.POST.get('behavior')

        # Update the chatbot's personality with the behavior
        chatbot.personality = f"Tone: {tone}, Behavior: {behavior}"
        chatbot.save()

        # Redirect to the next step (step 3)
        return redirect('create_chatbot_step3', chatbot_id=chatbot.id)

    return render(request, 'create_chatbot_step2.html', {'chatbot': chatbot})


def create_chatbot_step3(request, chatbot_id):
    chatbot = Chatbot.objects.get(id=chatbot_id, user=request.user)
    
    if request.method == 'POST':
        # Handle personality form
        personality_form = ChatbotPersonalityForm(request.POST, instance=chatbot)
        document_form = DocumentUploadForm(request.POST, request.FILES)

        if personality_form.is_valid() and document_form.is_valid():
            # Save personality data
            personality_form.save()

            # Save document file
            document = document_form.save(commit=False)
            document.chatbot = chatbot
            document.save()

            return redirect('dashboard')
        else:
            # If forms are not valid, return to the page with errors
            return render(request, 'create_chatbot_step3.html', {
                'chatbot': chatbot,
                'personality_form': personality_form,
                'document_form': document_form,
            })
    else:
        personality_form = ChatbotPersonalityForm(instance=chatbot)
        document_form = DocumentUploadForm()

    return render(request, 'create_chatbot_step3.html', {
        'chatbot': chatbot,
        'personality_form': personality_form,
        'document_form': document_form,
    })




@login_required
def dashboard(request):
    # Get all chatbots created by the logged-in user
    user_chatbots = Chatbot.objects.filter(user=request.user)

    # Calculate statistics
    total_chatbots = user_chatbots.count()
    chatbot_stats = [
        {
            "name": chatbot.name,
            "created_at": chatbot.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format the date
            "description": chatbot.description,
        }
        for chatbot in user_chatbots
    ]

    context = {
        "total_chatbots": total_chatbots,
        "chatbot_stats": chatbot_stats,
    }

    return render(request, "dashboard.html", context)

def default_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('dashboard')  # Redirect to dashboard
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def validate_file(file):
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        return False, 'File size exceeds 5MB.'
    return True, None