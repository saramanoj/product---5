from django.db import models


class TrainingCoordinator(models.Model):

    DESIGNATION_CHOICES = [
    ("","Select Specific Role"),
    ("professor", "Professor"),
    ("trainer", "Trainer"),
    ("admin", "Administrator"),
    ]

    # --- NEWLY ADDED ---
    GENDER_CHOICES = [
    ("", "Select gender"),
    ("Female", "Female"),
    ("Male", "Male"),
    ("Other", "Other"),
    ("Prefer not to say", "Prefer not to say"),
    ]

    full_name = models.CharField(max_length=100)

    official_email = models.EmailField(unique=True)

    country_code = models.CharField(max_length=5, default="+91")

    phone_number = models.CharField(max_length=10, unique=True)

    organization_name = models.CharField(max_length=150)

    department = models.CharField(max_length=100, blank=True, null=True)

    employee_id = models.CharField(max_length=30, unique=True)

    designation = models.CharField(
        max_length=20,
        choices=DESIGNATION_CHOICES,
        blank=True,
        null=True,
    )

    # --- NEWLY ADDED ---
    role = models.CharField(max_length=50, default="Training Coordinator")

    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )

    is_email_verified = models.BooleanField(default=False)

    is_mobile_verified = models.BooleanField(default=False)
    # -------------------

    password = models.CharField(max_length=255)

    registered_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name