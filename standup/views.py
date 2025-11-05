from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib import messages
from rest_framework import permissions
# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterForm,ProjectForm,ProjectAssignmentForm,ApproveUserForm,EmpProfileForm,DailyTaskForm,MeetingForm,ProfileForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,ProjectSerializer,RejectUserSerializer,ApproveUserSerializer,EmpProfileSerializer,MeetingSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User,Profile,EmpProfile,DailyUpdates
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import FCMToken
from datetime import timedelta
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DailyUpdates, Project
from .firebase import send_push_notification
from rest_framework import generics, permissions
from .models import Meeting
from .serializers import MeetingSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta, time
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import DailyUpdates
from .serializers import DailyUpdatesSerializer 
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Meeting
from .serializers import LoginSerializer,DailyUpdatesSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ProjectAssignment
from .serializers import ProjectAssignmentSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Meeting
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from datetime import timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import DailyUpdates

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import MeetingForm
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from .models import Project

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect
from standup.firebase import notify_user  # adjust path according to your project

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from standup.models import FCMToken,FCMNotification

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DailyTaskForm
from .models import DailyUpdates
from django.utils import timezone
from datetime import datetime, time, timedelta
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DailyTaskForm
from .models import DailyUpdates  # or whatever your model is
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import FCMToken
from .serializers import FCMTokenSerializer
from datetime import datetime
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DailyUpdates
from .serializers import DailyUpdatesSerializer
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from .models import DailyUpdates 
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import User  # adjust your model name
# def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.is_pending = True
#             user.save()
#             messages.success(request, "Registration successful! Wait for lead approval.")
#             return redirect("login_view")
#         else:
           
#             print("Form errors:", form.errors)
#             messages.error(request, "There was an error in your form. Please check and try again.")
#     else:
#         form = RegisterForm()
#     return render(request, "register.html", {"form": form})
def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password1")
        phone = request.POST.get("phone")

        # 🧩 Check if user already exists
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            # ✅ Allow re-registration for rejected users
            if not existing_user.is_approved and not existing_user.is_pending and not existing_user.is_active:
                existing_user.username = username
                existing_user.set_password(password)
                existing_user.is_pending = True
                existing_user.is_approved = False
                existing_user.is_active = False
                existing_user.save()

                messages.success(request, "Re-registration successful! Wait for lead approval.")
                return redirect("login_view")
            else:
                messages.error(request, "User already registered or pending approval.")
                return redirect("login_view")

        # 🆕 Otherwise, handle normal registration
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_pending = True
            user.is_approved = False
            user.save()
            messages.success(request, "Registration successful! Wait for lead approval.")
            return redirect("login_view")
        else:
            print("Form errors:", form.errors)
            messages.error(request, "There was an error in your form. Please check and try again.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})




def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error = "You need to register first."
            return render(request, 'login.html', {'error': error})

        # Check if user is approved
        if not user.is_approved:
            error = "Your account is not approved yet. Please wait for team lead approval."
            return render(request, 'login.html', {'error': error})

        # Authenticate user
        user_auth = authenticate(request, username=user.username, password=password)
        if user_auth is not None:
            login(request, user_auth)

            # Role-based redirect
            if user.role == "lead":
                return redirect('tech_dashboard')
            elif user.role == "employee":
                return redirect('employee_dashboard')
            elif user.role == "ceo" :
                return redirect('tech_dashboard')
            else:
                return redirect('login')
        else:
            error = "Invalid email or password."

    return render(request, 'login.html', {'error': error})


class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token,created  = Token.objects.get_or_create(user=user)
            
           

            return Response({
                "message": "User registered successfully. Pending approval.","token" : token.key
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='login_view')
def approval_list(request):
    if request.user.role  not in ['lead' ,'ceo']:
        return redirect('login_view')
  
    
   
    pending_users = User.objects.filter(is_pending=True).order_by('-date_joined')
    
  
    approved_users = User.objects.filter(is_approved=True, is_pending=False)
    
    return render(request, 'approve.html', {
        'pending_users': pending_users,
        'approved_users': approved_users
    })



@login_required(login_url='login_view')
def approve_user(request, user_id):
    
    if request.user.role  not in ['lead' ,'ceo']:
        return redirect('login_view')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ApproveUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = True
            user.is_pending = False 
            user.is_active = True

            # user.is_active = user.is_approved  
            user.save()
            return redirect('approval_list')
    else:
        form = ApproveUserForm(instance=user)
    return render(request, 'approve_user.html', {'form': form, 'user': user})


@login_required(login_url='login_view')
def reject_user(request, user_id):
    # if request.user.role != 'lead':
    if request.user.role  not in ['lead' ,'ceo']:
        return redirect('login_view')
    
    user = get_object_or_404(User, id=user_id)
    user.is_pending = False   # remove from pending list
    user.is_approved = False
    user.is_active = False
    user.save()
    
    return redirect('approval_list')


User = get_user_model()

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # ✅ The serializer already validated everything
            user = serializer.validated_data["user"]

            # Generate token
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Login successful.",
                "token": token.key,
                "role": user.role,
                "is_approved" : user.is_approved,
                "is_pending" : user.is_pending
               
                
            }, status=status.HTTP_200_OK)

        # If invalid, return serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@login_required
def add_project(request):
    if request.user.role not in ['lead', 'ceo', 'management']:
        return redirect("login")  # only lead can add project

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.lead = request.user
            project.save()
            return redirect("tech_dashboard")
    else:
        form = ProjectForm()

    return render(request, "addproject.html", {"form": form})


from django.contrib.auth import get_user_model
User = get_user_model()

