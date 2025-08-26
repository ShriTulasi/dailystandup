from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib import messages
from rest_framework import permissions
# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterForm,ProjectForm,profileform,ProjectAssignmentForm,ApproveUserForm,EmpProfileForm,DailyTaskForm,MeetingForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,ProjectSerializer,RejectUserSerializer,ApproveUserSerializer,EmpProfileSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User,Profile,EmpProfile,DailyUpdates
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, get_user_model

from .serializers import LoginSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ProjectAssignment
from .serializers import ProjectAssignmentSerializer

from django.utils import timezone


# def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login_view')  # Redirect to your login page
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.is_active = False
            user.save()
            messages.success(request, "Registration successful! Wait for lead approval.")

            # login(request, user)   # optional: log in after registration
            return redirect("login_view")  # redirect wherever you want
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})





# def login_view(request):
#     error = None
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             error = "You need to register first."
#             return render(request, 'login.html', {'error': error})

#         user = authenticate(request, username=user.username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('tech_dashboard')  # replace with your home page/dashboard
#         else:
#             error = "Invalid email or password."
#     return render(request, 'login.html', {'error': error})

# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
# from .models import User

# def login_view(request):
#     error = None
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             error = "You need to register first."
#             return render(request, 'login.html', {'error': error})

#         user = authenticate(request, username=user.username, password=password)
#         if user is not None:
#             login(request, user)

#             # Role-based redirect
#             if user.role == "lead":
#                 return redirect('tech_dashboard')
#             elif user.role == "employee":
#                 return redirect('employee_dashboard')
#             else:
#                 # fallback
#                 return redirect('login')
#         else:
#             error = "Invalid email or password."

#     return render(request, 'login.html', {'error': error})


# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             if not user.is_approved:
#                 messages.error(request, "Your account is not approved yet.")
#                 return redirect("login_view")
#             login(request, user)
#             # Redirect based on role
#             if user.role == 'lead':
#                 return redirect('tech_dashboard')
#             elif user.role == 'employee':
#                 return redirect('employee_dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, "login.html", {"form": form})



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User

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

        # Check password
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            # Check if approved
            if not user.is_approved:
                error = "Your account is not approved yet. Please wait for lead approval."
                return render(request, 'login.html', {'error': error})

            login(request, user)

            # Role-based redirect
            if user.role == "lead":
                return redirect('tech_dashboard')
            elif user.role == "employee":
                return redirect('employee_dashboard')
            else:
                return redirect('login')
        else:
            error = "Invalid email or password."

    return render(request, 'login.html', {'error': error})




class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@login_required(login_url='login_view')
def approval_list(request):
    if request.user.role != 'lead':
        return redirect('login_view')
    
    # Pending users (need approval)
    pending_users = User.objects.filter(is_pending=True)
    
    # Approved users (already approved)
    approved_users = User.objects.filter(is_approved=True, is_pending=False)
    
    return render(request, 'approve.html', {
        'pending_users': pending_users,
        'approved_users': approved_users
    })



@login_required(login_url='login_view')
def approve_user(request, user_id):
    if request.user.role != 'lead':
        return redirect('login_view')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ApproveUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = True
            user.is_pending = False  # remove from pending list
            user.is_active = True

            # user.is_active = user.is_approved  
            user.save()
            return redirect('approval_list')
    else:
        form = ApproveUserForm(instance=user)
    return render(request, 'approve_user.html', {'form': form, 'user': user})


@login_required(login_url='login_view')
def reject_user(request, user_id):
    if request.user.role != 'lead':
        return redirect('login_view')
    
    user = get_object_or_404(User, id=user_id)
    user.is_pending = False   # remove from pending list
    user.is_approved = False
    user.is_active = False
    user.save()
    
    return redirect('approval_list')







from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer

User = get_user_model()

# class LoginAPI(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']

