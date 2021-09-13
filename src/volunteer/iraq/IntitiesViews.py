from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# from django.contrib.auth.models import User,Group
from .models import Intity,AdminHOD,Member,Region,Classification,Comment,NumVolunteer,Poster,CustomUser,Reply,Gender
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








# # ========Views for Admin=================#

def dashboard(request):
    context = {
    'title':'معلومات المؤسسة',
    }
    return render(request, 'hod_template/dashboard.html', context)


@login_required(login_url='doLogin')
def admin_home(request):
    context = {
        # 'profiles': Profile.objects.all(),
    }
    return render(request,"hod_template/home_content.html",context)


@login_required(login_url='doLogin')
def Profile(request):
    context = {
        'region': Region.objects.all(),
        'gender':Gender.objects.all(),
        'admin': AdminHOD.objects.all(),
        'title':'الملف الشخصي',
    }
    return render(request,'hod_template/profile.html', context)


@login_required(login_url='do_login')
def ProfileUpdate(request,user_id):
    # return HttpResponse("Intity Id: "+str(user_id))
    user=AdminHOD.objects.get(id=user_id)
    if user==None:
        return HttpResponse("Intity Not Found")
    else:
        # return render(request, "hod_template/edit_intities_template.html",{'intity': intity})
        return HttpResponseRedirect("/profile")

          







