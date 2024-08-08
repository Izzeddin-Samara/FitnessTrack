from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import models
import bcrypt
from django.contrib.auth import logout
from .models import Session, Review, Coach, User

# Index view
def index(request):
    return render(request, 'index.html')

# User login view
def login(request):
    if request.method == 'POST':
        user = models.check(request)
        if user and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['userid'] = user.id
            messages.success(request, "Login successful", extra_tags='login')
            return redirect('/user_dashboard')
        else:
            messages.error(request, "Invalid email or password", extra_tags='login' )
    return redirect('/')

# User registration view
def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        user = models.add_user(request.POST)
        if user:
            messages.success(request, "Registered successfully", extra_tags='register')
            return render(request, 'user_dashboard.html', {'user': user})
        else:
            messages.error(request, "User creation failed", extra_tags='register')
            return redirect('/')

    return redirect('/')

# User dashboard view
def user_dashboard(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        user = models.get_user(user_id)
        user_sessions = models.user_sessions(user_id)
        user_reviews = models.user_reviews(user_id)
        all_the_coaches = models.show_all_coaches(request)
        return render(request, 'user_dashboard.html', {
            'user': user,
            'user_sessions': user_sessions,
            'user_reviews': user_reviews,
            'all_the_coaches': all_the_coaches
        })
    return redirect('/login')

# New session view
def new_session(request, coach_id):
    coach = models.get_coach(coach_id)
    return render(request, 'session_form.html', {'coach_id': coach_id, 'coach_name': f"{coach.first_name} {coach.last_name}"})

# Create session view
def create_session(request, coach_id):
    if request.method == 'POST':
        user_id = request.session['userid']
        date = request.POST['date']
        duration = request.POST['duration']  # Use the selected value
        
        coach = models.get_coach(coach_id)
        user = models.get_user(user_id)
        
        session = models.Session.objects.create(
            coach=coach,
            user=user,
            date=date,
            duration=duration
        )
        messages.success(request, f"Session created successfully with coach {coach.first_name} {coach.last_name}")
        return redirect('/user_dashboard')
    return redirect('/')

# Update session view
def update_session(request, session_id):
    session = get_object_or_404(models.Session, id=session_id)
    if request.method == 'POST':
        session.date = request.POST['date']
        session.duration = request.POST['duration']
        session.save()
        messages.success(request, f"Session updated successfully with coach {session.coach.first_name} {session.coach.last_name}")
        return redirect('/user_dashboard')
    return render(request, 'update_session.html', {'session': session, 'coach_name': f"{session.coach.first_name} {session.coach.last_name}"})

# Delete session view
def delete_session(request, session_id):
    session = get_object_or_404(models.Session, id=session_id)
    coach_name = f"{session.coach.first_name} {session.coach.last_name}"
    session.delete()
    messages.success(request, f"Session with coach {coach_name} deleted successfully")
    return redirect('/user_dashboard')

# Review form view
def review_form(request, coach_id):
    coach = models.get_coach(coach_id)
    reviews = Review.objects.filter(coach=coach).select_related('user')
    return render(request, 'review_form.html', {'coach_id': coach_id, 'coach_name': f"{coach.first_name} {coach.last_name}", 'reviews': reviews})

# Create review view
def create_review(request, coach_id):
    if request.method == 'POST':
        user_id = request.session['userid']
        content = request.POST['content']
        
        coach = models.get_coach(coach_id)
        user = models.get_user(user_id)
        
        # Check if the review already exists
        existing_review = Review.objects.filter(coach=coach, user=user).first()
        if existing_review:
            messages.error(request, "You have already reviewed this coach.")
            return redirect(f'/review_form/{coach_id}')
        
        review = models.Review.objects.create(
            coach=coach,
            user=user,
            content=content
        )
        messages.success(request, f"Review submitted successfully for coach {coach.first_name} {coach.last_name}")
        return redirect('/user_dashboard')
    return redirect('/')

# Update review view
def update_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.method == 'POST':
        review.content = request.POST['content']
        review.save()
        messages.success(request, f"Review updated successfully for coach {review.coach.first_name} {review.coach.last_name}")
        return redirect('/user_dashboard')
    return render(request, 'update_review.html', {'review': review, 'coach_name': f"{review.coach.first_name} {review.coach.last_name}"})

# Delete review view
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    coach_name = f"{review.coach.first_name} {review.coach.last_name}"
    review.delete()
    messages.success(request, f"Review for coach {coach_name} deleted successfully")
    return redirect('/user_dashboard')

# Logout view
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/')

def about_us(request):
    return render(request, 'about_us.html')

def terms_of_use(request):
    return render(request, 'terms.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')