#             # Get user by email
#             try:
#                 user_obj = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 return Response({"error": "You need to register first."}, status=status.HTTP_400_BAD_REQUEST)

#             # Authenticate using username
#             user = authenticate(username=user_obj.username, password=password)
#             if user:
#                 token, created = Token.objects.get_or_create(user=user)
#                 # ✅ Remove login() to avoid CSRF
#                 return Response({"message": "Login successful.", "token": token.key})
#             else:
#                 return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    if request.user.role != "lead":
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




@login_required(login_url='login') 
def tech_dashboard(request):
    
    if request.user.role != "lead":
        return redirect('login_view')
    now_date = timezone.localdate()
    now_time = timezone.localtime().time()

    # Lead can see meetings they host or participate in
    meetings = request.user.hosted_meetings.filter(
        Q(meeting_date__gt=now_date) |
        Q(meeting_date=now_date, meeting_time__gte=now_time)
    ).order_by('meeting_date', 'meeting_time')

    return render(request, "leaddashboard.html", {
        "meetings": meetings,
    })
    # return render(request, "leaddashboard.html")

# @login_required(login_url='login') 
# def employee_dashboard(request):
#     if request.user.role != "employee":
#         return redirect('login_view')
#     return render(request,'employeedashboard.html')

# from django.utils import timezone
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect

# @login_required(login_url='login') 
# def employee_dashboard(request):
#     if request.user.role != "employee":
#         return redirect('login_view')
    
#     now_date = timezone.localdate()
#     now_time = timezone.localtime().time()

#     # Future meetings
#     meetings_future = request.user.meetings.filter(meeting_date__gt=now_date)

#     # Today’s meetings not finished yet
#     meetings_today = request.user.meetings.filter(meeting_date=now_date, meeting_time__gte=now_time)

#     # Combine querysets and order
#     meetings = (meetings_future | meetings_today).order_by('meeting_date', 'meeting_time')

#     return render(request, 'employeedashboard.html', {'meetings': meetings})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q

@login_required(login_url='login') 
def employee_dashboard(request):
    if request.user.role != "employee":
        return redirect('login_view')
    
    now_date = timezone.localdate()
    now_time = timezone.localtime().time()

    # Only upcoming meetings (today not yet started + future)
    meetings = request.user.meetings.filter(
        Q(meeting_date__gt=now_date) |
        Q(meeting_date=now_date, meeting_time__gte=now_time)
    ).order_by('meeting_date', 'meeting_time')

    return render(request, 'employeedashboard.html', {'meetings': meetings})





class ProjectCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Only Tech Lead can create
        if request.user.role != "lead":
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
        # Only Tech Lead can add project
        if request.user.role != "lead":
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
    









@login_required
def add_profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = profileform(request.POST, instance=profile_obj, user=request.user)
        if form.is_valid():
            # Update User fields
            # request.user.first_name = form.cleaned_data['first_name']
            # request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.username = form.cleaned_data['username']
            request.user.save()

            form.save()
            return redirect('tech_dashboard')
    else:
        form = profileform(instance=profile_obj, user=request.user)

    return render(request, 'addprofile.html', {'form': form})




# views.py
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login_view')  # redirect to login page








def assign_project(request):
    if request.method == "POST":
        form = ProjectAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)  # Save object without M2M yet
            assignment.save()                     # Save to get ID
            form.save_m2m()                       # Save employees
            return redirect('tech_dashboard')     # or any success page
    else:
        form = ProjectAssignmentForm()
    return render(request, 'assignproject.html', {'form': form})






# List all assignments or create a new one
class ProjectAssignmentAPIView(generics.ListCreateAPIView):
    queryset = ProjectAssignment.objects.all()
    serializer_class = ProjectAssignmentSerializer
    permission_classes = [IsAuthenticated]  # optional








# class ApproveUserAPI(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, user_id):
#         if request.user.role != "lead":
#             return Response({"error": "Only leads can approve users."}, status=status.HTTP_403_FORBIDDEN)

