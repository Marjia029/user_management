from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import UserProfile

def home(request):
    """Display the home page"""
    return render(request, 'courses/home.html')

def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'courses/register.html', {'form': form})

@login_required
def manage_users(request):
    """Display all users and allow admin to manage roles"""
    # Check if user is admin
    if request.user.profile.role != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    users = User.objects.all().select_related('profile')
    return render(request, 'courses/manage_users.html', {'users': users})

@login_required
def change_role(request, user_id):
    """Allow admin to change user roles"""
    # Check if user is admin
    if request.user.profile.role != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        new_role = request.POST.get('role')
        
        if new_role in ['admin', 'advisor', 'normal']:
            user.profile.role = new_role
            user.profile.save()
            messages.success(request, f'Role updated successfully for {user.username}!')
        else:
            messages.error(request, 'Invalid role selected.')
    
    return redirect('manage_users')