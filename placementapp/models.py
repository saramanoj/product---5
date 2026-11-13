from django.db import models

#registration 

#training coordinator
class TrainingCoordinator(models.Model):

    DESIGNATION_CHOICES = [
    ("","Select Specific Role"),
    ("professor", "Professor"),
    ("trainer", "Trainer"),
    ("admin", "Administrator"),
    ]

    full_name = models.CharField(max_length=100)

    official_email = models.EmailField(unique=True)

    country_code = models.CharField(max_length=5, default="+91")

    phone_number = models.CharField(max_length=10, unique=True)

    organization_name = models.CharField(max_length=150)

    department = models.CharField(max_length=100)

    employee_id = models.CharField(max_length=30, unique=True)

    designation = models.CharField(
        max_length=20,
        choices=DESIGNATION_CHOICES,
    )

    password = models.CharField(max_length=255)

    registered_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name

#placementofficer

class PlacementOfficer(models.Model):
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('trainer', 'Trainer'),
        ('admin', 'Administrator'),
    ]

    full_name = models.CharField(max_length=200)
    official_email = models.EmailField(unique=True)
    country_code = models.CharField(max_length=10, default="+91")
    phone_number = models.CharField(max_length=15)
    organization_name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=100)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    password = models.CharField(max_length=255)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
 #recruiter registration

class Recruiter(models.Model):
    hr_id = models.CharField(max_length=20, unique=True)
    registered_on = models.CharField(max_length=20)

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)

    company = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    password = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name
       
#student registration

from django.contrib.auth.models import AbstractUser

class StudentRegistration(models.Model):
    # Use email as primary authentication field
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        RECRUITER = 'RECRUITER', 'Recruiter'
        TRAINING_COORDINATOR = 'TRAINING_COORDINATOR', 'Training Coordinator'
        PLACEMENT_OFFICER = 'PLACEMENT_OFFICER', 'Placement Officer'
        
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    
    # We allow blank/null usernames as authentication defaults to email
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.email} ({self.role})"


class StudentProfile(models.Model):
    StudentProfile = models.OneToOneField(StudentRegistration, on_delete=models.CASCADE, related_name='student_profile')
    country_code = models.CharField(max_length=10, default='+1')
    phone_number = models.CharField(max_length=20)
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    student_id = models.CharField(max_length=50, unique=True)
    registered_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Student Profile for {self.StudentProfile.email}"

#training coordinaator

class StudentCoordinator(models.Model):

    DESIGNATION_CHOICES = [
    ("","Select Specific Role"),
    ("professor", "Professor"),
    ("trainer", "Trainer"),
    ("admin", "Administrator"),
    ]

    full_name = models.CharField(max_length=100)
    official_email = models.EmailField(unique=True)
    country_code = models.CharField(max_length=5, default="+91")
    phone_number = models.CharField(max_length=10, unique=True)
    organization_name = models.CharField(max_length=150)
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=30, unique=True)
    designation = models.CharField(max_length=20,choices=DESIGNATION_CHOICES,)
    password = models.CharField(max_length=255)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

#login
#common login 

from .managers import UserManager

class commonlogin(AbstractUser):

    ROLE_CHOICES = (
        ("student", "Student"),
        ("recruiter", "Recruiter"),
        ("placement_officer", "Placement Officer"),
        ("training_coordinator", "Training Coordinator"),
    )
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=30,choices=ROLE_CHOICES)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
    
#placementofficerlogin


class PlacementOfficerlogin(models.Model):

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
#recruiterlogin

class RecruiterLogin(models.Model):

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

#studentlogin
class Studentlogin(models.Model):
    # Use email as primary authentication field
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        RECRUITER = 'RECRUITER', 'Recruiter'
        TRAINING_COORDINATOR = 'TRAINING_COORDINATOR', 'Training Coordinator'
        PLACEMENT_OFFICER = 'PLACEMENT_OFFICER', 'Placement Officer'
        
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    
    # We allow blank/null usernames as authentication defaults to email
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.email} ({self.role})"

#trainingcoordinator login

from django.contrib.auth.hashers import make_password

class TrainingCoordinator(models.Model):
    full_name = models.CharField(max_length=150)
    official_email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    
#adminlogin

