from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Project,EmployeeProject,Profile,ProjectAssignment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',  'role']






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

    employees = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # all registered employees
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = ProjectAssignment
        fields = ['project', 'employees']


    