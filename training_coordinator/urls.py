from django.urls import path
from .views import TrainingCoordinatorRegisterView

urlpatterns = [
    path(
        "training-coordinator/register/",
        TrainingCoordinatorRegisterView.as_view(),
        name="training-coordinator-register"
    ),
]