#         try:
#             user = User.objects.get(id=user_id, is_approved=False)
#         except User.DoesNotExist:
#             return Response({"error": "User not found or already processed."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = ApproveUserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": f"User {user.username} approved as {serializer.validated_data['role']}."})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.contrib.auth import get_user_model
# from .serializers import ApproveUserSerializer

# User = get_user_model()

# class ApproveUserAPI(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         """✅ List all users waiting for approval"""
#         if request.user.role != "lead":
#             return Response({"error": "Only leads can view pending users."}, status=status.HTTP_403_FORBIDDEN)

#         pending_users = User.objects.filter(is_approved=False)
#         serializer = ApproveUserSerializer(pending_users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, user_id=None):
#         """✅ Approve or Reject a user"""
#         if request.user.role != "lead":
#             return Response({"error": "Only leads can approve/reject users."}, status=status.HTTP_403_FORBIDDEN)

#         if not user_id:
#             return Response({"error": "User ID is required in the URL."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(id=user_id, is_approved=False)
#         except User.DoesNotExist:
#             return Response({"error": "User not found or already processed."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = ApproveUserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()

#             role = serializer.validated_data.get("role", "No role assigned")
#             approved = serializer.validated_data.get("is_approved")

#             if approved:
#                 return Response({
#                     "message": f"✅ User '{user.username}' approved as {role}."
#                 })
#             else:
#                 return Response({
#                     "message": f"❌ User '{user.username}' rejected."
#                 })

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    






# class RejectUserAPI(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, user_id):
#         if request.user.role != "lead":
#             return Response({"error": "Only leads can reject users."}, status=status.HTTP_403_FORBIDDEN)

#         try:
#             user = User.objects.get(id=user_id, is_approved=False)
#         except User.DoesNotExist:
#             return Response({"error": "User not found or already processed."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = RejectUserSerializer(user, data={}, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": f"User {user.username} rejected."})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# def add_emp_profile(request):
#     # Check if profile already exists
#     profile_instance = EmpProfile.objects.filter(users=request.user).first()

#     if request.method == "POST":
#         form = EmpProfileForm(request.POST, request.FILES, instance=profile_instance, user=request.user)
#         if form.is_valid():
#             profile = form.save(commit=False)

#             # Update User fields if edited
#             request.user.username = form.cleaned_data['username']
#             request.user.email = form.cleaned_data['email']
#             request.user.save()

#             profile.users = request.user
#             profile.save()
#             return redirect('dashboard')  # Redirect to dashboard
#     else:
#         form = EmpProfileForm(instance=profile_instance, user=request.user)

#     return render(request, 'empprofile.html', {'form': form})


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class ApproveUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
#         """✅ List all users waiting for approval"""
        if request.user.role != "lead":
            return Response({"error": "Only leads can view pending users."}, status=status.HTTP_403_FORBIDDEN)

        pending_users = User.objects.filter(is_approved=False)
        serializer = ApproveUserSerializer(pending_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        """
        Approve a user via API.
        Expect JSON body:
        {
            "role": "employee"  # optional, if approving
        }
        """
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

        return Response({
            "message": f"✅ User '{user.username}' approved as {user.role}."
        }, status=status.HTTP_200_OK)


class RejectUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """
        Reject a user via API.
        """
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
    # Check if profile already exists
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
            profile.user = request.user   # link profile to user
            profile.save()

            # Update User model fields
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            return redirect("employee_dashboard")  # redirect anywhere you like
    else:
        form = EmpProfileForm(instance=profile_instance, user=request.user)

    return render(request, "addprofile.html", {"form": form})




# class EmpProfileView(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
#     serializer_class = EmpProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         # Get logged-in user's profile, or None if not exists
#         return EmpProfile.objects.filter(user=self.request.user).first()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)





# class EmpProfileView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
#     serializer_class = EmpProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         # Always return the logged-in user's profile
#         profile, created = EmpProfile.objects.get_or_create(user=self.request.user)
#         return profile

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)