@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def ProfileEdit(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        # user=CustomUser.objects.update()
        user=AdminHOD.objects.get(id=request.POST.get('id',''))
        if user==None:
            return HttpResponse("<h2>Staff Not Found</h2>")
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
            return HttpResponseRedirect("profile_update/"+str(user.id)+"")





@login_required(login_url='doLogin')
def Intities(request):
    context = {
        'intitys' : Intity.objects.all(),
        'region': Region.objects.all(),
        'classification': Classification.objects.all(),

        # 'myFilter': searchFilter,
        'title':'المؤسسات'
    }
    return render(request, 'hod_template/intities.html', context)


@login_required(login_url='doLogin')
def ViewImageP(request):
    context = {
        'intitys' : Intity.objects.all(),
        'title':'الترخيص'
    }
    return render(request, 'hod_template/permission.html', context)


# @login_required(login_url='doLogin')
def More_Read_Intities(request):
    context = {
        'intitys' : Intity.objects.all(),
        'region': Region.objects.all(),
        'classification': Classification.objects.all(),
        'title':'معلومات المؤسسة'
    }
    return render(request, 'hod_template/more_read_intities.html', context)




@login_required(login_url='doLogin')
# # @allowedUsers(allowedGroups=['intityAdmin'])
def Profile_Intities(request):
    context = {
        'title':'معلومات المؤسسة',
        'intitys': Intity.objects.all(),
        'region': Region.objects.all(),
        # 'users': Intity.objects.filter(user=request.abstrs),
        'classification': Classification.objects.all(),
    }
    return render(request,"hod_template/profile_intities_template.html", context)  



# # # Create by using class based view replace function based view that provide Django
# # @login_required(login_url='login_intities')
# # # # @allowedUsers(allowedGroups=['intityAdmin'])
# # class IntitiesCreateView(CreateView):
# #     model=Intity
# #     fields = ['user','name','region','intities_pic','created','classification','works','abstract','permission']
# #     template_name = 'hod_template/add_intities_template.html'


@login_required(login_url='login_intities')
# @allowedUsers(allowedGroups=['intityAdmin'])
def Add_Intities_Save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile1']
        fs=FileSystemStorage()
        intities_picture=fs.save(file.name,file)
        file=request.FILES['profile2']
        fs=FileSystemStorage()
        permission=fs.save(file.name,file)
        try:
            region=Region.objects.get(id=request.POST.get('region',''))
            classification=Classification.objects.get(id=request.POST.get('classification',''))
            intity=Intity(admin=request.user,name=request.POST.get('name',''),created=request.POST.get('created',''),works=request.POST.get('works',''),abstract=request.POST.get('abstract',''),intities_pic=intities_picture,region=region,classification=classification,permission=permission)
            intity.save()
            messages.success(request,"Added Successfully")
        except Exception as e:
            print(e)
            messages.error(request,"Failed to Add Intities")
        return HttpResponseRedirect("/profile_intities")



# # # Create by using class based view replace function based view that provide Django
# # @login_required(login_url='login_intities')
# # # # # @allowedUsers(allowedGroups=['intityAdmin'])
# # class IntitiesUpdateView(LoginRequiredMixin,UpdateView):
# #     model=Intity
# #     fields = ['user','name','region','intities_pic','created','classification','works','abstract','permission']


# # @login_required(login_url='login_intities')
# # @allowedUsers(allowedGroups=['intityAdmin'])
def delete_intities(request, intity_id):
    intity=Intity.objects.get(id=intity_id)
    intity.delete()
    messages.error(request, "Deleted Successfully")
    return HttpResponseRedirect("/profile_intities") 



 

@login_required(login_url='login_intities')
def Update_Intities(request,intity_id):
    # return HttpResponse("Intity Id: "+str(intity_id))
    intity=Intity.objects.get(id=intity_id)
    if intity==None:
        return HttpResponse("Intity Not Found")
    else:
        # return render(request, "hod_template/edit_intities_template.html",{'intity': intity})
        return HttpResponseRedirect("/profile_intities")







 
          


@login_required(login_url='login_intities')
# @allowedUsers(allowedGroups=['intityAdmin'])
def Edit_Intities_Save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        intity=Intity.objects.get(id=request.POST.get('id',''))
        if intity==None:
            return HttpResponse("<h2>Intity Not Found</h2>")
        else:       
            if request.FILES.get('profile1') and request.FILES.get('profile2'):
                file = request.FILES['profile1']
                fs = FileSystemStorage()
                intities_pic = fs.save(file.name, file)
                file1 = request.FILES['profile2']
                fs = FileSystemStorage()
                permission = fs.save(file1.name, file1)
            else:
                intities_pic=None
                permission=None
            if (intities_pic!=None and permission!=None):   
                intity.intities_picture = intities_pic
                intity.permission=permission
            User =request.POST.get('user','')
            intity.name=request.POST.get('name','')
            intity.created=request.POST.get('created','')
            intity.works=request.POST.get('works','')
            intity.abstract=request.POST.get('abstract','')
            intity.save()
            messages.success(request,"Updated Successfully")
            return HttpResponseRedirect("update_intities/"+str(intity.id)+"")
 
      
          


class SearchIntitiesResultsView(ListView):
    model = Intity
    model = Region
    model = Classification
    template_name = 'hod_template/search_intities_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Intity.objects.filter(
            Q(name__icontains=query) | Q(region__icontains=query) | Q(classification__icontains=query)
        )
        return object_list








@login_required(login_url='doLogin')  
def Details(request):
    context = {
    'title':'قراءة المزيد',
    }
    return render(request, 'hod_template/details.html', context)


 
@login_required(login_url='doLogin')
def comments(request):
    comments = Comment.objects.all()
    # stuff = get_object_or_404(Comment, id=['pk'])
    # total_likes = stuff.total_likes()
    reply = Reply.objects.all()
    paginator = Paginator(comments, 4)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_page)
    context = {
        # 'Profile': Profile.objects.all(),
        'comments' : comments,
        'intitys': Intity.objects.all(),
        'num_com': Comment.objects.filter().count(),
        # 'total_likes': total_likes,
        'page': page,
        'title':'التعليقات',
    }
    return render(request, 'hod_template/comments.html', context)








@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def Add_Comment_Save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        com = Comment(comm_name=request.POST.get('comm_name',''),author=request.user,body=request.POST.get('body',''))
        com.save()
        return redirect("/comments")



@login_required(login_url='doLogin')
def LikeView(request,pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('comments'))



