from django.urls import path
from .views import register_view,RegisterAPI,login_view,LoginAPI,tech_dashboard,add_project,ProjectCreateAPI,add_profile,logout_view,assign_project
urlpatterns=[
    path('register_view/',register_view,name='register_view'),
    path('api/RegisterAPI/',RegisterAPI.as_view(),name='RegisterAPI'),
    path('login_view/',login_view,name='login_view'),
    path('api/LoginAPI/',LoginAPI.as_view(),name='LoginAPI'),
    path('tech_dashboard/',tech_dashboard,name='tech_dashboard'),
    path('add_project/',add_project,name='add_project'),
    path('api/ProjectCreateAPI/',ProjectCreateAPI.as_view(),name='ProjectCreateAPI'),
    path('add_profile/',add_profile,name='add_profile'),
    path('logout_view/',logout_view,name='logout_view'),
    path('assign_project/',assign_project,name='assign_project')

    
]