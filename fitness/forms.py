from django import forms
from .models import GymBranch, MembershipPlan, Trainer, Member, Payment, Trainer,Attendance


class GymBranchForm(forms.ModelForm):
    class Meta:
        model = GymBranch
        fields = ['name', 'location', 'contact_number']

class MembershipPlanForm(forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ['name', 'duration_days', 'price']

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'phone', 'specialization', 'branch']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'phone', 'branch', 'plan', 'trainer', 'start_date','expiry_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['member', 'branch']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['member', 'amount', 'payment_date',  'status', 'method']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type':'date', 'class': 'form-control'}),
        }