@login_required(login_url='login') 
def tech_dashboard(request):
    # ✅ Allow only authorized roles
    if request.user.role not in ['lead', 'ceo', 'management']:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login_view')

    now_date = timezone.localdate()
    now_time = timezone.localtime().time()
    cutoff = time(15, 30)

    employees = User.objects.filter(is_approved = True).exclude(role='ceo')
    submitted_today = DailyUpdates.objects.filter(task_date=now_date).values_list('user_id', flat=True)

    # ✅ For testing: ignore cutoff temporarily
    missed_emp = employees.exclude(id__in=submitted_today)
    meetings = Meeting.objects.filter(meeting_date__gte=now_date).order_by('meeting_date', 'meeting_time')

    # ✅ Debug prints
    print("🕒 Time:", now_time)
    print("👥 Employees:", list(employees.values_list('username', flat=True)))
    print("✅ Submitted today IDs:", list(submitted_today))
    print("❌ Missed employees:", list(missed_emp.values_list('username', flat=True)))
    print(meetings)

    return render(request, "leaddashboard.html", {
        "missed_employees": missed_emp,
        "cutoff": cutoff,
        "meetings" : meetings
    })


# @login_required(login_url='login') 
# def employee_dashboard(request):
#     if request.user.role != "employee":
#         return redirect('login_view')
    
#     now_date = timezone.localdate()
#     now_time = timezone.localtime().time()
#     user = request.user
#     all_tasks  = DailyUpdates.objects.filter(user=user)
#     total_completed = all_tasks.filter(status='completed').count()
#     total_pending = all_tasks.filter(status='pending').count()
#     total_blockers = all_tasks.filter(status='blocker').count()
#     total_planned = all_tasks.filter(status='planned').count()

#     # Only upcoming meetings (today not yet started + future)
#     meetings = request.user.meetings.filter(
#         Q(meeting_date__gt=now_date) |
#         Q(meeting_date=now_date, meeting_time__gte=now_time)
#     ).order_by('meeting_date', 'meeting_time')
#     context = {

#         #  today_tasks': today_tasks,
#         'total_completed': total_completed,
#         'total_pending': total_pending,
#         'total_blockers': total_blockers,
#         'total_planned': total_planned,
#         'meetings' : meetings,
#     }
#     return render(request, 'employeedashboard.html', context)





from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta
import json

# @login_required(login_url='login') 
# def employee_dashboard(request):
#     if request.user.role != "employee":
#         return redirect('login_view')
    
#     now_date = timezone.localdate()
#     now_time = timezone.localtime().time()
#     user = request.user
    
#     all_tasks = DailyUpdates.objects.filter(user=user)
#     total_completed = all_tasks.filter(status='completed').count()
#     total_pending = all_tasks.filter(status='pending').count()
#     total_blockers = all_tasks.filter(is_blocker=True).count()
    
#     # Get last 7 days for chart
#     end_date = now_date
#     start_date = end_date - timedelta(days=6)
    
#     # Get tasks in date range
#     recent_tasks = DailyUpdates.objects.filter(
#         user=user,
#         task_date__gte=start_date,
#         task_date__lte=end_date
#     ).select_related('project').order_by('task_date')
    
#     # Prepare dates for chart
#     dates = []
#     current_date = start_date
#     while current_date <= end_date:
#         dates.append(current_date.strftime('%b %d'))  # "Nov 04"
#         current_date += timedelta(days=1)
#     daily_breakdown = defaultdict(lambda: defaultdict(dict))
#     # current_date = start_date
#     while current_date <= end_date:
#         day_tasks = recent_tasks.filter(task_date=current_date)
#         did_completed = day_tasks.filter(is_yesterday=True, status='completed').count()
#         did_pending = day_tasks.filter(is_yesterday=True, status='pending').count()
#         will_do_pending = day_tasks.filter(is_today=True, status='pending').count()
#         blockers = day_tasks.filter(is_blocker=True).count()
      
#         daily_breakdown.append({
#             'date': current_date.strftime('%b %d'),
#             'did_completed': did_completed,
#             'did_pending': did_pending,
#             'will_do_pending': will_do_pending,
#             'blockers': blockers
#         })
#         current_date += timedelta(days=1)

#     # Calculate time spent by project
#     projects = list(recent_tasks.values_list('project__name', flat=True).distinct())
#     time_by_project = []
#     for project_name in projects:
#         tasks_for_project = recent_tasks.filter(project__name=project_name)
#         total_seconds = sum([
#             t.time_taken.total_seconds() for t in tasks_for_project if t.time_taken
#         ])
#         hours = total_seconds / 3600
#         time_by_project.append({
#             'project': project_name,
#             'hours': round(hours, 2)
#         })

#     time_by_project.sort(key=lambda x: x['hours'], reverse=True)
#     project_names = [item['project'] for item in time_by_project]
#     time_spent = [item['hours'] for item in time_by_project]

#     chart_data = {
#         'dates': dates,
#         'breakdown': daily_breakdown,
#         'projectNames': project_names,
#         'timeSpent': time_spent
#     }

#     # Upcoming meetings
#     meetings = request.user.meetings.filter(
#         Q(meeting_date__gt=now_date) |
#         Q(meeting_date=now_date, meeting_time__gte=now_time)
#     ).order_by('meeting_date', 'meeting_time')

#     context = {
#         'total_completed': total_completed,
#         'total_pending': total_pending,
#         'total_blockers': total_blockers,
#         'chart_data': json.dumps(chart_data),
#         'meetings': meetings,
#     }

#     return render(request, 'employeedashboard.html', context)
    


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import json
from collections import defaultdict
from .models import DailyUpdates

