from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GymBranch, MembershipPlan, Member, Attendance,Payment,Trainer
from .forms import GymBranchForm,MembershipPlanForm,MemberForm,AttendanceForm,PaymentForm,TrainerForm
from rest_framework import viewsets
from .serializers import (
    GymBranchSerializer, MembershipPlanSerializer,
    TrainerSerializer, MemberSerializer,
    PaymentSerializer, AttendanceSerializer
)
from .models import GymBranch,MembershipPlan,Trainer,Member,Attendance,Payment,UserProfile


import os
import json
import requests

from django.http import JsonResponse

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def gym_ai_chatbot(request):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        }, status=405)

    try:
        if not GEMINI_API_KEY:
            return JsonResponse({
                "status": "error",
                "message": "Gemini API key is missing"
            }, status=500)

        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({
                "status": "error",
                "message": "Message cannot be empty"
            }, status=400)

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-3.8-flash:generateContent"
        )

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }

        payload = {
            "contents": [{
                "parts": [{
                    "text": (
                        "You are a helpful fitness assistant "
                        "for FitSync Gym. "
                        "Answer clearly and concisely: "
                        + user_message
                    )
                }]
            }]
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        result = response.json()

        print("Gemini API Response:", result)

        if not response.ok:
            error_message = result.get(
                "error", {}
            ).get("message", "Gemini API Error")

            return JsonResponse({
                "status": "error",
                "message": error_message
            }, status=response.status_code)

        candidates = result.get("candidates", [])

        if candidates:
            ai_reply = (
                candidates[0]["content"]["parts"][0]["text"]
            )

            return JsonResponse({
                "status": "success",
                "reply": ai_reply
            })

        return JsonResponse({
            "status": "error",
            "message": "No response received from Gemini"
        }, status=502)

    except Exception as e:

        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)



@login_required
def branch_list(request):
    branches = GymBranch.objects.all()
    return render(request, 'fitness/branch_list.html', {'branches': branches})



def branch_list(request):
    branches = GymBranch.objects.all()
    return render(request, 'fitness/branch_list.html', {'branches':branches})

def plan_list(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'fitness/plan_list.html', {'plans':plans})

def member_list(request):
    members = Member.objects.all()
    return render(request, 'fitness/member_list.html', {'members': members})

def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-check_in_time')
    return render(request, 'fitness/attendance_list.html', {'attendances': attendances})

def payment_list(request):
    payments = Payment.objects.all().order_by('-payment_date')
    return render(request, 'fitness/payment_list.html', {'payments':payments})

def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request,'fitness/trainer_list.html',{'trainers':trainers})


def add_branch(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')


    if request.method == 'POST':
        form = GymBranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trainer_list')
    else:
        form = GymBranchForm()
    return render(request,'fitness/add_branch.html', {'form':form})

from django.shortcuts import redirect

# 2. Membership Plan Add View
def add_plan(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')


    if request.method == 'POST':
        form = MembershipPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plan_list')
    else:
        form = MembershipPlanForm()
    return render(request, 'fitness/add_plan.html', {'form': form})

# 3. Trainer Add View
def add_trainer(request):
    if not request.user.is_superuser:
        return redirect('staff_dashboard')


    if request.method == 'POST':
        form = TrainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trainer_list')
    else:
        form = TrainerForm()
    return render(request, 'fitness/add_trainer.html', {'form': form})

# 4. Member Add View
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'fitness/add_member.html', {'form': form})

# 5. Payment Add View
def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'fitness/add_payment.html', {'form': form})

# 6. Attendance Add View
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'fitness/add_attendance.html', {'form': form})

from django.shortcuts import get_object_or_404

# --- 1. GYM BRANCH UPDATE & DELETE ---
def update_branch(request, pk):
    branch = get_object_or_404(GymBranch, pk=pk)
    if request.method == 'POST':
        form = GymBranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('branch_list')
    else:
        form = GymBranchForm(instance=branch)
    return render(request, 'fitness/add_branch.html', {'form': form})

def delete_branch(request, pk):
    branch = get_object_or_404(GymBranch, pk=pk)
    if request.method == 'POST':
        branch.delete()
        return redirect('branch_list')
    return render(request, 'fitness/confirm_delete.html', {'obj': branch})


# --- 2. MEMBERSHIP PLAN UPDATE & DELETE ---
def update_plan(request, pk):
    plan = get_object_or_404(MembershipPlan, pk=pk)
    if request.method == 'POST':
        form = MembershipPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('plan_list')
    else:
        form = MembershipPlanForm(instance=plan)
    return render(request, 'fitness/add_plan.html', {'form': form})

