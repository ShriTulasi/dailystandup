

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        
        ('lead', 'Tech Lead'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')


    def __str__(self):
        return f"{self.username} ({self.role})"




class Project(models.Model):
    name =  models.CharField(max_length=100,unique=True)
    description = models.TextField()
    lead = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leading_projects", limit_choices_to={'role': 'lead'})

    def __str__(self):
        return f"{self.name}"
    


class EmployeeProject(models.Model):
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'employee'}
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.username} -> {self.project.name}"
    



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    phone = models.CharField(max_length=15)
    field = models.CharField(max_length=16)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user}"
    

class ProjectAssignment(models.Model):
    project = models.ForeignKey(Project,on_delete= models.CASCADE)
    employee = models.ManyToManyField(User)
    assigned_at = models.DateTimeField(auto_now_add=True)




        