@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def ComReply(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        # comment_name=Comment.objects.get(id=request.POST.get('comm_name',''))
        comment_name=Comment(comm_name=request.POST.get('comm_name',''))
        rep = Reply(comment_name=comment_name,author=request.user,reply_body=request.POST.get('body',''))
        rep.save()
        return redirect("/comments")
        # comment=Comment.objects.get(id=request.POST.get('comment',''))
        # comm_name=Comment(request.POST.get('comm_name','')),
        # comm_name = Comment(request.POST.get('comment',''))
        # comment_name=Comment.objects.get(id=request.POST.get('comment',''))
        # rep = Reply(comment=comment,reply_body=request.POST.get('reply_body',''),author=request.user)
        # rep.save()
        # return redirect("/comments")







@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def delete_comment(request,comment_id):
    comment=Comment.objects.get(id=comment_id)
    comment.delete()
    messages.error(request, "Deleted Successfully")
    return HttpResponseRedirect("/comments")  
    # return HttpResponse("Comment Id "+str(pk))






@login_required(login_url='doLogin')
# # @allowedUsers(allowedGroups=['intityAdmin'])
def Manage_Members(request):
    members = Member.objects.all()
    paginator = Paginator(members, 6)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_page)
    context = {
        'members': members ,
        'region': Region.objects.all(),
        'gender': Gender.objects.all(),
        'page': page,
        'title':'الاعضاء'
        # 'form':form
    }
    return render(request,"hod_template/manage_member.html", context)




@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def Add_Member_Save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        member_img=fs.save(file.name,file)
        try:
            region=Region.objects.get(id=request.POST.get('region',''))
            gender=Gender.objects.get(id=request.POST.get('gender',''))
            member=Member(name=request.POST.get('name',''),employee=request.POST.get('employee',''),phone=request.POST.get('phone',''),email=request.POST.get('email',''),member_image=member_img,region=region,gender=gender)
            member.save()
            messages.success(request,"Added Successfully")
        except Exception as e:
            print(e)
            messages.error(request,"Failed to Add Student")
        return HttpResponseRedirect("/manage_members")


@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def delete_member(request,member_id):
    member=Member.objects.get(id=member_id)
    member.delete()
    messages.error(request, "Deleted Successfully")
    return HttpResponseRedirect("/manage_members",{'member':member})


@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def update_member(request,member_id):
    member=Member.objects.get(id=member_id)
    if member==None:
        return HttpResponse("Member Not Found")
    else:
        return HttpResponseRedirect("/manage_members")



