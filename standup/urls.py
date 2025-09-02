from django.urls import path
from .views import register_view,RegisterAPI,login_view,LoginAPI,tech_dashboard,add_project,ProjectCreateAPI,add_profile,logout_view,assign_project,ProjectAssignmentAPIView,employee_dashboard,approval_list,approve_user,reject_user,ApproveUserAPI,RejectUserAPI,add_emp_profile,EmpProfileView,submit_daily_task,team_lead_task_view,employee_task_history,schedule_meeting,update_meeting,cancel_meeting,SubmitDailyTaskAPIView,ScheduleMeetingAPIView,UpdateMeetingAPIView,CancelMeetingAPIView,ApprovedListsAPI,logout_api,ProjectList,ParticipantMeetingsAPIView
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
    path('assign_project/',assign_project,name='assign_project'),
    path('api/ProjectAssignmentAPIView/',ProjectAssignmentAPIView.as_view(),name='ProjectAssignmentListCreateAPIView'),
    path('employee_dashboard/',employee_dashboard,name='employee_dashboard'),
    path('approval_list/',approval_list,name='approval_list'),
    path('approve_user/<int:user_id>/',approve_user,name='approve_user'),
    path('reject-user/<int:user_id>/', reject_user, name='reject_user'),
    path('api/ApproveUserAPI/<int:user_id>/',ApproveUserAPI.as_view(),name='ApproveUserAPI'),
    path('api/ApproveUserAPI/',ApproveUserAPI.as_view(),name='ApproveUserAPIList'),
    path('api/RejectUserAPI/<int:user_id>/',RejectUserAPI.as_view(),name='RejectUserAPI'),
    path('add_emp_profile/',add_emp_profile,name='add_emp_profile'),
    path('api/EmpProfileView/',EmpProfileView.as_view(),name='EmpProfileView'),
    path('submit_daily_task/',submit_daily_task,name='submit_daily_task'),
    path('team_lead_task_view/',team_lead_task_view,name='team_lead_task_view'),
    path('employee_task_history/',employee_task_history,name='employee_task_history'),
    path('schedule_meeting/',schedule_meeting,name='schedule_meeting'),
    # path('lead_meetings_list/',lead_meetings_list,name='lead_meetings_list')
    path('update_meeting/<int:pk>/',update_meeting,name='update_meeting'),
    path('cancel_meeting/<int:pk>/',cancel_meeting,name='cancel_meeting'),
    path('api/SubmitDailyTaskAPIView/',SubmitDailyTaskAPIView.as_view(),name='SubmitDailyTaskAPIView'),
    # path('api/schedule_meeting_api/',schedule_meeting_api,name='schedule_meeting_api')
    path('api/ScheduleMeetingAPIView/',ScheduleMeetingAPIView.as_view(),name='ScheduleMeetingAPIView'),
    path('api/UpdateMeetingAPIView/<int:pk>/',UpdateMeetingAPIView.as_view(),name='UpdateMeetingAPIView'),
    path('api/CancelMeetingAPIView/<int:pk>/',CancelMeetingAPIView.as_view(),name='CancelMeetingAPIView'),
    path('api/ApprovedListsAPI/',ApprovedListsAPI.as_view(),name='ApprovedListsAPI'),
    path('api/logout_api/',logout_api,name='logout_api'),
    path('api/ProjectList/',ProjectList.as_view(),name='ProjectList'),
    path('api/ParticipantMeetingsAPIView/',ParticipantMeetingsAPIView.as_view(),name='ParticipantMeetingsAPIView')
    


    
]