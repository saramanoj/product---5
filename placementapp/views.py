from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PlacementOfficerSerializer

#registration
#placement officer
class PlacementOfficerRegisterAPIView(APIView):

    def post(self, request):
        serializer = PlacementOfficerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Registration Successful",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#recruiter registration

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Recruiter
from .serializers import RecruiterSerializer
from datetime import date

# @api_view(['POST'])
# def recruiter_register(request):

from rest_framework.views import APIView

class RecruiterRegisterView(APIView):

    def get(self, request):
        return Response({"message": "Recruiter API Working"})

    def post(self, request):
        # POST logic here

        count = Recruiter.objects.count() + 1

        hr_id = f"HR-{count:03}"

        today = date.today().strftime("%d/%m/%Y")

        data = request.data.copy()

        data["hr_id"] = hr_id
        data["registered_on"] = today

        serializer = RecruiterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Registration Successful",
                "data":serializer.data
            },status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#student registration
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentRegistrationSerializer

class StudentRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration successful!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#student coordinator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentCoordinator
from .serializers import StudentCoordinatorSerializer


class StudentCoordinatorRegisterView(APIView):

    def post(self, request):
        serializer = StudentCoordinatorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Student Coordinator registered successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#training coordinator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TrainingCoordinator
from .serializers import TrainingCoordinatorSerializer


class TrainingCoordinatorRegisterView(APIView):

    def post(self, request):
        serializer = TrainingCoordinatorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Training Coordinator registered successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
#login
#common login
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import commonLoginSerializer

