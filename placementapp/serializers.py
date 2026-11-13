import re
from .models import PlacementOfficer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

#registration
#placement officer

class PlacementOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementOfficer
        fields = [
            "id", "role", "full_name", "email", "mobile", "university",
            "gender", "emp_id", "password", "bio",
            "is_email_verified", "is_mobile_verified", "terms_accepted",
            "created_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_email_verified": {"read_only": True},
            "is_mobile_verified": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def validate_email(self, value):
        if PlacementOfficer.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value.lower()

    def validate_mobile(self, value):
        if not re.fullmatch(r"[6-9]\d{9}", value):
            raise serializers.ValidationError("Enter a valid 10-digit mobile number.")
        if PlacementOfficer.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("Mobile number already registered.")
        return value

    def validate_emp_id(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Employer ID is required.")
        if PlacementOfficer.objects.filter(emp_id__iexact=value).exists():
            raise serializers.ValidationError("Employer ID already registered.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must contain at least 8 characters.")
        return value

    def validate_bio(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Bio maximum 500 characters.")
        return value

    def validate(self, attrs):
        if not attrs.get("terms_accepted"):
            raise serializers.ValidationError({"terms_accepted": "Please accept the terms and conditions."})
        return attrs

    def create(self, validated_data):
        # Demo project: password is stored as a hash.
        from django.contrib.auth.hashers import make_password
        validated_data["password"] = make_password(validated_data["password"])
        return PlacementOfficer.objects.create(**validated_data)


#recruiter registration

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
import re


class RecruiterRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    terms = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'role', 'full_name', 'email', 'mobile', 'designation',
            'gender', 'company_name', 'website', 'industry',
            'password', 'confirm_password', 'terms',
            'is_email_verified', 'is_mobile_verified',
        ]
        read_only_fields = ['is_email_verified', 'is_mobile_verified']
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True},
            'mobile': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value.lower()

    def validate_mobile(self, value):
        if not re.match(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError("Enter a valid 10-digit mobile number.")
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("Mobile number already registered.")
        return value

    def validate_website(self, value):
        if value:
            pattern = r'^(https?:\/\/)?(www\.)?[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+$'
            if not re.match(pattern, value):
                raise serializers.ValidationError("Enter a valid website URL.")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        if not attrs.get('terms'):
            raise serializers.ValidationError({"terms": "You must accept the terms and conditions."})

        # Optional: force verification before registration
        # if not attrs.get('is_email_verified') or not attrs.get('is_mobile_verified'):
        #     raise serializers.ValidationError("Please verify email and mobile first.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data.pop('terms')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.terms_accepted = True
        user.save()
        return user


class RecruiterSerializer(serializers.ModelSerializer):
    """For Read / Update (no password)"""
    class Meta:
        model = User
        fields = [
            'id', 'role', 'full_name', 'email', 'mobile', 'designation',
            'gender', 'company_name', 'website', 'industry',
            'is_email_verified', 'is_mobile_verified',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['email', 'mobile', 'role', 'is_email_verified', 'is_mobile_verified']


class VerifyOTPSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['email', 'mobile'])
    value = serializers.CharField()
    otp = serializers.CharField(max_length=6)   

#student registration

from django.contrib.auth import get_user_model
from django.db import transaction
from .models import StudentProfile
import re

StudentRegistrationUser = get_user_model()

class StudentRegistrationSerializer(serializers.Serializer):
    fullName = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    countryCode = serializers.CharField(max_length=10, default='+1')
    phoneNumber = serializers.CharField(max_length=20)
    InstitutionName = serializers.CharField(max_length=255)
    Degree = serializers.CharField(max_length=100)
    GraduationYear = serializers.IntegerField()
    StudentID = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if StudentRegistrationUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_StudentID(self, value):
        if StudentProfile.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("A student with this ID is already registered.")
        return value

    def validate(self, data):
        # 1. Password Matching Check
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError({"confirmPassword": "Passwords do not match."})

        # 2. Strong Password Validation
        password = data['password']
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one uppercase letter."})
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one lowercase letter."})
        if not re.search(r"\d", password):
            raise serializers.ValidationError({"password": "Password must contain at least one number."})
        if not re.search(r"[!@#$%^&*]", password):
            raise serializers.ValidationError({"password": "Password must contain at least one special character."})

        # 3. Phone Number Format (10 digits)
        phone = data['phoneNumber']
        if not re.match(r"^\d{10}$", phone):
            raise serializers.ValidationError({"phoneNumber": "Phone number must be exactly 10 digits."})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirmPassword')

        fullName = validated_data.pop('fullName')
        email = validated_data.pop('email')

        with transaction.atomic():
            user = StudentRegistrationUser.objects.create_user(
                email=email,
                username=email,
                full_name=fullName,
                password=password,
                role=StudentRegistrationUser.Role.STUDENT
            )

            StudentProfile.objects.create(
                user=user,
                country_code=validated_data.pop('countryCode'),
                phone_number=validated_data.pop('phoneNumber'),
                institution_name=validated_data.pop('InstitutionName'),
                degree=validated_data.pop('Degree'),
                graduation_year=validated_data.pop('GraduationYear'),
                student_id=validated_data.pop('StudentID')
            )

        return user
    
#student coordinator

from .models import StudentCoordinator

class StudentCoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCoordinator
        fields = '__all__'
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

#training coordinator
class TrainingCoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCoordinator
        fields = '__all__'
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }
        
#login

#common login

class commonLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=[
            "student",
            "recruiter",
            "placement_officer",
            "training_coordinator",
        ]
    )

#placementofficerlogin

from .models import PlacementOfficerlogin

class PlacementOfficerloginSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlacementOfficerlogin
        fields = "__all__"

#recruiterlogin
from .models import RecruiterLogin

class RecruiterLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruiterLogin
        fields = "__all__"

#trainingcoordinatorlogin

class TrainingCoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCoordinator
        fields = '__all__'
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

#adminlogin

from .models import Admin

class AdminLoginSerializer(serializers.Serializer):
    Email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}
        }

#forgotpassword

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()
    password = serializers.CharField(min_length=8)


#placementofficerdashboard

from rest_framework import serializers
from .models import *


class DashboardStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardStat
        fields = "__all__"


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = "__all__"


class QuickActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickAction
        fields = "__all__"


class UpcomingDriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingDrive
        fields = "__all__"


class TopCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TopCompany
        fields = "__all__"


class PlacementStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementStats
        fields = "__all__"


class DepartmentWiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentWise
        fields = "__all__"


class RecentActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentActivity
        fields = "__all__"


class CalendarScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarSchedule
        fields = "__all__"
        
#trainingcoordinatorprofile
from rest_framework import serializers
from .models import TrainingCoordinatorProfile

class TrainingCoordinatorProfileSerializer(serializers.ModelSerializer):
    # Mapping Django snake_case to React camelCase exactly
    ProfileImg = serializers.ImageField(source='profile_img', required=False)
    userName = serializers.CharField(source='user_name', read_only=True)
    RegistrationNum = serializers.CharField(source='registration_num', read_only=True)
    RegistrationDate = serializers.DateField(source='registration_date', read_only=True)
    InstituteAddress = serializers.CharField(source='institute_address', read_only=True)
    Bio = serializers.CharField(source='bio', read_only=True)
    aboutme = serializers.CharField(source='about_me', required=False, allow_blank=True)

    class Meta:
        model = TrainingCoordinatorProfile
        fields = [
            'id', 'ProfileImg', 'userName', 'designation', 'email', 'phone', 
            'city', 'state', 'Bio', 'dob', 'gender', 'address', 
            'RegistrationNum', 'experience', 'RegistrationDate', 
            'InstituteAddress', 'aboutme'
        ]
        
        # Locking down the fields React has marked as disabled
        read_only_fields = [
            'designation', 'city', 'state', 'experience'
        ]

#studentprofile
from .models import DetailedStudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    ProfileImg = serializers.ImageField(source='profile_img', required=False)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='phone_number', required=False, allow_blank=True)
    address1 = serializers.CharField(source='address', required=False, allow_blank=True)
    city = serializers.CharField(source='city', required=False, allow_blank=True)
    gender = serializers.CharField(source='gender', required=False, allow_blank=True)
    dob = serializers.DateField(source='dob', required=False, allow_null=True)
    aboutme = serializers.CharField(source='about_me', required=False, allow_blank=True)
    CGPA = serializers.CharField(source='cgpa', required=False, allow_blank=True)
    Department = serializers.CharField(source='department', required=False, allow_blank=True)
    InstitutionName = serializers.CharField(source='institution_name', required=False, allow_blank=True)
    Degree = serializers.CharField(source='degree', required=False, allow_blank=True)
    GraduationYear = serializers.IntegerField(source='graduation_year', required=False, allow_null=True)
    StudentID = serializers.CharField(source='student_id', required=False, allow_blank=True)
    skills = serializers.JSONField(source='skills', required=False)

    class Meta:
        model = DetailedStudentProfile
        fields = [
            'id', 'ProfileImg', 'email', 'phone', 'address1', 'city', 'gender', 'dob',
            'aboutme', 'CGPA', 'Department', 'InstitutionName', 'Degree', 'GraduationYear',
            'StudentID', 'skills'
        ]
        read_only_fields = ['email']

#recruiter profile serializers
from .models import Recruiter, PersonalInfo, CompanyDetails, Skill
import re

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = [
            'email', 'phone', 'gender', 'dob',
            'address1', 'address2', 'city', 'state', 'pincode'
        ]

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("*Email is required")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("*Enter a valid email address")
        return value

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("*Phone number is required")
        if not re.match(r'^[6-9]\d{9}$', value.strip()):
            raise serializers.ValidationError("*Enter a valid 10-digit phone number")
        return value.strip()

    def validate_gender(self, value):
        if not value or value == "Select":
            raise serializers.ValidationError("*please select your Gender")
        return value

    def validate_dob(self, value):
        if not value:
            raise serializers.ValidationError("*Select Your Date of Birth")
        return value

    def validate_address1(self, value):
        if not value:
            raise serializers.ValidationError("*please enter Address")
        return value

    def validate_city(self, value):
        if not value:
            raise serializers.ValidationError("*City is Required")
        return value

    def validate_state(self, value):
        if not value:
            raise serializers.ValidationError("*State is Required")
        return value

    def validate_pincode(self, value):
        if not value:
            raise serializers.ValidationError("*Pincode is Required")
        if not re.match(r'^\d{6}$', str(value).strip()):
            raise serializers.ValidationError("*Pincode must be 6 digits")
        return value


class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = [
            'Designation','company', 'joinedDate', 'Experience', 'companyEmail', 'companyAddress',
            'city', 'State', 'Pincode'
        ]

    def validate_companyEmail(self, value):
        if not value:
            raise serializers.ValidationError("please enter Company Email")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("*Enter a valid company email")
        return value

    def validate_companyAddress(self, value):
        if not value:
            raise serializers.ValidationError("*Company Address Required")
        return value

    def validate_companyLocation(self, value):
        if not value:
            raise serializers.ValidationError("*City is Required")
        return value

    def validate_companyState(self, value):
        if not value:
            raise serializers.ValidationError("*State is Required")
        return value

    def validate_companyPincode(self, value):
        if not value:
            raise serializers.ValidationError("*Pincode is Required")
        if not re.match(r'^\d{6}$', str(value).strip()):
            raise serializers.ValidationError("*Pincode must be 6 digits")
        return value


class RecruiterSerializer(serializers.ModelSerializer):
    personal_info = PersonalInfoSerializer(required=False)
    company_details = CompanyDetailsSerializer(required=False)
    skills = SkillSerializer(many=True, required=False)
    ProfileImg = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Recruiter
        fields = [
            'id', 'userName', 'EmpId', 'designation', 'Department',
            'experience', 'joinedOn', 'ProfileImg',
            'personal_info', 'company_details', 'skills',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.ProfileImg and request:
            data['ProfileImg'] = request.build_absolute_uri(instance.ProfileImg.url)
        elif instance.ProfileImg:
            data['ProfileImg'] = instance.ProfileImg.url
        else:
            data['ProfileImg'] = None
        return data

    def create(self, validated_data):
        personal_data = validated_data.pop('personal_info', None)
        company_data = validated_data.pop('company_details', None)
        skills_data = validated_data.pop('skills', [])

        recruiter = Recruiter.objects.create(**validated_data)

        if personal_data:
            PersonalInfo.objects.create(recruiter=recruiter, **personal_data)

        if company_data:
            CompanyDetails.objects.create(recruiter=recruiter, **company_data)

        for skill in skills_data:
            Skill.objects.create(recruiter=recruiter, name=skill['name'])

        return recruiter

    def update(self, instance, validated_data):
        personal_data = validated_data.pop('personal_info', None)
        company_data = validated_data.pop('company_details', None)
        skills_data = validated_data.pop('skills', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if personal_data is not None:
            personal_info, _ = PersonalInfo.objects.get_or_create(recruiter=instance)
            for attr, value in personal_data.items():
                setattr(personal_info, attr, value)
            personal_info.save()

        if company_data is not None:
            company_details, _ = CompanyDetails.objects.get_or_create(recruiter=instance)
            for attr, value in company_data.items():
                setattr(company_details, attr, value)
            company_details.save()

        if skills_data is not None:
            instance.skills.all().delete()
            for skill in skills_data:
                Skill.objects.create(recruiter=instance, name=skill['name'])

        return instance

#adminprofile

from .models import AdminProfile


class AdminProfileSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email"
    )

    profile_image = serializers.ImageField(
        required=False,
        allow_null=True
    )

    class Meta:

        model = AdminProfile

        fields = [
            "id",
            "user_name",
            "email",
            "profile_image",
            "gender",
            "phone",
            "dob",
            "address",
            "city",
            "state",
            "designation",
            "joined_on",
            "experience",
            "department",
            "employee_id",
            "responsibilities",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user_name",
            "designation",
            "joined_on",
            "experience",
            "department",
            "employee_id",
            "responsibilities",
            "created_at",
            "updated_at",
        ]

    def validate_phone(self, value):

        if not value:
            return value

        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        if value[0] not in "6789":
            raise serializers.ValidationError(
                "Enter a valid Indian mobile number."
            )

        return value

    def update(self, instance, validated_data):

        # ------------------------------------------
        # Update Django User email
        # ------------------------------------------

        user_data = validated_data.pop("user", {})

        if "email" in user_data:

            instance.user.email = user_data["email"]

            instance.user.save(
                update_fields=["email"]
            )

        # ------------------------------------------
        # Update AdminProfile
        # ------------------------------------------

        for attr, value in validated_data.items():

            setattr(
                instance,
                attr,
                value
            )

        instance.save()

        return instance
