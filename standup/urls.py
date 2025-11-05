from django.urls import path
    
from .views import register_view,RegisterAPI,login_view,LoginAPI,tech_dashboard,add_project,ProjectCreateAPI,add_profile,logout_view,assign_project,ProjectAssignmentAPIView,employee_dashboard,approval_list,approve_user,reject_user,ApproveUserAPI,RejectUserAPI,add_emp_profile,EmpProfileView,submit_daily_task,team_lead_task_view,employee_task_history,schedule_meeting,update_meeting,cancel_meeting,ScheduleMeetingAPIView,UpdateMeetingAPIView,CancelMeetingAPIView,ApprovedListsAPI,logout_api,ProjectList,ParticipantMeetingsAPIView,lead_daily_task,lead_task_history,team_lead_all_tasks_api,SaveFCMTokenAPIView,SendNotificationAPIView,RegisterFCMTokenAPI, CheckNotificationAPIView,SubmitDailyUpdateAPIView,employee_extra_history,change_role,api_change_role,weekly_report,download_weekly_report_pdf
urlpatterns=[
    path('register_view/',register_view,name='register_view'),
  
    path('login_view/',login_view,name='login_view'),
   
    path('tech_dashboard/',tech_dashboard,name='tech_dashboard'),
    path('add_project/',add_project,name='add_project'),
   
    path('add_profile/',add_profile,name='add_profile'),
    path('logout_view/',logout_view,name='logout_view'),
    path('assign_project/',assign_project,name='assign_project'),
    # path('api/ProjectAssignmentAPIView/',ProjectAssignmentAPIView.as_view(),name='ProjectAssignmentListCreateAPIView'),
    path('employee_dashboard/',employee_dashboard,name='employee_dashboard'),
    path('approval_list/',approval_list,name='approval_list'),
    path('approve_user/<int:user_id>/',approve_user,name='approve_user'),
    path('reject-user/<int:user_id>/', reject_user, name='reject_user'),
  
    path('add_emp_profile/',add_emp_profile,name='add_emp_profile'),
   
    path('submit_daily_task/',submit_daily_task,name='submit_daily_task'),
    path('team_lead_task_view/',team_lead_task_view,name='team_lead_task_view'),
    path('employee_task_history/',employee_task_history,name='employee_task_history'),
    path('schedule_meeting/',schedule_meeting,name='schedule_meeting'),
    # path('lead_meetings_list/',lead_meetings_list,name='lead_meetings_list')
    path('update_meeting/<int:pk>/',update_meeting,name='update_meeting'),
    path('cancel_meeting/<int:pk>/',cancel_meeting,name='cancel_meeting'),
    path("save-fcm-token/", SaveFCMTokenAPIView.as_view(), name="save-fcm-token"),
  
    path('send-notification/', SendNotificationAPIView.as_view(), name='send-notification'),
  
    path('employee_extra_history/',employee_extra_history,name='employee_extra_history'),
    path('change_role/<int:user_id>/<str:new_role>/', change_role, name='change_role'),
    path('weekly-report/', weekly_report, name='weekly_report'),
    path('weekly-report/download/', download_weekly_report_pdf, name='download_weekly_report_pdf'),



   



# api urls

path('api/RegisterAPI/',RegisterAPI.as_view(),name='RegisterAPI'),# register api
path('api/LoginAPI/',LoginAPI.as_view(),name='LoginAPI'),#login api  
path('api/logout_api/',logout_api,name='logout_api'),#logout api

# project api
path('api/ProjectCreateAPI/',ProjectCreateAPI.as_view(),name='ProjectCreateAPI'),#add project api
path('api/ProjectAssignmentAPIView/',ProjectAssignmentAPIView.as_view(),name='ProjectAssignmentListCreateAPIView'),# assignproject api
path('api/ProjectList/',ProjectList.as_view(),name='ProjectList'),#projectlist
# registeruser approve
path('api/ApproveUserAPI/<int:user_id>/',ApproveUserAPI.as_view(),name='ApproveUserAPI'),#approve the user
path('api/requesting_to_approve/',ApproveUserAPI.as_view(),name='ApproveUserAPIList'),#request to approve regiser user
path('api/RejectUserAPI/<int:user_id>/',RejectUserAPI.as_view(),name='RejectUserAPI'),# reject the register user
path('api/ApprovedList/',ApprovedListsAPI.as_view(),name='ApprovedListsAPI'),#approved register list

#emp profile create
path('api/EmpProfileView/',EmpProfileView.as_view(),name='EmpProfileView'),

#daily task update
# path('api/SubmitDailyTaskAPIView/',SubmitDailyTaskAPIView.as_view(),name='SubmitDailyTaskAPIView'),

# daily standup meeting
path('api/ScheduleMeetingAPIView/',ScheduleMeetingAPIView.as_view(),name='ScheduleMeetingAPIView'),
path('api/UpdateMeetingAPIView/<int:pk>/',UpdateMeetingAPIView.as_view(),name='UpdateMeetingAPIView'),
path('api/CancelMeetingAPIView/<int:pk>/',CancelMeetingAPIView.as_view(),name='CancelMeetingAPIView'),
path('api/ParticipantMeetingsAPIView/',ParticipantMeetingsAPIView.as_view(),name='ParticipantMeetingsAPIView'),

#lead task update
path('lead_daily_task/',lead_daily_task,name='lead_daily_task'),
path('lead_task_history/',lead_task_history,name='lead_task_history'),
path('api/team-lead/all-tasks/', team_lead_all_tasks_api, name='team_lead_all_tasks_api'),
path('api/RegisterFCMTokenAPI/',RegisterFCMTokenAPI.as_view(),name='RegisterFCMTokenAPI'),
path('api/SubmitDailyUpdateAPIView/',SubmitDailyUpdateAPIView,name='SubmitDailyUpdateAPIView'),
# path('api/today/task/',SubmitTodayTaskAPIView.as_view(),name='SubmitTodayTaskAPIView')
# path('api/checknotification/',CheckNotificationAPIView.as_view(),name='RegisterFCMTokenAPI')
path('api_change_role/',api_change_role,name='api_change_role')


]   

