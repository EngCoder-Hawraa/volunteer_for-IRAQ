# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import *
from iraq.models import CustomUser


class UserModel(UserAdmin):
    pass

# class IntityAdmin(admin.ModelAdmin):
#     list_display = ("region", "classification","name",) 
    
admin.site.register(CustomUser,UserModel)
admin.site.register(AdminHOD)
# admin.site.register(Staff)
admin.site.register(Intity)
admin.site.register(Region)
admin.site.register(Gender)
admin.site.register(Classification)
admin.site.register(People)
admin.site.register(Member)
admin.site.register(Poster)
admin.site.register(NumVolunteer)
admin.site.register(Comment)
admin.site.register(Reply)
# admin.site.register(Profile)
# admin.site.register(AttendanceReport)
# admin.site.register(LeaveReportStudent)
# admin.site.register(LeaveReportStaff)
# admin.site.register(FeedBackStudent)




# from django.contrib import admin
# # from iraq.models import Intity, Region, Classification, Member
# from django.contrib.auth.admin import UserAdmin
# from .models import *





# class PosterAdmin(admin.ModelAdmin):
#     list_display = ("name","classification")

# admin.site.register(Intity,IntityAdmin)
# admin.site.register(Region)
# admin.site.register(Classification)
# admin.site.register(Member)
# admin.site.register(Poster,PosterAdmin)
# admin.site.register(NumVolunteer)
# admin.site.register(Comment)
# admin.site.register(Like)
# admin.site.register(Profile)
# admin.site.register(CustomUser)
# admin.site.register(AdminHOD)
# admin.site.register(Staffs)
# # class UserModel(UserAdmin):
# #     pass

# # admin.site.register(CustomUser,UserModel)

# # Register your models here.
