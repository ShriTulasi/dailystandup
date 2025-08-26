

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        
        ('lead', 'Tech Lead'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True,null=True)
    is_approved = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)



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


# class EmpProfile(models.Model):
#     users = models.ForeignKey(User,on_delete=models.CASCADE,related_name="emp")
#     phone = models.CharField(max_length=15)
#     address = models.TextField()
#     profile = models.FileField()
#     dob = models.DateField(blank=True, null=True)
#     designation = models . CharField(max_length=100)



#     def __str__(self):
#         return self.user.username



        



class EmpProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emp")
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile = models.FileField()
    dob = models.DateField(blank=True, null=True)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username



class DailyUpdates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_description = models.TextField()
    task_date = models.DateField(default=timezone.localdate)
    time_taken = models.DurationField(null=True,blank=True)
    status = models.CharField(
    max_length=20,
    choices=[('completed','Completed'),('pending','Pending')],
    default='pending'
    )



    def __str__(self):
        return f"{self.user.username}-{self.project.name}"





# class Meeting(models.Model):
#     contact = models.ForeignKey(User,on_delete=models.CASCADE)
#     about = models.TextField()
#     meeting_time = models.DurationField(null=True,blank=True)
#     meeting_date = models.DateField(default=timezone.localdate)
#     link = models.CharField()


#     def __str__(self):
#         return f"{self.meeting_date}"
    


# class Meeting(models.Model):
#     host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_meetings')  # the lead
#     participants = models.ManyToManyField(User, related_name='meetings')  # employees invited
#     about = models.TextField()
#     meeting_time = models.DurationField(null=True, blank=True)
#     meeting_date = models.DateField(default=timezone.localdate)
#     link = models.URLField(max_length=500, blank=True)

#     def __str__(self):
#         return f"{self.host.username} - {self.meeting_date}"




from django.db import models
from django.conf import settings
from django.utils import timezone

class Meeting(models.Model):
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # use this instead of User
        on_delete=models.CASCADE,
        related_name='hosted_meetings'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # use this instead of User
        related_name='meetings'
    )
    about = models.TextField()
    meeting_time = models.TimeField(null=True, blank=True)
    meeting_date = models.DateField(default=timezone.localdate)
    link = models.URLField(max_length=500, blank=True)
    is_cancel = models.BooleanField(default=False)
    reason =  models .TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.host.username} - {self.meeting_date}"




