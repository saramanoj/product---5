from django.urls import path
from .views import PlacementOfficerRegisterAPIView,StudentRegistrationView,RecruiterRegisterView,StudentCoordinatorRegisterView, TrainingCoordinatorRegisterView
from .views import CommonLoginAPIView,PlacementLoginView,RecruiterLoginView,StudentLoginView,TrainingCoordinatorLoginView,AdminLoginView
from .views import ForgotPasswordAPIView,ResetPasswordAPIView,AdminDashboardDataView,TrainingCoordinatorDashboardView,RecruiterDashboardView,PlacementDashboardView,StudentDashboardAPIView
from .views import TrainingCoordinatorProfileView,StudentProfileView,RecruiterProfileView,AdminProfileView

urlpatterns = [
#registration
    path('placement-officer/register/', PlacementOfficerRegisterAPIView.as_view()),
    path('register/student/', StudentRegistrationView.as_view(), name='student-registration'),
    path('recruiter-register/', RecruiterRegisterView.as_view()),
    # path('student-coordinator/register/', StudentCoordinatorRegisterView.as_view(), name="student-coordinator-register"),
    path("training-coordinator/register/", TrainingCoordinatorRegisterView.as_view(), name="training-coordinator-register"),
    
#login
    path("commonlogin/", CommonLoginAPIView.as_view(), name="login"),
    path("placementlogin/", PlacementLoginView.as_view()),
    path("recruiterLogin/",RecruiterLoginView.as_view()),
    path('studentlogin/', StudentLoginView.as_view(), name='student-login'),
    path("training-coordinator/login/",TrainingCoordinatorLoginView.as_view(),name="training-coordinator-login"),
    path("admin/login/", AdminLoginView.as_view(), name="admin-login"),
    path("forgot-password/",ForgotPasswordAPIView.as_view(),name="forgot-password"),
    path("reset-password/",ResetPasswordAPIView.as_view(),name="reset-password"),

#Dashboard
    path('admin-dashboard/', AdminDashboardDataView.as_view(), name='admin-dashboard'),
    path("training-coordinator/dashboard/", TrainingCoordinatorDashboardView.as_view(), name="training-coordinator-dashboard"),
    path('recruiter-dashboard/', RecruiterDashboardView.as_view(), name='recruiter-dashboard'),
    path('placement-dashboard/', PlacementDashboardView.as_view(), name='placement-dashboard'),
    path("student-dashboard/",StudentDashboardAPIView.as_view(),name="student-dashboard"),

#Profile
    path('training-coordinator/profile/', TrainingCoordinatorProfileView.as_view(), name='tc-profile'),
    path('student/profile/', StudentProfileView.as_view(), name='student-profile'),
    path('recruiter/profile/', RecruiterProfileView.as_view(), name='recruiter-profile'),
    path("admin/profile/", AdminProfileView.as_view(), name="admin-profile"),

]
