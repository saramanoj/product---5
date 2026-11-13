from rest_framework import serializers
from .models import TrainingCoordinator

class TrainingCoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCoordinator
        fields = '__all__'
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    # --- NEWLY ADDED ---
    def to_internal_value(self, data):
        data = data.copy()
        field_map = {
            "fullName": "full_name",
            "email": "official_email",
            "mobile": "phone_number",
            "University": "organization_name",
            "EmpId": "employee_id",
            "isEmailVerified": "is_email_verified",
            "isMobileVerified": "is_mobile_verified",
        }
        for new_key, old_key in field_map.items():
            if new_key in data and old_key not in data:
                data[old_key] = data.pop(new_key)
        return super().to_internal_value(data)
    # -------------------