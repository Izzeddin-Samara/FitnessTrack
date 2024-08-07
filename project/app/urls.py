from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('new_session/<int:coach_id>/', views.new_session, name='new_session'),
    path('create_session/<int:coach_id>/', views.create_session, name='create_session'),
    path('update_session/<int:session_id>/', views.update_session, name='update_session'),
    path('delete_session/<int:session_id>/', views.delete_session, name='delete_session'),
    path('review_form/<int:coach_id>/', views.review_form, name='review_form'),
    path('create_review/<int:coach_id>/', views.create_review, name='create_review'),
    path('update_review/<int:review_id>/', views.update_review, name='update_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('logout/', views.logout_user, name='logout_user'),
]