class CommonLoginAPIView(APIView):

    def post(self, request):
        serializer = commonLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        role = serializer.validated_data["role"]

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is None:
            return Response(
                {
                    "success": False,
                    "message": "Invalid email or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.role != role:
            return Response(
                {
                    "success": False,
                    "message": "Selected role does not match the user."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "success": True,
                "message": "Login successful.",

                "access": str(refresh.access_token),
                "refresh": str(refresh),

                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                }
            },
            status=status.HTTP_200_OK
        )
    
#PLACEMENTOFFICERLOGIN

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PlacementOfficerlogin


class PlacementLoginView(APIView):

    def post(self, request):

        email = request.data.get("Email")
        password = request.data.get("password")

        if not email:
            return Response({
                "Email":"Email is required*"
            },status=400)

        if not password:
            return Response({
                "password":"Password is required*"
            },status=400)

        try:
            user = PlacementOfficerlogin.objects.get(email=email)

        except PlacementOfficerlogin.DoesNotExist:

            return Response({
                "loginError":"Invalid Email or Password. Please try again."
            },status=400)

        if user.password != password:

            return Response({
                "loginError":"Invalid Email or Password. Please try again."
            },status=400)

        return Response({

            "message":"Login Successful",

            "user":{

                "id":user.id,
                "email":user.email

            }

        },status=200)

#recruiterlogin

from rest_framework.views import APIView
from .models import RecruiterLogin

class RecruiterLoginView(APIView):

    def post(self, request):

        email = request.data.get("Email")
        password = request.data.get("password")

        if not email:
            return Response({
                "Email":"Email is required*"
            },status=400)

        if not password:
            return Response({
                "password":"Password is required*"
            },status=400)

        try:
            user = RecruiterLogin.objects.get(email=email)

        except RecruiterLogin.DoesNotExist:

            return Response({
                "loginError":"Invalid Email or Password. Please try again."
            },status=400)

        if user.password != password:

            return Response({
                "loginError":"Invalid Email or Password. Please try again."
            },status=400)

        return Response({

            "message":"Login Successful",

            "user":{

                "id":user.id,
                "email":user.email

            }

        },status=200)

#studentlogin 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class StudentLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate checks the credentials against the database
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Generate JWT tokens manually
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'role': user.role,
                'full_name': user.full_name,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid Email or Password."}, status=status.HTTP_401_UNAUTHORIZED)

#trainingcoordinator login

from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TrainingCoordinator
from .serializers import TrainingCoordinatorSerializer


class TrainingCoordinatorLoginView(APIView):

    def post(self, request):
        serializer = TrainingCoordinatorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Training Coordinator registered successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#adminlogin

from .models import Admin
from .serializers import AdminLoginSerializer

class AdminLoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = AdminLoginSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data["Email"]
            password = serializer.validated_data["password"]

            try:
                admin = Admin.objects.get(email=email)

            except Admin.DoesNotExist:

                return Response(
                    {
                        "success": False,
                        "message": "Invalid Credentials"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not admin.verify_password(password):

                return Response(
                    {
                        "success": False,
                        "message": "Invalid Credentials"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            refresh = RefreshToken()

            return Response({

                "success": True,
                "message": "Login Successful",

                "access": str(refresh.access_token),
                "refresh": str(refresh),

                "admin": {
                    "id": admin.id,
                    "full_name": admin.full_name,
                    "email": admin.email
                }

            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#forgotpassword

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import (urlsafe_base64_encode,urlsafe_base64_decode)
from django.utils.encoding import (force_bytes,force_str)
from django.core.mail import send_mail
from .serializers import (ForgotPasswordSerializer,ResetPasswordSerializer)

User = get_user_model()

class ForgotPasswordAPIView(APIView):

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": "Email not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = (
                f"http://localhost:5173/reset-password/{uid}/{token}/"
            )
            send_mail(
                subject="Password Reset",
                message=f"""
Hello,

Click below to reset your password.

{reset_link}

If you didn't request this, ignore this email.
""",

                from_email=None,
                recipient_list=[email],
            )

            return Response(
                {
                    "success": True,
                    "message": "Reset link sent successfully."
                }
            )

        return Response(serializer.errors, status=400)
    
class ResetPasswordAPIView(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data["uid"]
            token = serializer.validated_data["token"]
            password = serializer.validated_data["password"]

            try:
                user_id = force_str(
                    urlsafe_base64_decode(uid)
                )
                user = User.objects.get(pk=user_id)

            except:
                return Response(
                    {
                        "message": "Invalid Link"
                    },
                    status=400
                )

            if not PasswordResetTokenGenerator().check_token(
                user,
                token
            ):

                return Response(
                    {
                        "message": "Invalid or Expired Token"
                    },
                    status=400
                )

            user.set_password(password)
            user.save()
            return Response(
                {
                    "success": True,
                    "message": "Password Changed Successfully"
                }
            )

        return Response(serializer.errors, status=400)

#adminDashboard
from rest_framework.views import APIView
from rest_framework.response import Response

class AdminDashboardDataView(APIView):
    def get(self, request):
        mock_data = {
            "status": "success",
            "data": {
                "stats": {
                    "totalPlacements": "4,120",
                    "activeStudents": "12,482",
                    "verifiedRecruiters": "3,142",
                    "partnerCompanies": "312"
                },
                "placementData": [
                    { "month": "Jan", "placements": 22 },
                    { "month": "Feb", "placements": 34 },
                    { "month": "Mar", "placements": 28 },
                    { "month": "Apr", "placements": 47 },
                    { "month": "May", "placements": 39 },
                    { "month": "Jun", "placements": 58 }
                ],
                "activityLog": [
                    { "id": 1, "type": "new_user", "heading": "New User Registration", "subtitle": "Alex Morgan", "time": "2 mins ago" },
                    { "id": 2, "type": "doc_upload", "heading": "Company Document Uploaded", "subtitle": "Nexus Dynamics", "time": "45 mins ago" },
                    { "id": 3, "type": "recruiter_verify", "heading": "Recruiter Verified", "subtitle": "Global Tech", "time": "3 hrs ago" },
                    { "id": 4, "type": "security_update", "heading": "Security Policy Updated", "subtitle": "Applied globally", "time": "5 hrs ago" },
                    { "id": 5, "type": "login_failed", "heading": "Failed Login Attempt", "subtitle": "IP:192.168.1.45", "time": "8 hrs ago" }
                ],
                "userManagement": [
                    { "id": 1, "name": "Sarah K. Jenkins", "email": "sarah.j@globalhr.com", "role": "RECRUITER", "activity": "Published \"Senior AI Architect\" role", "time": "2 mins ago" },
                    { "id": 2, "name": "David Lee", "email": "d.lee@candidate.me", "role": "CANDIDATE", "activity": "Submitted portfolio via AI matching", "time": "1 hour ago" }
                ]
            }
        }
        return Response(mock_data)

#Training coordinator dashboard
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import DashboardSummary
from .serializers import DashboardSummarySerializer

class TrainingCoordinatorDashboardView(APIView):

    def get(self, request):
        dashboard_data = {
        "status": "success",
        "data": {

            "stats": {
                "activeBatches": 1250,
                "totalEnrollments": 462,
                "certificatesIssued": 199,
                "upcomingSessions": 35,
            },

            "upcomingSessions": [
                {
                    "id": 1,
                    "time": "10:00",
                    "period": "AM",
                    "title": "Full Stack",
                    "courseCode": "FS-DP-07",
                    "location": "FS-DP-07. Lab 1, Block A",
                    "status": "Scheduled",
                },
                {
                    "id": 2,
                    "time": "11:30",
                    "period": "AM",
                    "title": "Python Programming",
                    "courseCode": "PY-08",
                    "location": "PY-08. Lab 2, Block B",
                    "status": "In-Progress",
                },
                {
                    "id": 3,
                    "time": "02:00",
                    "period": "PM",
                    "title": "UI/UX Design",
                    "courseCode": "UIUX-06",
                    "location": "UIUX-06. Design Studio",
                    "status": "Scheduled",
                },
                {
                    "id": 4,
                    "time": "04:30",
                    "period": "PM",
                    "title": "Trainer Meeting",
                    "courseCode": "MEETING-01",
                    "location": "Conference Room",
                    "status": "Meeting",
                },
            ],

            "trainerAvailability": [
                {
                    "id": 1,
                    "name": "Sam Son",
                    "role": "Full Stack",
                    "status": "Available",
                },
                {
                    "id": 2,
                    "name": "David",
                    "role": "Python",
                    "status": "In Session",
                },
                {
                    "id": 3,
                    "name": "Sneha",
                    "role": "Data Analytics",
                    "status": "On Leave",
                },
                {
                    "id": 4,
                    "name": "Angel",
                    "role": "UI/UX",
                    "status": "Available",
                },
            ],

            "readiness": [
                {
                    "name": "Ready",
                    "value": 845,
                    "color": "#6ECEE9",
                },
                {
                    "name": "Need Mock Interview",
                    "value": 215,
                    "color": "#B46BEA",
                },
                {
                    "name": "Resume Pending",
                    "value": 145,
                    "color": "#7992E6",
                },
                {
                    "name": "Other Pending",
                    "value": 65,
                    "color": "#6409FF",
                },
            ],

        
            "recentActivities": [
                {
                    "id": 1,
                    "text": 'New batch "D-12" has been created.',
                    "date": "July 20 · 09:30 AM",
                },
                {
                    "id": 2,
                    "text": 'Assessment "Java test published."',
                    "date": "July 15 · 10:30 AM",
                },
                {
                    "id": 3,
                    "text": 'Session completed for "UI/UX laws".',
                    "date": "July 06 · 04:30 AM",
                },
                {
                    "id": 4,
                    "text": "Certificate issued to 12 students.",
                    "date": "July 10 · 03:30 AM",
                },
                {
                    "id": 5,
                    "text": 'New batch "UI-08" has been created.',
                    "date": "July 11 · 09:30 AM",
                },
            ],

            "pendingApprovals": [
                {
                    "id": 1,
                    "title": "Leave Request",
                    "count": 8,
                    "countText": "8 Requests",
                },
                {
                    "id": 2,
                    "title": "Assessment Evaluation",
                    "count": 15,
                    "countText": "15 Pending",
                },
                {
                    "id": 3,
                    "title": "Certificate Requests",
                    "count": 6,
                    "countText": "6 Requests",
                },
                {
                    "id": 4,
                    "title": "Course Transfer",
                    "count": 3,
                    "countText": "3 Requests",
                },
            ],


            "trainingProgress": [
                {
                    "id": 1,
                    "title": "Full Stack",
                    "code": "FS-DP-07",
                    "percent": 90,
                    "completed": 320,
                    "total": 356,
                },
                {
                    "id": 2,
                    "title": "Python",
                    "code": "PY-08",
                    "percent": 81,
                    "completed": 286,
                    "total": 300,
                },
                {
                    "id": 3,
                    "title": "Data Analytics",
                    "code": "DA-05",
                    "percent": 58,
                    "completed": 145,
                    "total": 248,
                },
                {
                    "id": 4,
                    "title": "UI/UX",
                    "code": "UI-09",
                    "percent": 94,
                    "completed": 210,
                    "total": 223,
                },
                {
                    "id": 5,
                    "title": "Java",
                    "code": "JD-04",
                    "percent": 72,
                    "completed": 321,
                    "total": 445,
                },
            ],


            "attendance": {
                "present": 1182,
                "absent": 49,
                "presentPercentage": 96,
            },
        }
    }

    return Response(dashboard_data)

#recruiter Dashboard
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.utils import timezone

from .models import *
from .serializers import *

class RecruiterDashboardView(APIView):
    """
    Single endpoint that returns everything the RecruiterDashboard needs.
    GET /api/dashboard/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Stats – prefer stored snapshots, fall back to live counts
        stored_stats = {s.key: s for s in DashboardStat.objects.all()}
        active_jobs = Job.objects.filter(status='active').count()
        new_apps = Application.objects.filter(
            applied_at__date=timezone.now().date()
        ).count()
        interviews_today = Interview.objects.filter(
            scheduled_at__date=timezone.now().date(),
            status='scheduled'
        ).count()
        placements_count = Placement.objects.count()

        def build_stat(key, live_value, default_badge='', default_class=''):
            s = stored_stats.get(key)
            if s:
                return {
                    'id': s.id,
                    'key': s.key,
                    'title': key.replace('_', ' ').upper(),
                    'value': s.value,
                    'badgeText': s.badge_text or default_badge,
                    'badgeClass': s.badge_class or default_class,
                }
            return {
                'id': None,
                'key': key,
                'title': key.replace('_', ' ').upper(),
                'value': live_value,
                'badgeText': default_badge,
                'badgeClass': default_class,
            }

        stats = [
            build_stat('active_jobs', active_jobs, '+12% VS LAST MO', 'Rec-Dashboard-badge-positive'),
            build_stat('new_applications', new_apps or Application.objects.count(), '+4 NEW TODAY', 'Rec-Dashboard-badge-blue'),
            build_stat('interviews_today', interviews_today, 'URGENT', 'Rec-Dashboard-badge-urgent'),
            build_stat('placements', placements_count, 'Target: 20', 'Rec-Dashboard-badge-target'),
        ]

        # Pipeline
        stage_map = {
            'sourcing': 'SOURCING',
            'applied': 'APPLIED',
            'interviewing': 'INTERVIEWING',
            'offer': 'OFFER STAGE',
        }
        stage_counts = dict(
            Application.objects.values('stage').annotate(c=Count('id')).values_list('stage', 'c')
        )
        # Include sourcing even if zero applications in that stage
        max_count = max(stage_counts.values()) if stage_counts else 1
        pipeline = []
        for key, label in stage_map.items():
            count = stage_counts.get(key, 0)
            pct = int((count / max_count) * 100) if max_count else 0
            pipeline.append({
                'stage': label,
                'count': count,
                'percentage': f'{pct}%',
            })

        pipeline_metrics = [
            {'label': 'AVG. RESPONSE', 'value': '4.2d'},
            {'label': 'CONVERSION', 'value': '18%'},
            {'label': 'TIME TO HIRE', 'value': '22d'},
        ]

        # Upcoming interviews
        interviews_qs = Interview.objects.filter(
            scheduled_at__gte=timezone.now(),
            status='scheduled'
        ).select_related('application__candidate', 'application__job')[:10]
        interviews = InterviewSerializer(interviews_qs, many=True).data

        # Resume verification table (from candidates + latest application status)
        verifications = []
        for c in Candidate.objects.all()[:20]:
            app = c.applications.order_by('-applied_at').first()
            status_label = app.status if app else 'pending'
            verifications.append({
                'id': c.id,
                'candidate': c.name,
                'resume': {
                    'label': 'Verified' if c.resume_verified else 'Pending',
                    'verified': c.resume_verified,
                },
                'portfolio': {
                    'label': 'Available' if c.portfolio_available else 'Not Available',
                    'available': c.portfolio_available,
                },
                'status': {
                    'label': status_label.capitalize(),
                    'value': status_label,
                },
            })

        ai_insights = AIInsightSerializer(
            AIInsight.objects.filter(is_active=True)[:5], many=True
        ).data

        quick_links = QuickLinkSerializer(
            QuickLink.objects.filter(is_active=True), many=True
        ).data

        return Response({
            'user': UserSerializer(request.user).data,
            'stats': stats,
            'pipeline': pipeline,
            'pipeline_metrics': pipeline_metrics,
            'interviews': interviews,
            'verifications': verifications,
            'ai_insights': ai_insights,
            'quick_links': quick_links,
        })

#placementofficerdashboard
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
from .serializers import *


class PlacementDashboardView(APIView):
    def get(self, request):
        data = {
        "stats": DashboardStatSerializer(
            DashboardStat.objects.all(),
            many=True
        ).data,

        "pipeline": PipelineSerializer(
            Pipeline.objects.all(),
            many=True
        ).data,

        "quickActions": QuickActionSerializer(
            QuickAction.objects.all(),
            many=True
        ).data,

        "upcomingDrives": UpcomingDriveSerializer(
            UpcomingDrive.objects.all(),
            many=True
        ).data,

        "topCompanies": TopCompanySerializer(
            TopCompany.objects.all(),
            many=True
        ).data,

        "placementStats": PlacementStatsSerializer(
            PlacementStats.objects.all(),
            many=True
        ).data,

        "departmentWise": DepartmentWiseSerializer(
            DepartmentWise.objects.all(),
            many=True
        ).data,

        "recentActivities": RecentActivitySerializer(
            RecentActivity.objects.all(),
            many=True
        ).data,

        "calendarSchedules": CalendarScheduleSerializer(
            CalendarSchedule.objects.all(),
            many=True
        ).data,
    }

    return Response(data)

#Student Dashboard
from rest_framework.views import APIView
from rest_framework.response import Response


class StudentDashboardAPIView(APIView):

    def get(self, request):

        data = {
         
            "student": {
                "name": "Alex",
                "profile_strength": 85,
                "profile_status": "Complete",
            },

            
            "summary": {
                "total_applications": 12,
                "applications_this_week": 3,
                "scheduled_interviews": 3,
                "next_interview": "2:00 PM",
                "application_updates_today": 2,
                "profile_strength": 85,
            },

           
            "applications": [
                {
                    "company": "Google",
                    "role": "Software Engineer Intern",
                    "status": "Under Review",
                    "updated": "Updated 2h ago",
                    "logo": "google_icon",
                },
                {
                    "company": "Stripe",
                    "role": "UI Designer",
                    "status": "Interview Scheduled",
                    "updated": "Tomorrow, 10:00 AM",
                    "logo": "stripe_icon",
                },
            ],

            # -----------------------------------------
            # RECOMMENDED JOBS
            # -----------------------------------------
            "recommended_jobs": [
                {
                    "title": "Product Designer",
                    "company": "Figma",
                    "location": "San Francisco, CA",
                    "type": "Remote",
                    "skills": [
                        "Figma",
                        "UI/UX",
                        "Design",
                    ],
                    "logo": "figmaLogo",
                },
                {
                    "title": "Frontend Engineer",
                    "company": "Vercel",
                    "location": "New York, NY",
                    "type": "",
                    "skills": [
                        "React",
                        "Tailwind",
                        "Next.js",
                    ],
                    "logo": "vercelLogo",
                },
                {
                    "title": "Backend Developer",
                    "company": "Supabase",
                    "location": "Austin, TX",
                    "type": "Remote",
                    "skills": [
                        "Node.js",
                        "PostgreSQL",
                        "Go",
                    ],
                    "logo": "figmaLogo",
                },
                {
                    "title": "Fullstack Engineer",
                    "company": "Stripe",
                    "location": "Seattle, WA",
                    "type": "Hybrid",
                    "skills": [
                        "TypeScript",
                        "React",
                        "Ruby",
                    ],
                    "logo": "figmaLogo",
                },
            ],

         
            "upcoming_tasks": [
                {
                    "date": "24 OCT",
                    "title": "Stripe Interview",
                    "time": "10:00 AM - 11:00 AM",
                    "note": (
                        "Review design portfolio and case studies "
                        "on payment flows."
                    ),
                    "icon": "clock_icon",
                },
                {
                    "date": "26 OCT",
                    "title": "Mock Session",
                    "time": "03:30 PM",
                    "note": "With Career Coach: Sarah M.",
                    "icon": "video_icon",
                },
                {
                    "date": "30 OCT",
                    "title": "Tech Workshop",
                    "time": "01:00 PM",
                    "note": "Mastering System Design",
                    "icon": "team_icon",
                },
            ],

            
            "offers": [
                {
                    "title": "Staff Engineer",
                    "company": "NexGen Fintech Solutions",
                    "salary": "$165,000 /yr",
                    "joining_date": "Nov 12, 2024",
                    "location": "Remote (Global)",
                    "benefits": "0.05% Equity",
                    "expires_in_days": 2,
                    "logo": "job_icon",
                    "secondary_icon": "stock_options_icon",
                },
                {
                    "title": "UX Strategy Lead",
                    "company": "Lumina Digital Agency",
                    "salary": "$142,000 /yr",
                    "joining_date": "Jan 05, 2025",
                    "location": "New York, NY",
                    "benefits": "Full Coverage",
                    "expires_in_days": 6,
                    "logo": "job_icon2",
                    "secondary_icon": "benefits_icon",
                },
            ],

            
            "application_status": [
                {
                    "name": "Applied",
                    "value": 8,
                    "color": "#FDBA8C",
                },
                {
                    "name": "Shortlisted",
                    "value": 4,
                    "color": "#A855F7",
                },
                {
                    "name": "Interview",
                    "value": 2,
                    "color": "#33C3F0",
                },
                {
                    "name": "Selected",
                    "value": 1,
                    "color": "#9B8AF7",
                },
            ],

            # -----------------------------------------
            # TODAY'S TASKS
            # -----------------------------------------
            "todays_tasks": [
                {
                    "title": "Update Resume",
                    "icon": "resume_icon",
                    "completed": False,
                },
                {
                    "title": "Complete Assessment",
                    "icon": "assessment_icon",
                    "completed": False,
                },
                {
                    "title": "Attend mock interview",
                    "icon": "interview_icon",
                    "completed": False,
                },
                {
                    "title": "Join Workshop",
                    "icon": "workshop_icon",
                    "completed": False,
                },
            ],
        }

        return Response(data)


#Training coordinator profile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import TrainingCoordinatorProfile
from .serializers import TrainingCoordinatorProfileSerializer


class TrainingCoordinatorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = TrainingCoordinatorProfileSerializer
    permission_classes = [IsAuthenticated]

    # Automatically grab the profile belonging to the logged-in user
    def get_object(self):
        profile, created = TrainingCoordinatorProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

# Student profile
from .models import DetailedStudentProfile
from .serializers import StudentProfileSerializer

class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = DetailedStudentProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

#recruiter profile
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Recruiter, PersonalInfo, CompanyDetails, Skill
from .serializers import (
    RecruiterSerializer,
    PersonalInfoSerializer,
    CompanyDetailsSerializer,
    SkillSerializer
)

class RecruiterProfileView(generics.RetrieveUpdateAPIView):
    queryset = Recruiter.objects.select_related(
        'personal_info', 'company_details'
    ).prefetch_related('skills').all()

    serializer_class = RecruiterSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    # ========== PERSONAL INFORMATION ==========
    @action(detail=True, methods=['get', 'patch'], url_path='personal-info')
    def personal_info(self, request, pk=None):
        recruiter = self.get_object()
        personal_info, _ = PersonalInfo.objects.get_or_create(recruiter=recruiter)

        if request.method == 'GET':
            serializer = PersonalInfoSerializer(personal_info)
            return Response(serializer.data)

        serializer = PersonalInfoSerializer(
            personal_info,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # ========== COMPANY DETAILS ==========
    @action(detail=True, methods=['get', 'patch'], url_path='company-details')
    def company_details(self, request, pk=None):
        recruiter = self.get_object()
        company_details, _ = CompanyDetails.objects.get_or_create(recruiter=recruiter)

        if request.method == 'GET':
            serializer = CompanyDetailsSerializer(company_details)
            return Response(serializer.data)

        serializer = CompanyDetailsSerializer(
            company_details,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # ========== PROFILE IMAGE ==========
    @action(detail=True, methods=['patch', 'delete'], url_path='profile-image')
    def profile_image(self, request, pk=None):
        recruiter = self.get_object()

        if request.method == 'PATCH':
            image = request.FILES.get('ProfileImg')
            if not image:
                return Response(
                    {"ProfileImg": ["No image provided"]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recruiter.ProfileImg = image
            recruiter.save()
            serializer = self.get_serializer(recruiter)
            return Response(serializer.data)

        # DELETE - Remove profile image
        if recruiter.ProfileImg:
            recruiter.ProfileImg.delete(save=False)
            recruiter.ProfileImg = None
            recruiter.save()
        return Response({"message": "Profile image removed"}, status=status.HTTP_204_NO_CONTENT)

    # ========== SKILLS ==========
    @action(detail=True, methods=['get', 'post', 'put'], url_path='skills')
    def skills(self, request, pk=None):
        recruiter = self.get_object()

        if request.method == 'GET':
            skills = recruiter.skills.all()
            serializer = SkillSerializer(skills, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            skill_name = request.data.get('name', '').strip()
            if not skill_name:
                return Response(
                    {"name": ["Skill name is required"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            skill, created = Skill.objects.get_or_create(
                recruiter=recruiter,
                name=skill_name
            )
            if not created:
                return Response(
                    {"name": ["Skill already exists"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(SkillSerializer(skill).data, status=status.HTTP_201_CREATED)

        if request.method == 'PUT':
            skills_list = request.data.get('skills', [])

            if not isinstance(skills_list, list) or len(skills_list) == 0:
                return Response(
                    {"skills": ["*Add atleast one Skill"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            recruiter.skills.all().delete()

            new_skills = []
            for name in skills_list:
                name = name.strip() if isinstance(name, str) else name.get('name', '').strip()
                if name:
                    skill = Skill.objects.create(recruiter=recruiter, name=name)
                    new_skills.append(skill)

            serializer = SkillSerializer(new_skills, many=True)
            return Response(serializer.data)

    # ========== DELETE SINGLE SKILL ==========
    @action(detail=True, methods=['delete'], url_path=r'skills/(?P<skill_id>\d+)')
    def delete_skill(self, request, pk=None, skill_id=None):
        recruiter = self.get_object()
        try:
            skill = recruiter.skills.get(id=skill_id)
            skill.delete()
            return Response(
                {"message": "Skill deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Skill.DoesNotExist:
            return Response(
                {"error": "Skill not found"},
                status=status.HTTP_404_NOT_FOUND
            )

from .serializers import AdminProfileSerializer

#admin profile

def get_or_create_admin_profile(user):

    profile, created = AdminProfile.objects.get_or_create(

        user=user,

        defaults={
            "employee_id": f"ADM-{user.id:04d}",

            "designation": "Administrator",

            "department": "Administration",

            "experience": "0 years",

            "responsibilities": [
                "User Management",
                "Role & Permission Control",
                "Company Verification",
                "Reports Monitoring"
            ]
        }
    )

    return profile
    
class AdminProfileView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [
        JSONParser,
        MultiPartParser,
        FormParser
    ]

    def get(self, request):

        profile = get_or_create_admin_profile(
            request.user
        )

        serializer = AdminProfileSerializer(
            profile,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )