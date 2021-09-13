from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# from django.contrib.auth.models import User,Group
from .models import Intity,People, Member,Region,Classification,Comment,NumVolunteer,Poster,CustomUser,Reply,Gender
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.db.models import Q # new
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.views.generic import TemplateView, ListView ,CreateView
from django.urls import reverse

# import json
# import requests
# # from .forms import AddMemberForm,IntitiesForm
# from django.urls import reverse
# # from .filters import IntityFilter
# from .decorators import notLoggedUsers,allowedUsers,IntityAdmins
# # from .forms import IntityForm
# # from .forms import UserUpdateForm, ProfileUpdateForm
# # from .forms import UserUpdateForm,ProfileUpdateForm

# # Create by using class based view replace function based view that provide Django
# # from django.views.generic import CreateView,UpdateView
# # from django.contrib.auth.mixins import LoginRequiredMixin


# # ========Views for User=================#
@login_required(login_url='doLogin')
def user_home(request):
    return render(request,"user_template/home_content.html")


@login_required(login_url='doLogin')
def Profile1(request):
    context = {
        'region': Region.objects.all(),
        'gender':Gender.objects.all(),
        'people':People.objects.all(),
        'title':'الملف الشخصي',
    }
    return render(request,'user_template/profile.html', context)


@login_required(login_url='do_login')
def ProfileUpdate(request,user_id):
    # return HttpResponse("Intity Id: "+str(user_id))
    user=People.objects.get(id=user_id)
    if user==None:
        return HttpResponse("Intity Not Found")
    else:
        # return render(request, "hod_template/edit_intities_template.html",{'intity': intity})
        return HttpResponseRedirect("/profile1")

          







@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def ProfileEdit(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        # user=CustomUser.objects.update()
        user=People.objects.get(id=request.POST.get('id',''))
        if user==None:
            return HttpResponse("<h2>People Not Found</h2>")
        else:       
            if request.FILES.get('profile'):
                file = request.FILES['profile']
                fs = FileSystemStorage()
                profile_pic = fs.save(file.name, file)
            else:
                    profile_pic=None
            if profile_pic!=None:  
                user.profile_pic= profile_pic
            user.username =request.POST.get('username','')
            user.email=request.POST.get('email','')
            user.phone=request.POST.get('phone','')
            user.region=request.POST.get('region','')
            user.birth=request.POST.get('birth','')
            user.gender=request.POST.get('gender','')
            user.employee=request.POST.get('employee','')
            user.password=request.POST.get('password','')
            user.save()
            messages.success(request,"Updated Successfully")
            return HttpResponseRedirect("profile_update1/"+str(user.id)+"")


@login_required(login_url='doLogin')
def Intities2(request):
    context = {
    'intitys' : Intity.objects.all(),
    'classifications': Classification.objects.all(),
    'regions': Region.objects.all(),
    # 'num_com': Comment.objects.filter().count(),
    'title':'المؤسسات'
    }
    return render(request, 'user_template/intities.html', context)



# @login_required(login_url='doLogin')
def More_Read_Intities(request):
    context = {
        'intitys' : Intity.objects.all(),
        'region': Region.objects.all(),
        'classification': Classification.objects.all(),
        'title':'معلومات المؤسسة'
    }
    return render(request, 'user_template/more_read_intities.html', context)


class SearchIntitiesResultsView1(ListView):
    model = Intity
    model = Region
    model = Classification
    template_name = 'user_template/search_intities_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Intity.objects.filter(
            Q(name__icontains=query) | Q(region__icontains=query) | Q(classification__icontains=query)
        )
        return object_list



@login_required(login_url='doLogin')  
def Details2(request):
    context = {
    'title':'قراءة المزيد',
    }
    return render(request, 'user_template/details.html', context)


@login_required(login_url='doLogin')
def Profile_Intities1(request):
    context = {
        'title':'معلومات المؤسسة'
    }
    return render(request,'user_template/profile_intities_template.html', context) 


@login_required(login_url='doLogin')
def Declaration1(request):
    context = {
        'posters': Poster.objects.all(),
        'regions': Region.objects.all(),
        'num_poster': Poster.objects.filter().count(),
        'classifications': Classification.objects.all(),
        'title':'الاعلانات',
    }
    return render(request, 'user_template/poster.html', context)

# # class SearchPosterEduResultsView(ListView):
# #     model = Poster
# #     template_name = 'hod_template/search_posterEdu_results.html'
# #     queryset = Poster.objects.filter(classification__icontains='تعليم') # new

# # class SearchPosterEnvResultsView(ListView):
# #     model = Poster
# #     template_name = 'hod_template/search_posterEnv_results.html'
# #     queryset = Poster.objects.filter(classification__icontains='بيئي') # new

# # class SearchPosterHeaResultsView(ListView):
# #     model = Poster
# #     template_name = 'hod_template/search_posterHea_results.html'
# #     queryset = Poster.objects.filter(classification__icontains='صحي') # new

# # class SearchPosterArtResultsView(ListView):
# #     model = Poster
# #     template_name = 'hod_template/search_posterArt_results.html'
# #     queryset = Poster.objects.filter(classification__icontains='فنون') # new

# # class SearchPosterOthResultsView(ListView):
# #     model = Poster
# #     template_name = 'hod_template/search_posterOth_results.html'
# #     queryset = Poster.objects.filter(classification__icontains='أخرى') # new


class SearchPosterEduResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterEdu_results1.html'
    queryset = Poster.objects.filter(classification__icontains='تعليم') # new


class SearchPosterEnvResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterEnv_results1.html'
    queryset = Poster.objects.filter(classification__icontains='بيئة') # new


class SearchPosterHeaResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterHea_results1.html'
    queryset = Poster.objects.filter(classification__icontains='صحي') # new


class SearchPosterArtResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterArt_results1.html'
    queryset = Poster.objects.filter(classification__icontains='فنون') # new


class SearchPosterOthResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterOth_results1.html'
    queryset = Poster.objects.filter(classification__icontains='أخرى') # new



@login_required(login_url='doLogin')
def Add_Notification(request):
    context = {
    'numvolunteers': NumVolunteer.objects.all(),
    'region': Region.objects.all(),
    'gender':Gender.objects.all(),
    'title':'ارسال اشعار للمؤسسة للتطوع'
    }
    return render(request, 'user_template/add_notification.html', context)



@login_required(login_url='doLogin')
def Send_Notification(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        volunteer_img=fs.save(file.name,file)
        try:
            region=Region.objects.get(id=request.POST.get('region',''))
            numvolunteer=NumVolunteer(name=request.POST.get('name',''),age=request.POST.get('age',''),gender=request.POST.get('gender',''),employee=request.POST.get('employee',''),volunteer_image=volunteer_img,region=region)
            numvolunteer.save()
            messages.success(request,"Added Successfully")
        except Exception as e:
            print(e)
            messages.error(request,"فشل في ارسال الاشعار")
        return HttpResponseRedirect("/add_notification")





@login_required(login_url='doLogin')
def comments1(request):
    comments = Comment.objects.all()
    paginator = Paginator(comments, 4)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_page) 
    context = {
        'comments' : comments,
        'num_com': Comment.objects.filter().count(),
        # 'total_likes': total_likes,
        'page': page,
        'title':'التعليقات',
    }
    return render(request, 'user_template/comments.html', context)

@login_required(login_url='doLogin')
def LikeView1(request,pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('comments1'))

   







@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def Add_Comment_Save_User(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        com = Comment(comm_name=request.POST.get('comm_name',''),author=request.user,body=request.POST.get('body',''))
        com.save()
        return redirect("/comments1")

@login_required(login_url='doLogin')
def About2(request):
    context = {
    'title':'من نحن',
    }
    return render(request, 'user_template/about.html', context)









































      

 