@login_required(login_url='login')
def employee_dashboard(request):
    if request.user.role != "employee":
        return redirect('login_view')

    user = request.user
    now_date = timezone.localdate()

    # Summary
    all_tasks = DailyUpdates.objects.filter(user=user)
    total_completed = all_tasks.filter(status='completed').count()
    total_pending = all_tasks.filter(status='pending').count()
    total_blockers = all_tasks.filter(is_blocker=True).count()

    # Date range (7 days)
    end_date = now_date
    start_date = end_date - timedelta(days=6)
    recent_tasks = DailyUpdates.objects.filter(
        user=user,
        task_date__range=(start_date, end_date)
    ).select_related('project')

    # daily_data[date][project] = {completed, pending, planned, blockers}
    daily_data = defaultdict(lambda: defaultdict(lambda: {'completed': 0, 'pending': 0, 'planned': 0, 'blockers': 0}))

    for task in recent_tasks:
        date_label = task.task_date.strftime('%b %d')
        project = task.project.name if task.project else 'Unassigned'

        if task.status == 'completed':
            daily_data[date_label][project]['completed'] += 1
        elif task.status == 'pending' and not task.is_today and not task.is_yesterday:
            daily_data[date_label][project]['planned'] += 1
        elif task.status == 'pending':
            daily_data[date_label][project]['pending'] += 1

        if task.is_blocker:
            daily_data[date_label][project]['blockers'] += 1

    # Chart data
    dates = [(start_date + timedelta(days=i)).strftime('%b %d') for i in range(7)]
    all_projects = sorted({p for d in daily_data.values() for p in d.keys()})

    # Assign one color per project
    color_palette = [
        '#0d6efd', '#6610f2', '#6f42c1', '#d63384', '#dc3545',
        '#fd7e14', '#ffc107', '#198754', '#20c997', '#0dcaf0'
    ]

    datasets = []
    for i, project in enumerate(all_projects):
        data_points = []
        for date in dates:
            # total tasks that day for that project (all statuses)
            p = daily_data[date][project]
            total = p['completed'] + p['pending'] + p['planned'] + p['blockers']
            data_points.append(total)
        datasets.append({
            'label': project,
            'data': data_points,
            'backgroundColor': color_palette[i % len(color_palette)],
            'borderRadius': 6,
            'barPercentage': 0.7,
        })

    chart_data = {
        'dates': dates,
        'datasets': datasets,
        'project_breakdown': daily_data,  # for tooltip
    }
    meetings = Meeting.objects.filter(
        meeting_date__gte=now_date
    ).filter(
        participants=user
    ).order_by('meeting_date', 'meeting_time')
    hosted_meetings = Meeting.objects.filter(host=user)
    all_meetings = meetings | hosted_meetings  # union of both
    all_meetings = all_meetings.distinct().order_by('meeting_date', 'meeting_time')
    print("📅 Upcoming meetings for employee:", list(all_meetings.values_list('about', flat=True)))

    context = {
        'total_completed': total_completed,
        'total_pending': total_pending,
        'total_blockers': total_blockers,
        'chart_data': json.dumps(chart_data),
        'meetings': all_meetings
    }
    return render(request, 'employeedashboard.html', context)


   



class ProjectCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Only Tech Lead can create
        if request.user.role not in ['lead', 'ceo', 'management']:
            return Response({"error": "Only Tech Lead can add project."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(lead=request.user)  # assign lead automatically
            return Response({"message": "Project created successfully", "project": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectCreateAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def post(self, request):
       
        # if request.user.role != "lead":
        if request.user.role not in ['lead', 'ceo', 'management']:
            return Response(
                {"error": "Only Tech Lead can add project."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(lead=request.user) 
            return Response(
                {"message": "Project created successfully", "project": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProjectList(APIView):
    
    def get(self,request):
        project = Project.objects.all()
        serializer = ProjectSerializer(project,many = True)
        return Response(serializer.data,status= status.HTTP_200_OK)


@login_required
def add_profile(request):
   
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile_obj, user=request.user)
        if form.is_valid():
            
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()

           
            form.save()
            return redirect('tech_dashboard')
    else:
       
        form = ProfileForm(instance=profile_obj, user=request.user)

    return render(request, 'addprofile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')  


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_api(request):
   
    try:
        request.user.auth_token.delete()
        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )
    except Exception:
        return Response(
            {"error": "Logout failed"},
            status=status.HTTP_400_BAD_REQUEST
        )

def assign_project(request):
    if request.method == "POST":
        form = ProjectAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)  
            assignment.save()                    
            form.save_m2m()                       
            return redirect('tech_dashboard')    
    else:
        form = ProjectAssignmentForm()
    return render(request, 'assignproject.html', {'form': form})


class ProjectAssignmentAPIView(generics.ListCreateAPIView):
    queryset = ProjectAssignment.objects.all()
    serializer_class = ProjectAssignmentSerializer
    permission_classes = [IsAuthenticated]  


User = get_user_model()


class ApproveUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):

        if request.user.role != "lead":
            return Response({"error": "Only leads can view pending users."}, status=status.HTTP_403_FORBIDDEN)

        pending_users = User.objects.filter(is_approved=False)
        serializer = ApproveUserSerializer(pending_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        
        if request.user.role != "lead":
            return Response({"error": "Only leads can approve users."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, id=user_id, is_pending=True)

        role = request.data.get("role")
        if role:
            user.role = role

        user.is_approved = True
        user.is_pending = False
        user.is_active = True
        user.save()



        # send_fcm_message(
        #     fcmtoken='',
        #     notification_title='Approved',
        #     notification_body='hey your approved by techlead'
        # )


        notify_user(
                user,
                title="Registration Approved",
                body="Hey! You have been approved by your Tech Lead. You can now login."
            )


        return Response({
            "message": f"✅ User '{user.username}' approved as {user.role}."
        }, status=status.HTTP_200_OK)
    




    


class RejectUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
       
        if request.user.role != "lead":
            return Response({"error": "Only leads can reject users."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, id=user_id, is_pending=True)

        user.is_approved = False
        user.is_pending = False
        user.is_active = False
        user.save()

        return Response({
            "message": f"❌ User '{user.username}' rejected."
        }, status=status.HTTP_200_OK)
    

    






@login_required
def add_emp_profile(request):
    # Get profile if exists, else None
    profile_instance = EmpProfile.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = EmpProfileForm(
            request.POST, 
            request.FILES, 
            instance=profile_instance, 
            user=request.user
        )
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user   
            profile.save()

           
            request.user.username = form.cleaned_data.get('username', request.user.username)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()

            return redirect("employee_dashboard")  
    else:
       
        form = EmpProfileForm(instance=profile_instance, user=request.user)

    return render(request, "addprofile.html", {"form": form})


class EmpProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = EmpProfile.objects.get_or_create(user=request.user)
        serializer = EmpProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, created = EmpProfile.objects.get_or_create(user=request.user)
        serializer = EmpProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile, created = EmpProfile.objects.get_or_create(user=request.user)
        serializer = EmpProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@login_required(login_url='login')
def submit_daily_task(request):
    if request.method == 'POST':
        
        now = timezone.localtime().time()
        cutoff = time(23, 30)
        if now > cutoff:
            messages.warning(request, "⏰ Time is over! You can’t update after 10:30 AM.")
            return redirect('employee_dashboard')

        project_count = 1
        while f'project_yesterday_{project_count}' in request.POST:
            
           
            project_id = request.POST.get(f'project_yesterday_{project_count}')
            tasks = request.POST.getlist(f'tasks_yesterday_{project_count}[]')
            times = request.POST.getlist(f'time_taken_yesterday_{project_count}[]')
            statuses = request.POST.getlist(f'status_yesterday_{project_count}[]')

            for i, task in enumerate(tasks):
                task = task.strip()
                if task:
                    time_taken = timedelta(hours=1)
                    if i < len(times) and times[i]:
                        h, m = map(int, times[i].split(':'))
                        time_taken = timedelta(hours=h, minutes=m)

                    DailyUpdates.objects.create(
                        user=request.user,
                        project_id=project_id,
                        task_description=task,
                        time_taken=time_taken,
                        status=statuses[i] if i < len(statuses) else 'pending',
                        task_date=timezone.localdate(),
                        is_yesterday=True,
                    )
            project_count += 1

        # ----------------------------
        # 2️⃣ Handle "What You Will Do Today"
        # ----------------------------
        # project_count = 1
        # while f'project_today_{project_count}' in request.POST:
        #     project_id = request.POST.get(f'project_today_{project_count}')
        #     tasks = request.POST.getlist(f'tasks_today_{project_count}[]')
        #     times = request.POST.getlist(f'time_taken_today_{project_count}[]')
        #     statuses = request.POST.getlist(f'status_today_{project_count}[]')

        #     for i, task in enumerate(tasks):
        #         task = task.strip()
        #         if task:
        #             time_taken = timedelta(hours=1)
        #             if i < len(times) and times[i]:
        #                 h, m = map(int, times[i].split(':'))
        #                 time_taken = timedelta(hours=h, minutes=m)

        #             DailyUpdates.objects.create(
        #                 user=request.user,
        #                 project_id=project_id,
        #                 task_description=task,
        #                 time_taken=time_taken,
        #                 status=statuses[i] if i < len(statuses) else 'pending',
        #                 task_date=timezone.localdate(),
        #                 is_today=True,
        #             )
        #     project_count += 1

        # ----------------------------
# 2️⃣ Handle "What You Will Do Today"
# ----------------------------
        today_projects = [
            key for key in request.POST.keys()
            if key.startswith("project_today_")
        ]

        for key in today_projects:
            index = key.split("_")[-1]  # e.g. 'project_today_3' → '3'
            project_id = request.POST.get(f'project_today_{index}')
            tasks = request.POST.getlist(f'tasks_today_{index}[]')
            times = request.POST.getlist(f'time_taken_today_{index}[]')
            statuses = request.POST.getlist(f'status_today_{index}[]')

            for i, task in enumerate(tasks):
                task = task.strip()
                if task:
                    time_taken = timedelta(hours=1)
                    if i < len(times) and times[i]:
                        h, m = map(int, times[i].split(':'))
                        time_taken = timedelta(hours=h, minutes=m)

                    DailyUpdates.objects.create(
                        user=request.user,
                        project_id=project_id,
                        task_description=task,
                        time_taken=time_taken,
                        status=statuses[i] if i < len(statuses) else 'pending',
                        task_date=timezone.localdate(),
                        is_today=True,
                    )


        
        blocker_project = request.POST.get("blocker_project_id")
        blockers_text = request.POST.get("blockers_description")

        if blockers_text:
            DailyUpdates.objects.create(
                user=request.user,
                project_id=blocker_project if blocker_project else None,
                task_description=blockers_text.strip(),
                status="blocker",
                is_blocker=True,
                task_date=timezone.localdate(),
            )

        messages.success(request, "✅ Daily Standup submitted successfully!")
        if hasattr(request.user, 'role') and request.user.role == 'lead':
            return redirect('lead_dashboard')
        else:
            return redirect('employee_dashboard')
        

    else:
        form = DailyTaskForm()
        today = timezone.localdate()
        return render(request, 'dailystandup.html', {'form': form, 'today': today})



@login_required(login_url='login')
def lead_daily_task(request):
    if request.method == 'POST':
        now = timezone.localtime().time()
        cutoff = time(23, 30)
        if now > cutoff:
            messages.warning(request, "⏰ Time is over! You can’t update after 10:30 AM.")
            return redirect('tech_dashboard')  

        project_count = 1
        while f'project_{project_count}' in request.POST:
            project_id = request.POST.get(f'project_{project_count}')
            tasks = request.POST.getlist(f'tasks_project_{project_count}[]')
            times = request.POST.getlist(f'time_taken_{project_count}[]')
            statuses = request.POST.getlist(f'status_{project_count}[]')

            for i, task in enumerate(tasks):
                task = task.strip()
                if task:
                    time_taken = None
                    if i < len(times) and times[i]:
                        h, m = map(int, times[i].split(':'))
                        from datetime import timedelta
                        time_taken = timedelta(hours=h, minutes=m)

                    DailyUpdates.objects.create(
                        user=request.user,
                        project_id=project_id,
                        task_description=task,
                        time_taken=time_taken,
                        status=statuses[i] if i < len(statuses) else 'pending',
                        task_date=timezone.localdate()
                    )

            project_count += 1

        # ✅ These must be outside the loop
        today_project = request.POST.get("today_project_id")
        today_task_description = request.POST.get("today_task_description")

        if today_project and today_task_description:
            DailyUpdates.objects.create(
                user=request.user,
                project_id=today_project,
                task_description=today_task_description.strip(),
                status="planned",
                task_date=timezone.localdate(),
            )

        blocker_project = request.POST.get("blocker_project_id")
        blockers_text = request.POST.get("blockers_description")

        if blockers_text:
            DailyUpdates.objects.create(
                user=request.user,
                project_id=blocker_project if blocker_project else None,
                task_description=blockers_text.strip(),
                status="blocker",
                task_date=timezone.localdate(),
            )

        
        messages.success(request, "✅ Daily Standup submitted successfully!")
        return redirect('tech_dashboard')

    else:
        form = DailyTaskForm()
        today = timezone.localdate()
        return render(request, 'dailystandup.html', {'form': form, 'today': today})





def team_lead_task_view(request):
    today = timezone.localdate()

    # 🔍 Filters
    search = request.GET.get("search", "").strip()
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    status_filter = request.GET.get("status", "").strip()
    username_filter = request.GET.get("username", "").strip()

    # ✅ Base queryset
    updates = DailyUpdates.objects.select_related("user", "project")

    # 🗓 Apply date range filter
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            updates = updates.filter(created_at__date__range=(start, end))
        except ValueError:
            updates = updates.filter(created_at__date=today)
    elif start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            updates = updates.filter(created_at__date__gte=start)
        except ValueError:
            updates = updates.filter(created_at__date=today)
    elif end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            updates = updates.filter(created_at__date__lte=end)
        except ValueError:
            updates = updates.filter(created_at__date=today)
    else:
        # Default: today
        updates = updates.filter(created_at__date=today)

    # 🔍 Search and other filters
    if search:
        updates = updates.filter(
            Q(user__username__icontains=search) |
            Q(project__name__icontains=search)
        )

    if username_filter:
        updates = updates.filter(user__username=username_filter)

    if status_filter:
        updates = updates.filter(status__iexact=status_filter)

    # ✅ Sort results
    updates = updates.order_by("user__username", "-created_at")

    
    grouped = defaultdict(lambda: defaultdict(lambda: {"yesterday": [], "today": [], "blockers": []}))

    for update in updates:
        emp = update.user.username
        date_key = update.created_at.date().strftime("%b %d, %Y")

        if update.is_blocker:
            grouped[emp][date_key]["blockers"].append(update)
        elif update.is_yesterday:
            grouped[emp][date_key]["yesterday"].append(update)
        elif update.is_today:
            grouped[emp][date_key]["today"].append(update)

    # ✅ Sort date keys (most recent first)
    final_grouped = {}
    for emp, date_data in grouped.items():
        sorted_dates = dict(
            sorted(
                date_data.items(),
                key=lambda x: datetime.strptime(x[0], "%b %d, %Y"),
                reverse=True
            )
        )
        final_grouped[emp] = sorted_dates

    # ✅ Pagination
    paginator = Paginator(list(final_grouped.items()), 4)
    page_number = request.GET.get("page", 1)
    if search:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    all_users = DailyUpdates.objects.values_list("user__username", flat=True).distinct()

    context = {
        "grouped_updates_page": page_obj,
        "today": today,
        "search": search,
        "start_date": start_date,
        "end_date": end_date,
        "status_filter": status_filter,
        "username_filter": username_filter,
        "all_users": all_users,
    }
    return render(request, "lead_taskupdates.html", context)







from django.core.paginator import Paginator



@login_required(login_url='login')
def employee_extra_history(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    project_filter = request.GET.get('project','') 
    tasks = DailyUpdates.objects.filter(user=request.user).order_by('-task_date','-created_at')
    if query:
        tasks = tasks.filter(
            Q(task_description__icontains=query) |
            Q(project__name__icontains=query) |
            Q(user__username__icontains=query)

        )
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if project_filter:
        tasks = tasks.filter(project__name__icontains=project_filter)


    
    for task in tasks:
        if task.time_taken:
            total_seconds = task.time_taken.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            task.time_taken_str = f"{hours}h {minutes}m"
        else:
            task.time_taken_str = "-"

    paginator = Paginator(tasks,15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)



    projects = Project.objects.all()

    return render(request, 'extraemphistory.html',{
        'page_obj' : page_obj,
        'query' : query,
        'status_filter' : status_filter,
        'project_filter': project_filter,
        'projects': projects

    })


from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .models import DailyUpdates, Project

from collections import defaultdict
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DailyUpdates

@login_required(login_url='login')
def employee_task_history(request):
    user = request.user
    selected_date = request.GET.get('date', '')

    
    all_tasks = (
        DailyUpdates.objects
        .filter(user=user)
        .select_related('project')
        .order_by('-task_date', '-created_at')
    )

    
    for t in all_tasks:
        if t.time_taken:
            total_seconds = t.time_taken.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            t.time_taken_str = f"{hours}h {minutes}m"
        else:
            t.time_taken_str = "-"

    
    grouped_history = defaultdict(list)
    for t in all_tasks:
        grouped_history[t.task_date].append(t)

    all_dates = sorted(grouped_history.keys(), reverse=True)

    
    recent_dates = all_dates[:2]
    grouped_list = [(d, grouped_history[d]) for d in recent_dates]

    
    if selected_date:
        try:
            
            selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date_obj = None

        
        selected_tasks = grouped_history.get(selected_date_obj, [])

       
        grouped_list = [(selected_date_obj, selected_tasks)] if selected_date_obj else []

   
    return render(request, 'emptaskhistory.html', {
        'grouped_list': grouped_list,
        'selected_date': selected_date,
    })




@login_required(login_url='login')
def lead_task_history(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    project_filter = request.GET.get('project','') 
    tasks = DailyUpdates.objects.filter(user=request.user).order_by('-task_date','-created_at')
    if query:
        tasks = tasks.filter(
            Q(task_description__icontains=query) |
            Q(project__name__icontains=query) |
            Q(user__username__icontains=query)

        )
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if project_filter:
        tasks = tasks.filter(project__name__icontains=project_filter)
    # convert time_taken to string for display
    for task in tasks:
        if task.time_taken:
            total_seconds = task.time_taken.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            task.time_taken_str = f"{hours}h {minutes}m"
        else:
            task.time_taken_str = "-"

    paginator = Paginator(tasks,15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    
    projects = Project.objects.all()

    return render(request, 'lead_task_history.html',{
        'page_obj' : page_obj,
        'query' : query,
        'status_filter' : status_filter,
        'project_filter': project_filter,
        'projects': projects
    }

        )


@login_required(login_url='login_view')
def schedule_meeting(request):
    
    if request.user.role not in ['lead', 'ceo', 'management']:
        messages.error(request, "You are not authorized to host a meeting.")
        return redirect('login_view')

    if request.method == 'POST':
        form = MeetingForm(request.POST,user=request.user)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.host = request.user  
            meeting.save()
            form.save_m2m()
            
             # save participants
            messages.success(request, "Meeting scheduled successfully!")
            return redirect('tech_dashboard')  # or redirect based on role if you want
    else:
        form = MeetingForm(user=request.user)
    

    return render(request, 'meeting.html', {
        'form': form,
        'today': timezone.localdate()  # optional
    })










@login_required
def update_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)

    if request.user != meeting.host:  # only the host can update
        messages.error(request, "You are not authorized to edit this meeting.")
        return redirect("employee_dashboard")

    if request.method == "POST":
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, "Meeting updated successfully.")
            return redirect("tech_dashboard")
    else:
        form = MeetingForm(instance=meeting)

    return render(request, "meeting.html", {"form": form, "meeting": meeting})


@login_required
def cancel_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)

    if request.user != meeting.host:
        messages.error(request, "Only the host can cancel this meeting.")
        return redirect("lead_dashboard")

    reason = request.POST.get("cancel_reason", "").strip()
    if not reason:
        messages.error(request, "Cancellation reason is required.")
        return redirect("update_meeting", pk=pk)

    meeting.is_cancel = True
    meeting.reason = reason
    meeting.save()

    messages.success(request, "Meeting canceled successfully.")
    return redirect("tech_dashboard")

from rest_framework import generics, permissions
from .models import Meeting
from .serializers import MeetingSerializer
from rest_framework.response import Response
from rest_framework import status

class ScheduleMeetingAPIView(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    # def get_queryset(self):
    #     now = timezone.localtime()  
    #     today = now.date()
    #     current_time = now.time()

    #     today_meetings = Q(meeting_date=today, meeting_time__gte=current_time)
    #     future_meetings = Q(meeting_date__gt=today)

    #     queryset = Meeting.objects.filter(today_meetings | future_meetings).order_by(
    #         "meeting_date", "meeting_time"
    #     )
    #     return queryset.prefetch_related("participants")
    def get_queryset(self):
        now = timezone.localtime()
        today = now.date()
        current_time = now.time()

        today_meetings = Q(meeting_date=today, meeting_time__gte=current_time)
        future_meetings = Q(meeting_date__gt=today)

        queryset = Meeting.objects.filter(
            (today_meetings | future_meetings),
            is_cancel=False   # ✅ Added line — hide canceled meetings
        ).order_by("meeting_date", "meeting_time")

        return queryset.prefetch_related("participants")


    def create(self, request, *args, **kwargs):
        # Call default create method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Get the saved instance
        instance = serializer.instance
        # Refresh instance with prefetch so participants and count are correct
        instance = Meeting.objects.filter(pk=instance.pk).prefetch_related("participants").first()
        # Serialize with prefetch applied
        data = self.get_serializer(instance).data
        return Response(data, status=status.HTTP_201_CREATED)



class ParticipantMeetingsAPIView(generics.ListAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        now = timezone.localtime()
        today = now.date()
        current_time = now.time()

        # Meetings today but not finished
        today_meetings = Q(meeting_date=today, meeting_time__gte=current_time)
        # Future meetings
        future_meetings = Q(meeting_date__gt=today)

        return Meeting.objects.filter(
            Q(participants=user) & (today_meetings | future_meetings)
        ).order_by("meeting_date", "meeting_time")


    





class UpdateMeetingAPIView(generics.RetrieveUpdateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        meeting = self.get_object()

        # Only host can update the meeting
        if meeting.host != request.user:
            return Response(
                {"detail": "You are not authorized to edit this meeting."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)
    
  



class CancelMeetingAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)

        # Only the host can cancel
        if meeting.host != request.user:
            return Response(
                {"detail": "Only the host can cancel this meeting."},
                status=status.HTTP_403_FORBIDDEN
            )

        reason = request.data.get("reason", "").strip()
        if not reason:
            return Response(
                {"detail": "Cancellation reason is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        meeting.is_cancel = True
        meeting.reason = reason
        meeting.save()

        return Response(
            {
                "detail": "Meeting canceled successfully.",
                "meeting": MeetingSerializer(meeting).data
            },
            status=status.HTTP_200_OK
        )
    

    


class ApprovedListsAPI(APIView):
    permission_classes = [permissions.AllowAny]  

    def get(self, request):
        approved_users = User.objects.filter(is_approved=True)
        serializer = ApproveUserSerializer(approved_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_lead_all_tasks_api(request):
    # date_str = request.GET.get('date')
    # start_date_str = request.GET.get('start_date')
    # end_date_str = request.GET.get('end_date')
    # username = request.GET.get('username')

    # ✅ Date or range filter
    # if date_str:
    #     try:
    #         target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    #     except ValueError:
    #         return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
    #     tasks = DailyUpdates.objects.filter(task_date=target_date)
    # elif start_date_str and end_date_str:
    #     try:
    #         start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    #         end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    #     except ValueError:
    #         return Response({"error": "Invalid date range format. Use YYYY-MM-DD."}, status=400)
    #     tasks = DailyUpdates.objects.filter(task_date__range=[start_date, end_date])
    # else:
    #     today = timezone.localdate()
    #     tasks = DailyUpdates.objects.filter(task_date=today)

    # # ✅ Username filter
    # if username:
    #     tasks = tasks.filter(user__username__iexact=username)

    # tasks = tasks.select_related('user', 'project').order_by('task_date', 'user__username')
    tasks = DailyUpdates.objects.select_related('user', 'project').order_by('-task_date')
    # ✅ Group tasks by date → then by user → then by status type
    grouped_data = {}

    for task in tasks:
        date_key = str(task.task_date)
        if date_key not in grouped_data:
            grouped_data[date_key] = {}

        user_key = task.user.username
        if user_key not in grouped_data[date_key]:
            grouped_data[date_key][user_key] = {
                "what_you_did": [],
                "what_you_will_do": [],
                "blockers": []

            }

        
        if task.is_yesterday:
            grouped_data[date_key][user_key]["what_you_did"].append({
                "project": task.project.name if task.project else None,
                "task_description": task.task_description,
                "status": task.status,
            })
        elif task.is_today:
            grouped_data[date_key][user_key]["what_you_will_do"].append({
                "project": task.project.name if task.project else None,
                "task_description": task.task_description,
                "status": task.status,
            })
        elif task.is_blocker:
            grouped_data[date_key][user_key]["blockers"].append({
                "project": task.project.name if task.project else None,
                "task_description": task.task_description,
                "status": task.status,
            })
        formatted_results = []
        for date, users in grouped_data.items():
            user_list = []
            for username, tasks_dict in users.items():
                user_list.append({
                    "username": username,
                    **tasks_dict
                })
            formatted_results.append({
                "date": date,
                "users": user_list
            })

    return Response({
        "total_records": tasks.count(),
        
        # "results": grouped_data
        "results" : formatted_results
    })





class SaveFCMTokenAPIView(APIView):
   

    def post(self, request):
        token = request.data.get("fcm_token")
        if token:
            # Update existing or create new token
            FCMToken.objects.update_or_create(user=request.user, defaults={"token": token})
            return Response({"detail": "FCM token saved."}, status=status.HTTP_200_OK)
        return Response({"detail": "FCM token not provided."}, status=status.HTTP_400_BAD_REQUEST)
    



class SendNotificationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        title = request.data.get("title")
        body = request.data.get("body")
        user_id = request.data.get("user_id")

        if not all([title, body, user_id]):
            return Response({"detail": "Missing fields"}, status=400)

        tokens = list(FCMToken.objects.filter(user_id=user_id).values_list('token', flat=True))
        if not tokens:
            return Response({"detail": "No tokens found for this user"}, status=404)

        result = send_push_notification(tokens, title, body)
        return Response(result)




class RegisterFCMTokenAPI(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    

    def post(self, request):
        serializer = FCMTokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            device_name = serializer.validated_data.get('device_name', None)
            
            # Check if token already exists
            obj, created = FCMToken.objects.update_or_create(
                token=token,
                defaults={
                    'user': request.user,
                    'device_name': device_name
                }
            )
            return Response({"message": "FCM token registered successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.contrib.auth import get_user_model
from .firebase import notify_user,send_fcm_message

User = get_user_model()

def notify_team_leads_new_user(new_user):
   
    team_leads = User.objects.filter(role='lead', is_active=True)
    for lead in team_leads:
        notify_user(
            lead,
            title="New User Registered",
            body=f"{new_user.username} has registered and is waiting for approval."
        )

class CheckNotificationAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        send_fcm_message(fcmtoken=token,notification_title = "hiiiii",notification_body = "hehehehh")
        return Response({"message": "Notification worked successfully"},status=status.HTTP_200_OK)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def SubmitDailyUpdateAPIView(request):
    

    user = request.user

    # ----------------------------------------------------------------------
    # ✅ GET — Fetch all daily standup entries for this user
    # ----------------------------------------------------------------------
    # if request.method == 'GET':
    #     date_filter = request.GET.get('date')  # optional ?date=YYYY-MM-DD
    #     queryset = DailyUpdates.objects.filter(user=user)

    #     if date_filter:
    #         queryset = queryset.filter(task_date=date_filter)

    #     queryset = queryset.order_by('-task_date', '-id')
    #     serializer = DailyUpdatesSerializer(queryset, many=True)
    #     return Response({
         
    #         "data": serializer.data
    #     }, status=status.HTTP_200_OK)
    if request.method == 'GET':
        date_filter = request.GET.get('date')  # optional ?date=YYYY-MM-DD
        queryset = DailyUpdates.objects.filter(user=user)

        if date_filter:
            queryset = queryset.filter(task_date=date_filter)
        else:
            queryset = queryset.filter(task_date=timezone.localdate())

        queryset = queryset.order_by('-task_date', '-id')

        # Separate data by category
        yesterday_updates = queryset.filter(is_yesterday=True)
        today_updates = queryset.filter(is_today=True)
        blocker_updates = queryset.filter(is_blocker=True)

        yesterday_serializer = DailyUpdatesSerializer(yesterday_updates, many=True)
        today_serializer = DailyUpdatesSerializer(today_updates, many=True)
        blocker_serializer = DailyUpdatesSerializer(blocker_updates, many=True)

        return Response({
            "date": date_filter or str(timezone.localdate()),
            "yesterday": yesterday_serializer.data,
            "today": today_serializer.data,
            "blockers": blocker_serializer.data
        }, status=status.HTTP_200_OK)

   
    elif request.method == 'POST':
        now = timezone.localtime(timezone.now())

        
        cutoff = now.replace(hour=12, minute=30, second=0, microsecond=0)
        if now > cutoff:
            return Response(
                {"message": "⏰ Time is over! You can’t update after 10:30 AM."},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data
        print("Current local time:", now)
        print("Cutoff time:", cutoff)
        print("Comparison result:", now > cutoff)


        # ----------------------------
        # 1️⃣ What You Did Yesterday
        # ----------------------------
        yesterday_tasks = data.get("yesterday", [])
        for project_block in yesterday_tasks:
            project_id = project_block.get("project_id")
            tasks = project_block.get("tasks", [])

            for t in tasks:
                if not t.get("description"):
                    continue
                h, m = map(int, t.get("time", "0:0").split(":"))
                DailyUpdates.objects.create(
                    user=user,
                    project_id=project_id,
                    task_description=t["description"].strip(),
                    time_taken=timedelta(hours=h, minutes=m),
                    status=t.get("status", "pending"),
                    task_date=timezone.localdate(),
                    is_yesterday=True,
                )

       
        today_tasks = data.get("today", [])
        for project_block in today_tasks:
            project_id = project_block.get("project_id")
            tasks = project_block.get("tasks", [])

            for t in tasks:
                if not t.get("description"):
                    continue
                h, m = map(int, t.get("time", "0:0").split(":"))
                DailyUpdates.objects.create(
                    user=user,
                    project_id=project_id,
                    task_description=t["description"].strip(),
                    time_taken=timedelta(hours=h, minutes=m),
                    status=t.get("status", "pending"),
                    task_date=timezone.localdate(),
                    is_today=True,
                )

       
        blockers = data.get("blockers", {})
        if blockers.get("description"):
            DailyUpdates.objects.create(
                user=user,
                project_id=blockers.get("project_id"),
                task_description=blockers["description"].strip(),
                status="blocker",
                is_blocker=True,
                task_date=timezone.localdate(),
            )

        return Response(
            {"message": "✅ Daily Standup submitted successfully!"},
            status=status.HTTP_201_CREATED
        )



@login_required
def change_role(request, user_id, new_role):
    user = get_object_or_404(User, id=user_id)
    user.role = new_role
    user.save()
    messages.success(request, f"{user.username}'s role changed to {new_role} successfully!")
    return redirect('approval_list')  # redirect where you want
@login_required
@require_POST
def api_change_role(request,user_id):
    user = get_object_or_404 (User,id=user_id)
    new_role = request.POST.get('newrole')

    if not new_role:
        return JsonResponse({'message': '❌ Role not provided.'},status = 400)
    user.role = new_role
    user.save()
    return JsonResponse({
        'message': f"✅ {user.username}'s role has been changed to '{new_role}'."
    })




@login_required(login_url='login_view')
def weekly_report(request):
    # ✅ Allow only lead, CEO, or management
    if request.user.role not in ['lead', 'ceo', 'management']:
        messages.warning(request, "You are not authorized to view this page.")
        return redirect('employee_dashboard')

    today = timezone.now().date()
    start_date = today - timedelta(days=7)

    # ✅ Get only tasks updated within last 7 days
    tasks = DailyUpdates.objects.filter(
        task_date__range=[start_date, today]
    ).select_related('user', 'project').order_by('user__username', '-task_date')

    # ✅ Group tasks by employee
    employee_data = {}
    for t in tasks:
        if t.user not in employee_data:
            employee_data[t.user] = []
        employee_data[t.user].append(t)

    context = {
        'employee_data': employee_data,
        'start_date': start_date,
        'end_date': today,
    }
    return render(request, 'report.html', context)



from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import DailyUpdates


@login_required(login_url='login_view')
def download_weekly_report_pdf(request):
    """Compact weekly report showing missing days (no updates)"""
    today = timezone.now().date()
    start_date = today - timedelta(days=6)  # 7-day range

    tasks = DailyUpdates.objects.filter(
        task_date__range=[start_date, today]
    ).select_related('user', 'project').order_by('user__username', 'task_date')

    # Group by employee
    employee_data = {}
    for t in tasks:
        employee_data.setdefault(t.user, []).append(t)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="weekly_report.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=25,
        leftMargin=25,
        topMargin=30,
        bottomMargin=25
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    title = styles["Heading1"]
    subtitle = styles["Heading3"]

    elements = []
    elements.append(Paragraph(f"Weekly Report ({start_date} → {today})", title))
    elements.append(Spacer(1, 8))

    # For each employee
    for employee, entries in employee_data.items():
        elements.append(Paragraph(
            f"<b>Employee:</b> {employee.get_full_name() or employee.username}",
            subtitle
        ))
        elements.append(Spacer(1, 4))

        # Group by date
        grouped_by_date = {}
        for t in entries:
            grouped_by_date.setdefault(t.task_date, []).append(t)

        # Loop through every date in range (even missing)
        current_date = start_date
        while current_date <= today:
            elements.append(Paragraph(f"<b>Date:</b> {current_date}", styles["Heading5"]))
            date_tasks = grouped_by_date.get(current_date, [])
            table_data = [["Category", "Project", "Task Description", "Status", "Time Taken"]]

            if date_tasks:
                categories = {
                    "What You Did Yesterday": [x for x in date_tasks if x.is_yesterday],
                    "What You Will Do Today": [x for x in date_tasks if x.is_today],
                    "Blocker": [x for x in date_tasks if x.is_blocker],
                }

                for category, cat_tasks in categories.items():
                    if cat_tasks:
                        first = True
                        for t in cat_tasks:
                            table_data.append([
                                category if first else "",
                                t.project.name if t.project else "-",
                                Paragraph(t.task_description or "-", normal),
                                t.status or "-",
                                str(t.time_taken or "-")
                            ])
                            first = False
                    elif category == "Blocker":
                        table_data.append([category, "-", "No blockers", "-", "-"])
            else:
                # 🚫 Show missing update day
                table_data.append(["-", "-", "No updates submitted on this day.", "-", "-"])

            # Compact table layout
            table = Table(
                table_data,
                repeatRows=1,
                colWidths=[1.3 * inch, 1.3 * inch, 2.8 * inch, 0.9 * inch, 0.8 * inch]
            )
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#007bff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("FONTSIZE", (0, 1), (-1, -1), 8.5),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 5))
            current_date += timedelta(days=1)

        # Add subtle separator, no page break
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("<hr/>", normal))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    return response















