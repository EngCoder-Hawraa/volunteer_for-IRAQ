from django import forms
from .models import CustomUser
# from django.contrib.auth.forms import UserCreationForm
from .models import Intity, Member,Region, Classification
from django.forms import ModelForm

# class IntityForm(ModelForm):
#     class Meta:
#         model = Intity
#         fields ="__all__"




class CreateNewUser(forms.Form):
    username = forms.CharField(label='اسم المستخدم', max_length=255,help_text='اسم المستخدم يجب الا يحتوي على مسافات' ,
                        widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
    email = forms.EmailField(label='البريد الإلكتروني',
                        widget= forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password1 = forms.CharField(label='كلمة المرور',help_text='يجب الايقل عن ثمانية',
                        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), min_length=8,required=True)
    password2 = forms.CharField(label='تأكيد كلمة المرور', 
                        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), min_length=8,required=True)
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = CustomUser.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError('يوجد مستخدم مسجل بهذا الاسم.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = CustomUser.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError('هذا الايميل مسجل مسبقا')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('كلمة المرور غير متطابقة')

    class Meta:
            model = CustomUser
            fields = ('username', 'email', 'password1', 'password2')

    
    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password1'] != cd['password2']:
    #         raise forms.ValidationError('كلمة المرور غير متطابقة')
    #     return cd['password2']

    # def clean_username(self):
    #     cd = self.cleaned_data
    #     if CustomUser.objects.filter(username=cd['username']).exists():
    #         raise forms.ValidationError('يوجد مستخدم مسجل بهذا الاسم.')
    #     return cd['username']
    # class Meta:
    #     model = CustomUser
    #     fields = ('username', 'email', 'password1', 'password2')
    




# class UserUpdateForm(forms.ModelForm):
#     # username = forms.CharField(label='اسم المستخدم', max_length=255,help_text='اسم المستخدم يجب الا يحتوي على مسافات' ,
#     #                 widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
#     # email = forms.EmailField(label='البريد الإلكتروني',
#     #                         widget= forms.TextInput(attrs={'class': 'form-control mb-3'}))      
#     class Meta:
#         model = User
#         fields = ('username','email')

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('profile_img',)


    


# class AddMemberForm(forms.Form):
#     gender_choice=(
#         ("Male","ذكر"),
#         ("Female","انثى")
#     )
#     name=forms.CharField(label='اسم العضو',max_length=255,required=True, widget= forms.TextInput(attrs={'class': 'form-control mb-3'}))
#     gender=forms.ChoiceField(label='الجنس',choices=gender_choice,required=True,widget=forms.Select(attrs={"class":"form-control  mb-3"}))
#     regions=Region.objects.all()
#     regions_list=[]
#     for region in regions:
#         small_region=(region.id,region.region_name)
#         regions_list.append(small_region)
        
        
#     region=forms.ChoiceField(label='المحافظة',choices=regions_list,widget=forms.Select(attrs={'class':'form-control mb-3 .float-right'}))
#     employee=forms.CharField(label='الوظيفة', widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
#     phone=forms.CharField(label='رقم الهاتف',max_length=255,widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
#     email=forms.EmailField(label='البريد الالكتروني',max_length=255, widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
#     member_image=forms.FileField(label='صورة العضو',widget=forms.FileInput(attrs={'class':'form-control mb-3'}))

  



