from django.contrib import admin
from django.urls import path
from . import views

app_name = 'records' 

urlpatterns = [
    # Admin endpoints
    path('admin/', admin.site.urls),
    
    # Class endpoints
    path('classes/', views.ClassList.as_view(), name='class-list'),
    path('classes/<int:pk>/', views.ClassDetail.as_view(), name='class-detail'),
    
    # Student endpoints
    path('students/', views.StudentList.as_view(), name='student-list'),
    path('students/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    
    # Test endpoints
    path('tests/', views.TestList.as_view(), name='test-list'),
    path('tests/<int:pk>/', views.TestDetail.as_view(), name='test-detail'),
]