from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Project,EmployeeProject,Profile,ProjectAssignment,EmpProfile,DailyUpdates,Meeting

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False   # cannot login until approved
        user.is_pending = True   # show in lead dashboard
        if commit:
            user.save()
        return user


class ApproveUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role'] 


    



# class ProjectForm(forms.ModelForm):
#     class Meta:
#         model = Project
#         fields = ['name', 'description']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter project name"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter project description"
            }),
        }


class AssignEmployeeForm(forms.Form):
    class Meta:
        model = EmployeeProject
        fields = ['project', 'employee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['employee'].queryset = User.objects.filter(role='employee')



# class profileform(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['phone', 'field', 'designation']
#         widgets = {
#             'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone'}),
#             'field': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter field'}),
#             'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation'}),
            
#         }




class profileform(forms.ModelForm):
    username = forms.CharField(
        max_length=30, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['username', 'email', 'phone', 'field', 'designation']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone'}),
            'field': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter field'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # self.fields['first_name'].initial = user.first_name
            # self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username




# class ProjectAssignmentForm(forms.ModelForm):
#     class Meta:
#         model = ProjectAssignment
#         fields = ['project', 'employees']

#     project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label="Select Project")
#     employees = forms.ModelMultipleChoiceField(
#         queryset=EmployeeProject.objects.all(),
#         widget=forms.CheckboxSelectMultiple  # or use SelectMultiple for dropdown
#     )


from django import forms
from .models import ProjectAssignment, Project, User  # Employee = your employee model

class ProjectAssignmentForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        empty_label="Select Project",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    employee = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # all registered employees
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = ProjectAssignment
        fields = ['project', 'employee']








from django import forms
from .models import EmpProfile

class EmpProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = EmpProfile
        fields = ['username','email','phone', 'address', 'profile', 'dob', 'designation']  # only EmpProfile fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True, user=None):
        """Save EmpProfile and update User fields"""
        emp_profile = super().save(commit=False)

        if user:  # update user model too
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()

        if commit:
            emp_profile.save()
        return emp_profile





# class DailyTaskForm(forms.ModelForm):
#     class Meta:
#         model = DailyUpdates
#         fields = ['project', 'task_description']  # task_date is automatic
#         widgets = {
#             'task_description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your task'}),
#         }




class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = DailyUpdates
        fields = ['project']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            # 'task_description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:120px;'}),
        }





# class MeetingForm(forms.ModelForm):
#     class Meta:
#         model = Meeting
#         fields = ['participants', 'about', 'meeting_time', 'meeting_date', 'link']
#         widgets = {
#             'participants': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
#             'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'meeting_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'meeting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'link': forms.URLInput(attrs={'class': 'form-control'}),
#         }





# from django import forms
# from .models import Meeting
# from django.contrib.auth.models import User

# class MeetingForm(forms.ModelForm):
#     class Meta:
#         model = Meeting
#         fields = ['participants', 'about', 'meeting_time', 'meeting_date', 'link']
#         widgets = {
#             'participants': forms.CheckboxSelectMultiple(),
#             'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'meeting_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'meeting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'link': forms.URLInput(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(MeetingForm, self).__init__(*args, **kwargs)
#         # Filter only employees (assuming 'employee' is a role in your User model)
#         self.fields['participants'].queryset = User.objects.filter(role='employee')



from django import forms
from .models import Meeting
from django.contrib.auth import get_user_model

User = get_user_model()  # this points to your custom standup.User

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['participants', 'about', 'meeting_time', 'meeting_date', 'link']
        widgets = {
            'participants': forms.CheckboxSelectMultiple(),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'meeting_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'meeting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        # Filter only employees (assuming 'employee' is a role in your User model)
        self.fields['participants'].queryset = User.objects.filter(role='employee')