class EmpProfileView(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    serializer_class = EmpProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Fetch the logged-in user's profile, or return None if not exists
        profile = EmpProfile.objects.filter(user=self.request.user).first()
        return profile

    def perform_create(self, serializer):
        # Link the profile to logged-in user
        serializer.save(user=self.request.user)




# @login_required(login_url='login')
# def submit_daily_task(request):
#     if request.method == 'POST':
#         form = DailyTaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.user = request.user
#             task.save()
#             return redirect('employee_dashboard')
#     else:
#         form = DailyTaskForm()
#     return render(request, 'dailystandup.html', {'form': form})



# @login_required(login_url='login')
# def submit_daily_task(request):
#     if request.method == 'POST':
#         form = DailyTaskForm(request.POST)
#         if form.is_valid():
#             project = form.cleaned_data['project']
#             tasks = request.POST.getlist('tasks[]')  # get all rows (tasks)

#             # save as bullet points in one field
#             description = "\n".join(f"• {t}" for t in tasks if t.strip())

#             DailyUpdates.objects.create(
#                 user=request.user,
#                 project=project,
#                 task_description=description  # stored neatly as bullet points
#                 # task_date auto set by model default
#             )
#             return redirect('employee_dashboard')
#     else:
#         form = DailyTaskForm()
#     return render(request, 'dailystandup.html', {'form': form})




# @login_required(login_url='login')
# def submit_daily_task(request):
#     if request.method == 'POST':
#         projects = request.POST.getlist('project')  # multiple projects

#         for idx, project_id in enumerate(projects, start=1):
#             # ⬇️ Now fetch tasks with the correct field name
#             tasks = request.POST.getlist(f'tasks_project_{idx}[]')
#             description = "\n".join(f"• {t}" for t in tasks if t.strip())

#             if description:  # only save if not empty
#                 DailyUpdates.objects.create(
#                     user=request.user,
#                     project_id=project_id,
#                     task_description=description
#                 )

#         return redirect('employee_dashboard')

#     else:
#         form = DailyTaskForm()

#     return render(request, 'dailystandup.html', {'form': form})




# @login_required(login_url='login')
# def submit_daily_task(request):
#     if request.method == 'POST':
#         idx = 1
#         while f'project_{idx}' in request.POST:
#             project_id = request.POST.get(f'project_{idx}')
#             tasks = request.POST.getlist(f'tasks_project_{idx}[]')
            
#             # Combine all tasks for this project
#             description = "\n".join(f"• {t.strip()}" for t in tasks if t.strip())
            
#             if description:  # only save if not empty
#                 DailyUpdates.objects.create(
#                     user=request.user,
#                     project_id=project_id,
#                     task_description=description
#                 )
            
#             idx += 1

#         return redirect('employee_dashboard')

#     else:
#         form = DailyTaskForm()

#     return render(request, 'dailystandup.html', {'form': form})



# @login_required(login_url='login')
# def submit_daily_task(request):
#     if request.method == 'POST':
#         idx = 1
#         while f'project_{idx}' in request.POST:
#             project_id = request.POST.get(f'project_{idx}')
#             tasks = request.POST.getlist(f'tasks_project_{idx}')  # get all tasks for this project

#             # Save each task separately
#             for task in tasks:
#                 task = task.strip()
#                 if task:  # only save if not empty
#                     DailyUpdates.objects.create(
#                         user=request.user,
#                         project_id=project_id,
#                         task_description=task
#                     )

#             idx += 1

#         return redirect('employee_dashboard')
#     else:
#         form = DailyTaskForm()

#     return render(request, 'dailystandup.html', {'form': form})



# @login_required(login_url='login')
# def submit_daily_task(request):
#     if request.method == 'POST':
#         idx = 1
#         while f'project_{idx}' in request.POST:
#             project_id = request.POST.get(f'project_{idx}')
#             tasks = request.POST.getlist(f'tasks_project_{idx}')  # <-- fixed

#             # Save each task separately
#             for task in tasks:
#                 task = task.strip()
#                 if task:  # only save if not empty
#                     DailyUpdates.objects.create(
#                         user=request.user,
#                         project_id=project_id,
#                         task_description=task
#                     )

#             idx += 1

#         return redirect('employee_dashboard')
#     else:
#         form = DailyTaskForm()

#     return render(request, 'dailystandup.html', {'form': form})






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DailyTaskForm
from .models import DailyUpdates

# @login_required(login_url='login')
# def submit_daily_task(request):
#     if request.method == 'POST':
#         project_count = 1
#         while f'project_{project_count}' in request.POST:
#             project_id = request.POST.get(f'project_{project_count}')
#             tasks = request.POST.getlist(f'tasks_project_{project_count}[]')
#             print(f"Project {project_id} tasks:", tasks)  # all tasks for this project

#             for task in tasks:
#                 task = task.strip()
#                 if task:  # only save non-empty tasks
#                     DailyUpdates.objects.create(
#                         user=request.user,
#                         project_id=project_id,
#                         task_description=task
#                     )

#             project_count += 1

#         return redirect('employee_dashboard')

#     else:
#         form = DailyTaskForm()

#     return render(request, 'dailystandup.html', {'form': form})




# @login_required(login_url='login')
# def submit_daily_task(request):
#     if request.method == 'POST':
#         project_count = 1
#         while f'project_{project_count}' in request.POST:
#             project_id = request.POST.get(f'project_{project_count}')

#             # get all task rows for this project
#             tasks = request.POST.getlist(f'tasks_project_{project_count}[]')
#             times = request.POST.getlist(f'time_taken_{project_count}[]')
#             statuses = request.POST.getlist(f'status_{project_count}[]')
#             dates = request.POST.getlist(f'task_date_{project_count}[]')

#             print(f"Project {project_id} tasks:", tasks)

#             for i, task in enumerate(tasks):
#                 task = task.strip()
#                 if task:
#                     DailyUpdates.objects.create(
#                         user=request.user,
#                         project_id=project_id,
#                         task_description=task,
#                         time_taken=times[i] if i < len(times) else None,
#                         status=statuses[i] if i < len(statuses) else 'pending',
#                         task_date=dates[i] if i < len(dates) else timezone.localdate()
#                     )

#             project_count += 1

#         return redirect('employee_dashboard')

#     else:
#         form = DailyTaskForm()
#         today = timezone.localdate()
#         return render(request, 'dailystandup.html', {'form': form, 'today': today})





# from django.utils import timezone

# @login_required(login_url='login')
# def submit_daily_task(request):
#     if request.method == 'POST':
#         project_count = 1
#         while f'project_{project_count}' in request.POST:
#             project_id = request.POST.get(f'project_{project_count}')

#             tasks = request.POST.getlist(f'tasks_project_{project_count}[]')
#             times = request.POST.getlist(f'time_taken_{project_count}[]')
#             statuses = request.POST.getlist(f'status_{project_count}[]')
#             dates = request.POST.getlist(f'task_date_{project_count}[]')

#             for i, task in enumerate(tasks):
#                 task = task.strip()
#                 if task:
#                     DailyUpdates.objects.create(
#                         user=request.user,
#                         project_id=project_id,
#                         task_description=task,
#                         time_taken=times[i] if i < len(times) else None,
#                         status=statuses[i] if i < len(statuses) else 'pending',
#                         task_date=dates[i] if i < len(dates) else timezone.localdate()
#                     )

#             project_count += 1

#         return redirect('employee_dashboard')

#     else:
#         form = DailyTaskForm()
#         today = timezone.localdate()  # ← add this
#         return render(request, 'dailystandup.html', {'form': form, 'today': today})  # ← pass today




from django.utils import timezone

@login_required(login_url='login')
def submit_daily_task(request):
    if request.method == 'POST':
        project_count = 1
        while f'project_{project_count}' in request.POST:
            project_id = request.POST.get(f'project_{project_count}')

            tasks = request.POST.getlist(f'tasks_project_{project_count}[]')
            times = request.POST.getlist(f'time_taken_{project_count}[]')
            statuses = request.POST.getlist(f'status_{project_count}[]')
            dates = request.POST.getlist(f'task_date_{project_count}[]')

            for i, task in enumerate(tasks):
                task = task.strip()
                if task:
                    # Convert time_taken string to timedelta
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
                        task_date=dates[i] if i < len(dates) else timezone.localdate()
                    )

            project_count += 1

        return redirect('employee_dashboard')

    else:
        form = DailyTaskForm()
        today = timezone.localdate()  # ← send today's date to template
        return render(request, 'dailystandup.html', {'form': form, 'today': today})




# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import DailyUpdates

# @login_required(login_url='login')
# def team_lead_task_view(request):
#     # Get all tasks submitted by employees
#     tasks = DailyUpdates.objects.select_related('user', 'project').order_by('-task_date')

#     return render(request, 'lead_taskupdates.html', {'tasks': tasks})




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import DailyUpdates

@login_required(login_url='login')
def team_lead_task_view(request):
    tasks = DailyUpdates.objects.select_related('user', 'project').order_by('-task_date')

    # convert time_taken to human-readable string
    for task in tasks:
        if task.time_taken:
            total_seconds = task.time_taken.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            task.time_taken_str = f"{hours}h {minutes}m"
        else:
            task.time_taken_str = "-"

    return render(request, 'lead_taskupdates.html', {'tasks': tasks})



@login_required(login_url='login')
def employee_task_history(request):
    tasks = DailyUpdates.objects.filter(user=request.user).order_by('-task_date')
    
    # convert time_taken to string for display
    for task in tasks:
        if task.time_taken:
            total_seconds = task.time_taken.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            task.time_taken_str = f"{hours}h {minutes}m"
        else:
            task.time_taken_str = "-"

    return render(request, 'emptaskhistory.html', {'tasks': tasks})












# @login_required
# def schedule_meeting(request):
#     if request.method == 'POST':
#         form = MeetingForm(request.POST)
#         if form.is_valid():
#             meeting = form.save(commit=False)
#             meeting.host = request.user
#             meeting.save()
#             form.save_m2m()  # save participants
#             # Optional: send notification here
#             return redirect('lead_dashboard')
#     else:
#         form = MeetingForm()
#     return render(request, 'meeting.html', {'form': form})




