from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import MyTokenObtainPairView, DegreeListView, DepartmentListView, StudentListView, DashboardStatsView

urlpatterns = [
    path('', views.get_routes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.UserViewSet.as_view({'get': 'retrieve', 'post': 'post'})),
    path('user/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
    path('student/', views.StudentViewSet.as_view({'post': 'post'})),
    path('students/<int:pk>/', views.StudentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='student-detail'),
    path('faculty/<int:pk>/', views.FacultyViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='faculty-detail'),
    path('departments/<int:pk>/', views.DepartmentViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='department-detail'),
    path('parents/<int:pk>/', views.ParentViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='parent-detail'),
    path('degrees/', DegreeListView.as_view(), name='degree-list'),
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('users/', views.UserListView.as_view(), name='user-list'),

]