def delete_plan(request, pk):
    plan = get_object_or_404(MembershipPlan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        return redirect('plan_list')
    return render(request, 'fitness/confirm_delete.html', {'obj': plan})


# --- 3. TRAINER UPDATE & DELETE ---
def update_trainer(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    if request.method == 'POST':
        form = TrainerForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('trainer_list')
    else:
        form = TrainerForm(instance=trainer)
    return render(request, 'fitness/add_trainer.html', {'form': form})

def delete_trainer(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    if request.method == 'POST':
        trainer.delete()
        return redirect('trainer_list')
    return render(request, 'fitness/confirm_delete.html', {'obj': trainer})


# --- 4. MEMBER UPDATE & DELETE ---
def update_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'fitness/add_member.html', {'form': form})

def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('member_list')
    return render(request, 'fitness/confirm_delete.html', {'obj': member})

def branch_member_list(request, branch_id):
    branch = get_object_or_404(GymBranch, id=branch_id)
    members = Member.objects.filter(branch=branch)
    context = {
        'branch': branch,
        'members': members
    }
    return render(request, 'fitness/branch_member_list.html', context)

def branch_trainer_list(request, branch_id):
    branch = get_object_or_404(GymBranch, id=branch_id)
    trainers = Trainer.objects.filter(branch=branch)
    context = {
        'branch': branch,
        'trainers': trainers
    }
    return render(request, 'fitness/branch_trainer_list.html', context)

def branch_attendance_list(request, branch_id):
    branch = get_object_or_404(GymBranch, id=branch_id)
    attendances = Attendance.objects.filter(branch=branch)
    context = {'branch': branch, 'attendances': attendances}
    return render(request, 'fitness/branch_attendance_list.html', context)


def admin_dashboard(request):
    total_branches = GymBranch.objects.count()
    total_members = Member.objects.count()
    total_trainers = Trainer.objects.count()
    
    # റീസെന്റ് അറ്റൻഡൻസും പേയ്‌മെന്റുകളും (ഏറ്റവും പുതിയ 5 എണ്ണം വീതം)
    recent_attendances = Attendance.objects.order_by('-check_in_time')[:5]
    recent_payments = Payment.objects.order_by('-id')[:5]  # അല്ലെങ്കിൽ ഡേറ്റ് ഫീൽഡ് അനുസരിച്ച്
    
    context = {
        'total_branches': total_branches,
        'total_members': total_members,
        'total_trainers': total_trainers,
        'recent_attendances': recent_attendances,
        'recent_payments': recent_payments,
    }
    return render(request, 'fitness/admin_dashboard.html', context)


@login_required
def staff_dashboard(request):
    # യൂസർ സ്റ്റാഫ് ആണോ എന്ന് ചെക്ക് ചെയ്യാം
    try:
        profile = request.user.userprofile
        if profile.role != 'staff' and not request.user.is_superuser:
            return redirect('home') # അഡ്മിനോ സ്റ്റാഫോ അല്ലെങ്കില്‍ ഹോമിലേക്ക് വിടാം
        
        branch = profile.branch
    except UserProfile.DoesNotExist:
        branch = None

    context = {'branch': branch}
    return render(request, 'fitness/staff_dashboard.html', context)


@login_required
def member_dashboard(request):
    try:
        profile = request.user.userprofile
        if profile.role != 'member' and not request.user.is_superuser:
            return redirect('home')
    except UserProfile.DoesNotExist:
        return redirect('home')

    # ലോഗിൻ ചെയ്ത യൂസറുമായി ബന്ധിപ്പിച്ചിരിക്കുന്ന Member പ്രൊഫൈൽ എടുക്കുന്നു
    member = Member.objects.filter(user=request.user).first()
    
    if member:
        attendances = Attendance.objects.filter(member=member).order_by('-id')
        payments = Payment.objects.filter(member=member).order_by('-id')
    else:
        attendances = []
        payments = []

    context = {
        'member': member,
        'attendances': attendances,
        'payments': payments,
    }
    return render(request, 'fitness/member_dashboard.html', context)


class GymBranchViewSet(viewsets.ModelViewSet):
    queryset = GymBranch.objects.all()
    serializer_class = GymBranchSerializer

class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


@login_required
def home_view(request):
    # സൂപ്പർയൂസർ (Admin) ആണെങ്കിൽ നേരെ അഡ്മിൻ പേജിലേക്ക് (അല്ലെങ്കിൽ admin_dashboard-ലേക്ക്)
    if request.user.is_superuser:
        return render(request, 'fitness/home.html') # അല്ലെങ്കിൽ return redirect('admin_dashboard')

    # മറ്റ് യൂസർമാരുടെ റോൾ ചെക്ക് ചെയ്ത് അതത് ഡാഷ്‌ബോർഡിലേക്ക് വിടുന്നു
    try:
        profile = request.user.userprofile
        if profile.role == 'staff':
            return redirect('staff_dashboard')
        elif profile.role == 'trainer':
            return redirect('trainer_dashboard')
        elif profile.role == 'member':
            return redirect('member_dashboard')
    except UserProfile.DoesNotExist:
        pass

    return render(request, 'fitness/home.html')




