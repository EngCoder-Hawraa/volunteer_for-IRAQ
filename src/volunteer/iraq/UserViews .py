from django.shortcuts import render, redirect

@login_required(login_url='login_user')
def user_home(request):
    return render(request,"user_template/home_content.html")