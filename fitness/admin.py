from django.contrib import admin
from .models import GymBranch, MembershipPlan,Member,Attendance,Payment,Trainer,UserProfile

admin.site.register(GymBranch)
admin.site.register(MembershipPlan)
admin.site.register(Member)
admin.site.register(Attendance)
admin.site.register(Payment)
admin.site.register(Trainer)
admin.site.register(UserProfile)

