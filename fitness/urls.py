from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
router.register(r'api/branches', views.GymBranchViewSet)
router.register(r'api/plans', views.MembershipPlanViewSet)
router.register(r'api/trainers', views.TrainerViewSet)
router.register(r'api/members', views.MemberViewSet)
router.register(r'api/payments', views.PaymentViewSet)
router.register(r'api/attendance', views.AttendanceViewSet)

urlpatterns = [
    # 0. Root / Home & Auth Routes
    path('', views.home_view, name='home'),  # സെർവർ തുറക്കുമ്പോൾ നേരെ ഹോം പേജിലേക്ക് വരാൻ
    path('login/', auth_views.LoginView.as_view(template_name='fitness/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 1. HTML List Views (ഡാറ്റ കാണാനുള്ള ലിങ്ക് പേജുകൾ)
    path('branches/', views.branch_list, name='branch_list'),
    path('plans/', views.plan_list, name='plan_list'),
    path('members/', views.member_list, name='member_list'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('payments/', views.payment_list, name='payment_list'),
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('member/dashboard/', views.member_dashboard, name='member_dashboard'),

    # 2. Add / Create Views (പുതിയ ഡാറ്റ ചേർക്കാനുള്ള ഫോമുകൾ)
    path('branch/add/', views.add_branch, name='add_branch'),
    path('branch/<int:branch_id>/members/', views.branch_member_list, name='branch_member_list'),
    path('branch/<int:branch_id>/trainers/', views.branch_trainer_list, name='branch_trainer_list'),
    path('branch/<int:branch_id>/attendance/', views.branch_attendance_list, name='branch_attendance_list'),
    path('plan/add/', views.add_plan, name='add_plan'),
    path('trainer/add/', views.add_trainer, name='add_trainer'),
    path('member/add/', views.add_member, name='add_member'),
    path('payment/add/', views.add_payment, name='add_payment'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),

    # 3. Update Views (ഡാറ്റ എഡിറ്റ് ചെയ്യാൻ)
    path('branch/update/<int:pk>/', views.update_branch, name='update_branch'),
    path('plan/update/<int:pk>/', views.update_plan, name='update_plan'),
    path('trainer/update/<int:pk>/', views.update_trainer, name='update_trainer'),
    path('member/update/<int:pk>/', views.update_member, name='update_member'),

    # 4. Delete Views (ഡാറ്റ ഡിലീറ്റ് ചെയ്യാൻ)
    path('branch/delete/<int:pk>/', views.delete_branch, name='delete_branch'),
    path('plan/delete/<int:pk>/', views.delete_plan, name='delete_plan'), # ആവശ്യമെങ്കിൽ plan_delete വ്യൂ കൂടി ശ്രദ്ധിക്കുക
    path('trainer/delete/<int:pk>/', views.delete_trainer, name='delete_trainer'),
    path('member/delete/<int:pk>/', views.delete_member, name='delete_member'),

    # 5. DRF API Routes (ഇത് താഴേക്ക് മാറ്റിയിരിക്കുന്നു, അതിനാൽ ഹോം പേജ് തടസ്സപ്പെടില്ല)
    path('', include(router.urls)),
    path('ai-chat/', views.gym_ai_chatbot, name='ai_chat'),
   
]