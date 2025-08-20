from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterForm,ProjectForm,profileform,ProjectAssignmentForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,ProjectSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User,Profile
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, get_user_model

from .serializers import LoginSerializer



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
            user = form.save()
            # login(request, user)   # optional: log in after registration
            return redirect("login_view")  # redirect wherever you want
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

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tech_dashboard')  # replace with your home page/dashboard
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






# User = get_user_model()

# class LoginAPI(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']

#             # Check if user exists
#             try:
#                 user_obj = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 return Response({"error": "You need to register first."}, status=status.HTTP_400_BAD_REQUEST)

#             # Authenticate user
#             user = authenticate(username=user_obj.username, password=password)
#             if user:
#                 token, created = Token.objects.get_or_create(user=user)
                
#                 return Response({"message": "Login successful.","token" : token.key})
#             else:
#                 return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer

User = get_user_model()

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Get user by email
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "You need to register first."}, status=status.HTTP_400_BAD_REQUEST)

            # Authenticate using username
            user = authenticate(username=user_obj.username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                # ✅ Remove login() to avoid CSRF
                return Response({"message": "Login successful.", "token": token.key})
            else:
                return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# @login_required
# def add_project(request):
#     if request.user.role != "lead":
#         return redirect("home")  # only Tech Lead can add project

#     if request.method == "POST":
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.lead = request.user
#             project.save()
#             return redirect("project_list")
#     else:
#         form = ProjectForm()
#     return render(request, "add_project.html", {"form": form})

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
    return render(request, "leaddashboard.html")







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


# class ProjectCreateAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
       
#         if request.user.role != "lead":
#             return Response({"error": "Only Tech Lead can add project."}, status=status.HTTP_403_FORBIDDEN)
        
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(lead=request.user)  # assign lead automatically
#             return Response({"message": "Project created successfully", "project": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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
    



# def add_profile(request):
#     if request.method == 'POST':
#         form = profileform(request.data,instance=User)
#         if form.is_valid():
#             form.save()
#             return redirect("tech_dashboard")
#     else:
#         form = profileform(isinstance=User)
#         return render(request,"addprofile,html" ,{'form' : form}) 







# @login_required
# def add_profile(request):
#     # Get or create profile for the logged-in user
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         form = profileform(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('tech_dashboard')  # or any page you want to redirect
#     else:
#         form = profileform(instance=profile)  # prefill form with existing data

#     return render(request, "addprofile.html", {'form': form})





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
    return redirect('logout_view')  # redirect to login page





# def assign_project(request):
#     if request.method == 'POST':
#         form = ProjectAssignmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('tech_dashboard')  
#     else:
#         form = ProjectAssignmentForm()

#     return render(request, 'assignproject.html', {'form': form})

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




