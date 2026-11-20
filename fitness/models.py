from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError




class GymBranch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.location})"


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Gym Admin'),
        ('staff', 'Branch Staff / Receptionist'),
        ('trainer', 'Trainer'),
        ('member', 'Member'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    branch = models.ForeignKey(GymBranch, on_delete=models.SET_NULL, null=True, blank=True) 
    



class MembershipPlan(models.Model):
    name = models.CharField(max_length=50)
    duration_days = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} - Rs.{self.price}"


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    branch = models.ForeignKey(GymBranch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.specialization})"
        




class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, default='default Name')
    phone = models.CharField(max_length=15, blank=True, null=True)
    branch = models.ForeignKey(GymBranch, on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    # Core Business Logic: Expiry date check cheythu status update cheyyunnu
    def check_membership_status(self):
        if self.expiry_date and self.expiry_date < timezone.now().date():
            if self.is_active:
                self.is_active = False
                self.save()
        return self.is_active


class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    branch = models.ForeignKey(GymBranch, on_delete=models.CASCADE, null=True, blank=True)
    check_in_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validation: Expired aaya member-nu check-in block cheyyum
        if not self.member.check_membership_status():
            raise ValidationError(f"Check-in Denied! Membership expired for {self.member.user.username}.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.member and self.member.user:
            username = self.member.user.username
        else:
            username = "Unknown Member"

        return f"{username} checked in at {self.check_in_time.strftime('%Y-%m-%d %H:%M')}"


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)

    PAYMENT_STATUS = (
        ('paid', 'paid'),
        ('pending','pending'),
        ('overdue', 'overdue'),

    )
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

    PAYMENT_METHOD = (
        ('UPI', 'UPI'),
        ('cash', 'cash'),
        ('card', 'card'),

    )
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='UPI')

    def __str__(self):
        return f"{self.member.name} - {self.amount} ({self.status})"