from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Meeting

# User = get_user_model()

# @login_required
# def schedule_meeting(request):
#     # Fetch only employees
#     employees = User.objects.filter(role='employee')
#     today = timezone.localdate()

#     if request.method == "POST":
#         participant_ids = request.POST.getlist('participants')  # list of selected employees
#         about = request.POST['about']
#         link = request.POST['link']
#         meeting_date = request.POST['meeting_date']
#         meeting_time = request.POST['meeting_time']

#         meeting = Meeting.objects.create(
#             lead=request.user,
#             about=about,
#             meeting_date=meeting_date,
#             meeting_time=meeting_time,
#             link=link
#         )
#         meeting.participants.set(participant_ids)
#         return redirect('team_lead_task_view')

#     return render(request, 'meeting.html', {'employees': employees, 'today': today})




# @login_required(login_url='login')
# def schedule_meeting(request):
#     if request.method == 'POST':
#         form = MeetingForm(request.POST)
#         if form.is_valid():
#             meeting = form.save(commit=False)
#             meeting.host = request.user  # the lead
#             meeting.save()
#             form.save_m2m()  # save participants
#             return redirect('meeting_list')  # or any page you want
#     else:
#         form = MeetingForm()
#     return render(request, 'meeting.html', {'form': form})





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import MeetingForm

