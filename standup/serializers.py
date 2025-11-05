from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Project,ProjectAssignment,Meeting,FCMToken
from .models import EmpProfile
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework import serializers
from .models import DailyUpdates

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .models import EmpProfile
from rest_framework import serializers
from .models import FCMToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # User fields
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    # Extra profile fields
    phone = serializers.CharField(max_length=15, required=True)
    address = serializers.CharField(required=True)
    dob = serializers.DateField(required=False)
    designation = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'phone', 'address', 'dob', 'designation']

    def create(self, validated_data):
        
        profile_data = {
            'phone': validated_data.pop('phone'),
            'address': validated_data.pop('address'),
            'dob': validated_data.pop('dob', None),
            'designation': validated_data.pop('designation'),
        }

        # Create user
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_pending'] = True
        validated_data['is_approved'] = False
        validated_data['is_active'] = False
        user = User.objects.create(**validated_data)

        # Create profile
        EmpProfile.objects.create(user=user, **profile_data)

        return user



User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "You need to register first."})

        # Authenticate user with username (since Django default login uses username)
        user = authenticate(username=user.username, password=password)

        if not user:
            raise serializers.ValidationError({"password": "Invalid email or password."})

        # Check approval
        if not user.is_approved:
            raise serializers.ValidationError({"detail": "Your account is not approved yet. Please wait for lead approval."})

        attrs["user"] = user
        return attrs


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description','id']  # no  'lead'
        read_only_fields = ['lead']  # lead will be set from request.user



class ProjectAssignmentSerializer(serializers.ModelSerializer):
    # Read-only fields for GET
    project = serializers.StringRelatedField(read_only=True)
    employee = serializers.StringRelatedField(many=True, read_only=True)

    # Write-only fields for POST
    project_name = serializers.CharField(write_only=True)
    employee_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )




class ProjectAssignmentSerializer(serializers.ModelSerializer):
    # Read-only fields for GET
    project = serializers.StringRelatedField(read_only=True)
    employee = serializers.StringRelatedField(many=True, read_only=True)

    # Write-only fields for POST
    project_name = serializers.CharField(write_only=True)
    employee_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    class Meta: 
        model = ProjectAssignment
        fields = ['project', 'employee', 'project_name', 'employee_names']

    def create(self, validated_data):
        project_name = validated_data.pop('project_name')
        project = Project.objects.get(name=project_name)

        employee_names = validated_data.pop('employee_names')
        employees = User.objects.filter(username__in=employee_names)

        assignment = ProjectAssignment.objects.create(project=project)
        assignment.employee.set(employees)
        return assignment



User = get_user_model()

class ApproveUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[("employee", "Employee"), ("lead", "Lead")])

    class Meta:
        model = User
        fields = ["id", "role", "is_approved", "is_active","username","email"]
        read_only_fields = ["id","username","email"]

    def update(self, instance, validated_data):
        instance.role = validated_data.get("role", instance.role)
        instance.is_approved = validated_data.get("is_approved",instance.is_approved)
        instance.is_active = instance.is_approved
        instance.save()
        return instance


class RejectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "is_approved", "is_active"]
        read_only_fields = ["id", "is_approved", "is_active"]

    def update(self, instance, validated_data):
        instance.is_approved = False
        instance.is_active = False
        instance.save()
        return instance




class RejectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "is_approved", "is_active"]
        read_only_fields = ["id", "is_approved", "is_active"]

    def update(self, instance, validated_data):
        instance.is_approved = False
        instance.is_active = False
        instance.save()
        return instance






class EmpProfileSerializer(serializers.ModelSerializer):
    # Prefill username/email from User model, read-only
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = EmpProfile
        fields = ["id", "username", "email", "phone", "address", "profile", "dob", "designation"]




class DailyUpdatesSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    class Meta:
        model = DailyUpdates
        fields = [ 'user','project_name', 'project', 'task_description', 'task_date','status','time_taken']
        read_only_fields = ['id', 'user', 'task_date']  # user and date will be set automatically

    def create(self, validated_data):
        # Automatically assign the logged-in user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)










class MeetingSerializer(serializers.ModelSerializer):
    host = serializers.StringRelatedField(read_only=True)  # shows host username
    count = serializers.SerializerMethodField()

    
    participants = serializers.SlugRelatedField(
        many=True,
        slug_field='username',   # accept "username" instead of ID
        queryset=User.objects.all()
    )

    class Meta:
        model = Meeting
        fields = [
            "id",
            "host",
            "participants",
            "about",
            "meeting_time",
            "meeting_date",
            "link",
            "count",
            # "is_cancel",
            # "reason",
        ]

    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        meeting = Meeting.objects.create(**validated_data)
        meeting.participants.set(participants)
        return meeting


    def get_count(self,obj):
        return obj.participants.count()+1




class ApproveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]   # keep it minimal



class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ['token', 'device_name']