@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def edit_member(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        member=Member.objects.get(id=request.POST.get('id',''))
        if member==None:
            return HttpResponse("<h2>Member Not Found</h2>")
        else:
            if request.FILES.get('profile')!=None:
                file = request.FILES['profile']
                fs = FileSystemStorage()
                member_img = fs.save(file.name, file)
            else:
                member_img=None

            if member_img!=None:
                member.member_image=member_img
            member.name=request.POST.get('name','')
            member.gender=request.POST.get('gender','')
            member.employee=request.POST.get('employee','')
            member.phone=request.POST.get('phone','')
            member.email=request.POST.get('email','')
            member.save()

            messages.success(request,"Updated Successfully")
            return HttpResponseRedirect("update_member/"+str(member.id)+"")



@login_required(login_url='doLogin')
def Declaration(request):
    context = {
        'posters': Poster.objects.all(),
        'regions': Region.objects.all(),
        'num_poster': Poster.objects.filter().count(),
        'classifications': Classification.objects.all(),
        'title':'الاعلانات',
    }
    return render(request, 'hod_template/poster.html', context)


@login_required(login_url='doLogin')   
# @allowedUsers(allowedGroups=['intityAdmin'])
def Save_Poster(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        poster_img=fs.save(file.name,file)
        try:
            region=Region.objects.get(id=request.POST.get('region',''))
            classification=Classification.objects.get(id=request.POST.get('classification',''))
            poster = Poster(name=request.POST.get('name',''),place=request.POST.get('place',''),posts=request.POST.get('posts',''),date_poster=request.POST.get('date_poster',''),poster_image=poster_img,region=region, classification=classification)
            poster.save() 
            messages.success(request,"Added Successfully")
        except Exception as e:
            print(e)
            messages.error(request,"Failed to Add Student")
        return HttpResponseRedirect("/poster")

@login_required(login_url='doLogin')
def update_poster(request,poster_id):
    poster=Poster.objects.get(id=poster_id)
    if poster==None:
        return HttpResponse("Member Not Found")
    else:
        return HttpResponseRedirect("/poster")



@login_required(login_url='doLogin')
def edit_poster(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        poster=Poster.objects.get(id=request.POST.get('id',''))
        if poster==None:
            return HttpResponse("<h2>Poster Not Found</h2>")
        else:
            if request.FILES.get('profile')!=None:
                file = request.FILES['profile']
                fs = FileSystemStorage()
                poster_img = fs.save(file.name, file)
            else:
                poster_img=None

            if poster_img!=None:
                poster.poster_image=poster_img
            poster.name=request.POST.get('name','')
            # poster.region=request.POST.get('region','')
            poster.place=request.POST.get('place','')
            # poster.classification=request.POST.get('classification','')
            poster.posts=request.POST.get('posts','')
            poster.date_poster=request.POST.get('date_poster','')
            poster.time_poster=request.POST.get('time_poster','')
            poster.save()
            messages.success(request,"Updated Successfully")
            return HttpResponseRedirect("update_poster/"+str(poster.id)+"")        
                

@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def DeletePoster(request,poster_id):
    poster=Poster.objects.get(id=poster_id)
    poster.delete()
    messages.error(request, "Deleted Successfully")
    return HttpResponseRedirect("/poster")
 


class SearchPosterEduResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterEdu_results.html'
    queryset = Poster.objects.filter(classification__icontains='تعليم') # new

class SearchPosterEnvResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterEnv_results.html'
    queryset = Poster.objects.filter(classification__icontains='بيئة') # new

class SearchPosterHeaResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterHea_results.html'
    queryset = Poster.objects.filter(classification__icontains='صحة') # new

class SearchPosterArtResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterArt_results.html'
    queryset = Poster.objects.filter(classification__icontains='فنون') # new

class SearchPosterOthResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterOth_results.html'
    queryset = Poster.objects.filter(classification__icontains='أخرى') # new









  

@login_required(login_url='doLogin')
def Notification(request):
    numvolunteers = NumVolunteer.objects.all()
    paginator = Paginator(numvolunteers, 1)
    page = request.GET.get('page')
    try:
        numvolunteers = paginator.page(page)
    except PageNotAnInteger:
        numvolunteers = paginator.page(1)
    except EmptyPage:
        numvolunteers = paginator.page(paginator.num_page)
    context = {
        'num_volunteer':NumVolunteer.objects.filter().count(),
        'region': Region.objects.all(),
        'gender':Gender.objects.all(),
        'numvolunteers': numvolunteers,
        'page': page,
        'title':'الاشعارات'
    }
    return render(request, 'hod_template/notification.html', context)




@login_required(login_url='doLogin')
# @IntityAdmins
# @allowedUsers(allowedGroups=['intityAdmin'])
def AddVolunteer(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        volunteer_img=fs.save(file.name,file)
        try:
            region=Region.objects.get(id=request.POST.get('region',''))
            gender=Gender.objects.get(id=request.POST.get('gender',''))
            numvolunteer=NumVolunteer(name=request.POST.get('name',''),age=request.POST.get('age',''),employee=request.POST.get('employee',''),volunteer_image=volunteer_img,region=region,gender=gender)
            numvolunteer.save()
            messages.success(request,"Added Successfully")
        except Exception as e:
            print(e)
            messages.error(request,"فشل في ارسال الاشعار")
        return HttpResponseRedirect("/notification")



@login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
def DeleteVolunteer(request,notification_id):
    notification=NumVolunteer.objects.get(id=notification_id)
    notification.delete()
    messages.error(request, "Deleted Successfully")
    return HttpResponseRedirect("/notification")





   


@login_required(login_url='doLogin')
def About(request):
    context = {
    'title':'من نحن',
    }
    return render(request, 'hod_template/about.html', context)



