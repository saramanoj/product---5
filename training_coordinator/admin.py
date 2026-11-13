from django.contrib import admin
from .models import TrainingCoordinator

@admin.register(TrainingCoordinator)
class TrainingCoordinatorAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "official_email",
        "phone_number",
        "employee_id",
        "designation",
        # --- NEWLY ADDED ---
        "gender",
        "is_email_verified",
        "is_mobile_verified",
    )

    search_fields = (
        "full_name",
        "official_email",
        "employee_id",
    )

    list_filter = (
        "designation",
        # --- NEWLY ADDED ---
        "gender",
        "is_email_verified",
        "is_mobile_verified",
    )