from django.contrib.auth.hashers import make_password, check_password
class Admin(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email

#trainingCoordinatorDashboard

class DashboardSummary(models.Model):
    active_batches = models.PositiveIntegerField()
    total_enrollments = models.PositiveIntegerField()
    certificates_issued = models.PositiveIntegerField()
    upcoming_sessions = models.PositiveIntegerField()

    def __str__(self):
        return "Dashboard Summary"

#placementofficerdashboard

class DashboardStat(models.Model):
    label = models.CharField(max_length=100)
    value = models.IntegerField()
    badge = models.CharField(max_length=100)
    bg = models.CharField(max_length=30)
    color = models.CharField(max_length=30)


class Pipeline(models.Model):
    stage = models.CharField(max_length=100)
    count = models.IntegerField()


class QuickAction(models.Model):
    label = models.CharField(max_length=100)
    icon = models.CharField(max_length=255)
    bg = models.CharField(max_length=30)
    color = models.CharField(max_length=30)


class UpcomingDrive(models.Model):
    company = models.CharField(max_length=100)
    logo = models.CharField(max_length=255)
    date_time = models.CharField(max_length=100)
    branches = models.CharField(max_length=255)


class TopCompany(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField()
    percentage = models.CharField(max_length=20)


class PlacementStats(models.Model):
    month = models.CharField(max_length=20)
    applied = models.IntegerField()
    offered = models.IntegerField()


class DepartmentWise(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()
    color = models.CharField(max_length=30)


class RecentActivity(models.Model):
    text = models.CharField(max_length=255)
    time = models.CharField(max_length=100)


class CalendarSchedule(models.Model):
    date = models.DateField()
    company = models.CharField(max_length=100)
    logo = models.CharField(max_length=255)
    time = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    students = models.CharField(max_length=100)
    meeting_url = models.URLField()
    meeting_platform = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    status_color = models.CharField(max_length=30)

#trainingCoordinatorProfile
from django.contrib.auth.models import User

class TrainingCoordinatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tc_profile')
    
   
    profile_img = models.ImageField(upload_to='tc_profiles/', null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)

    # --- Read-Only Fields (Set by Admins) ---
    user_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, default='Training Coordinator')
    registration_num = models.CharField(max_length=50, unique=True, null=True, blank=True) # Employee ID
    experience = models.IntegerField(null=True, blank=True) # Stored as an integer (years)
    registration_date = models.DateField(null=True, blank=True) # Joined On
    institute_address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True) # Short quote bio

    def __str__(self):
    return self.user_name

#studentProfile

class DetailedStudentProfile(models.Model):
    user = models.OneToOneField(StudentRegistration, on_delete=models.CASCADE, related_name='detailed_profile')
    
    profile_img = models.ImageField(upload_to='detailed_student_profiles/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    
    institution_name = models.CharField(max_length=255, null=True, blank=True)
    degree = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    cgpa = models.CharField(max_length=10, null=True, blank=True)
    
    student_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    skills = models.JSONField(default=list, blank=True)
    
    registered_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Detailed Profile for {self.user.email}"


#recruiter Profile models
class Recruiter(models.Model):
    """Core Recruiter Identity"""
    userName = models.CharField(max_length=150)
    EmpId = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100)
    Department = models.CharField(max_length=100)
    experience = models.CharField(max_length=50, blank=True)
    joinedOn = models.DateField(null=True, blank=True)
    ProfileImg = models.ImageField(upload_to='profiles/', null=True, blank=True)  # ← Moved here

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Recruiter"
        verbose_name_plural = "Recruiters"

    def __str__(self):
        return f"{self.userName} ({self.EmpId})"


class PersonalInfo(models.Model):
    """Personal Information"""
    recruiter = models.OneToOneField(
        Recruiter,
        on_delete=models.CASCADE,
        related_name='personal_info'
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"Personal Info - {self.recruiter.userName}"


class CompanyDetails(models.Model):
    """Company Details"""
    recruiter = models.OneToOneField(
        Recruiter,
        on_delete=models.CASCADE,
        related_name='company_details'
    )
    Designation = models.CharField(max_length=100)
    company = models.CharField(max_length=150)
    joinedDate = models.DateField(null=True, blank=True)
    Experience = models.CharField(max_length=50, blank=True)
    companyEmail = models.EmailField()
    companyAddress = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    State = models.CharField(max_length=100, blank=True)
    Pincode = models.CharField(max_length=10, blank=True)
 

    def __str__(self):
        return f"Company Details - {self.recruiter.userName}"


class Skill(models.Model):
    """Skills of Recruiter"""
    recruiter = models.ForeignKey(
        Recruiter,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('recruiter', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.recruiter.userName}"


#admin profile
from django.conf import settings

class AdminProfile(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_profile"
    )

    profile_image = models.ImageField(
        upload_to="admin_profiles/",
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    dob = models.DateField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        default="Administrator"
    )

    joined_on = models.DateField(
        blank=True,
        null=True
    )

    experience = models.CharField(
        max_length=50,
        blank=True
    )

    department = models.CharField(
        max_length=100,
        default="Administration"
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    responsibilities = models.JSONField(
        default=list,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"