@login_required(login_url='login')
def schedule_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.host = request.user  # the lead
            meeting.save()
            form.save_m2m()  # save participants
            return redirect('tech_dashboard')  # or any page you want
    else:
        form = MeetingForm()
    return render(request, 'meeting.html', {
        'form': form,
        'today': timezone.localdate()  # optional, for default date in template
    })





# @login_required(login_url='login')
# def lead_meetings_list(request):
#     if request.user.role != "":
#         return redirect('login_view')

#     # Get only meetings created by this lead
#     meetings = Meeting.objects.filter(host=request.user).order_by('-date', '-time')
#     return render(request, 'list.html', {'meetings': meetings})





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

    meeting.is_canceled = True
    meeting.cancel_reason = reason
    meeting.save()

    messages.success(request, "Meeting canceled successfully.")
    return redirect("tech_dashboard")




# views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.utils import timezone
# from datetime import timedelta
# from .models import DailyUpdates
# from .serializers import DailyUpdatesSerializer

# class SubmitDailyTaskAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         project_count = 1

#         # Loop through projects dynamically
#         while f'project_{project_count}' in request.data:
#             project_id = request.data.get(f'project_{project_count}')

#             tasks = request.data.getlist(f'tasks_project_{project_count}[]')
#             times = request.data.getlist(f'time_taken_{project_count}[]')
#             statuses = request.data.getlist(f'status_{project_count}[]')
#             dates = request.data.getlist(f'task_date_{project_count}[]')

#             for i, task in enumerate(tasks):
#                 task = task.strip()
#                 if task:
#                     # Convert time_taken string "HH:MM" to timedelta
#                     time_taken = None
#                     if i < len(times) and times[i]:
#                         h, m = map(int, times[i].split(':'))
#                         time_taken = timedelta(hours=h, minutes=m)

#                     # Create the DailyUpdates object
#                     DailyUpdates.objects.create(
#                         user=user,
#                         project_id=project_id,
#                         task_description=task,
#                         time_taken=time_taken,
#                         status=statuses[i] if i < len(statuses) else 'pending',
#                         task_date=dates[i] if i < len(dates) else timezone.localdate()
#                     )

#             project_count += 1

#         return Response({'detail': 'Daily tasks submitted successfully.'}, status=status.HTTP_201_CREATED)







# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from datetime import timedelta
from .models import DailyUpdates

class SubmitDailyTaskAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        project_count = 1

        # Loop through projects dynamically
        while f'project_{project_count}' in request.data:
            project_id = request.data.get(f'project_{project_count}')

            # Get lists from JSON
            tasks = request.data.get(f'tasks_project{project_count}', [])
            times = request.data.get(f'time_taken{project_count}', [])
            statuses = request.data.get(f'status{project_count}', [])
            dates = request.data.get(f'task_date{project_count}', [])

            # Make sure each is a list
            if not isinstance(tasks, list):
                tasks = [tasks]
            if not isinstance(times, list):
                times = [times]
            if not isinstance(statuses, list):
                statuses = [statuses]
            if not isinstance(dates, list):
                dates = [dates]

            for i, task in enumerate(tasks):
                task = task.strip()
                if task:
                    # Convert time_taken string "HH:MM" to timedelta
                    time_taken = None
                    if i < len(times) and times[i]:
                        h, m = map(int, times[i].split(':'))
                        time_taken = timedelta(hours=h, minutes=m)

                    DailyUpdates.objects.create(
                        user=user,
                        project_id=project_id,
                        task_description=task,
                        time_taken=time_taken,
                        status=statuses[i] if i < len(statuses) else 'pending',
                        task_date=dates[i] if i < len(dates) else timezone.localdate()
                    )

            project_count += 1

        return Response({'detail': 'Daily tasks submitted successfully.'}, status=status.HTTP_201_CREATED)
