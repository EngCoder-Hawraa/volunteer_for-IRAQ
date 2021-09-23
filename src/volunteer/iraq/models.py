
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import SlugField
from django.db.models.signals import post_save
from django.utils.text import slugify
import uuid
from django.dispatch import receiver
from django.urls import reverse
#import image from pillow desktop
from PIL import Image
from django.template.defaultfilters import date, slugify, title

# Create your models here.


class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"people"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)






def user_directory_path(instance, filename):
    # this file will be uploaded to MEDIA_ROOT /user(id)/filename
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)
    class meta:
        verbose_name = 'Tag'
        verbose_name_plural ='Tags'

    def get_absolute_url(self):
        return reverse("tags", org=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=False)
    caption = models.TextField(max_length=1500, verbose_name='Caption', )
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    likes = models.IntegerField()

    def get_absolute_url(self):
        return reverse("post_details", args=[str(self.id)])


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')

class Stream(models.Model):
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower,date=post.posted, following=user)
            stream.save()

post_save.connect(Stream.add_post, sender=Post) 



    




class Gender(models.Model):
    MALE = 'ذكر'
    FEMALE = 'انثى'
    gender = [
        (MALE, 'ذكر'),
        (FEMALE, 'انثى'),
    ]
    gender = models.CharField(max_length=255,choices= gender,default=MALE)
    def __str__(self):
        return self.gender


class Classification(models.Model):
    Ed = 'تعليم'
    Ev = 'بيئة'
    H = 'صحة'
    A = 'فنون'
    O = 'أخرى'
    classification = [
        (Ed , 'تعليم'),(Ev , 'بيئة'),(H, 'صحة'),(A, 'فنون'),(O, 'أخرى')
    ]
    classification = models.CharField(
        max_length=255,choices= classification,default= Ed)
    def __str__(self):
        return self.classification


class Region(models.Model):
    E = 'اربيل'
    AN = 'الانبار'
    BA = 'بابل'
    B = 'بغداد'
    Bs = 'البصرة'
    Du = 'دهوك'
    Q = 'القادسية'
    D = 'ديالى'
    Dh = 'ذي قار'
    S ='السليمانية'
    Sa ='صلاح الدين'
    K ='كركوك'
    Ka ='كربلاء'
    Mu ='المثنى'
    M ='ميسان'
    Na ='النجف'
    N ='نينوى'
    W ='واسط'
    region = [
        (E,'Erbil' ),(AN, 'Al-Anbar'),(BA, 'Babil'),(B, 'Baghdad'),
        (Bs, 'Basrah'),(Du, 'Dohuk'),(Q, 'Al-Qadisyah'),(D, 'Diyala'),
        (Dh,'Dhi Qar'),(S,'Sulymaniah'),(Sa, 'Salah Din'),(K, 'Kirkuk'),
        (Ka, 'Karbala'),(Mu,'Muthana'),(M, 'Maysan'),(Na,'Najaf'),
        (N, 'Nineveh'),(W, 'Wasit')
    ]
    region = models.CharField(
        max_length=255,choices= region,default=E)
    def __str__(self):
        return self.region


class AdminHOD(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    phone=models.CharField(max_length=255,null=True)
    birth=models.DateField(max_length=255, null=True, default="1994-10-07",blank=True)
    facebook=models.URLField(max_length=255,default='https://www.facebook.com/')
    gender=models.CharField(max_length=255, null=True)
    employee=models.CharField(max_length=255, null=True)
    region=models.CharField(max_length=255,null=True)
    profile_pic=models.ImageField(default='default.jpg', upload_to='profile_pics')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        profile_pic =Image.open(self.profile_pic.path)
        if profile_pic.width > 300 or profile_pic.height > 300:
            output_size =(300, 300)
            profile_pic.thumbnail(output_size)
            profile_pic.save(self.profile_pic.path)


    


class People(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    phone=models.CharField(max_length=255,null=True)
    birth=models.DateField(max_length=255, null=True, default="1994-10-07")
    facebook=models.URLField(max_length=255,default='https://www.facebook.com/')
    gender=models.CharField(max_length=255, null=True)
    employee=models.CharField(max_length=255, null=True)
    region=models.CharField(max_length=255,null=True)
    profile_pic=models.ImageField(default='default.jpg', upload_to='profile_pics')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        profile_pic =Image.open(self.profile_pic.path)
        if profile_pic.width > 300 or profile_pic.height > 300:
            output_size =(300, 300)
            profile_pic.thumbnail(output_size)
            profile_pic.save(self.profile_pic.path)





@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance,phone="",birth="1994-10-07",gender="",employee="",region="",fcm_token="")
        if instance.user_type==2:
            People.objects.create(admin=instance,fcm_token="",gender="",employee="",region="",birth="1994-10-07")


@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type ==1:
        instance.adminhod.save()
    if instance.user_type ==2:
        instance.people.save()
    # if instance.user_type==2:
    #     instance.intity.save()
    # if instance.user_type ==3:
    #     instance.people.save()





class Intity(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,null=True)
    region=models.CharField(max_length=255,null=False)
    created=models.DateField(null=False)
    classification=models.CharField(max_length=255,null=False)
    works=models.TextField(default="",null=False)
    abstract=models.TextField(default="",null=False)
    intities_pic=models.FileField(upload_to='images',null=False) 
    permission=models.FileField(upload_to='images',null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    class Meta:
      verbose_name_plural = "intities"
    def __str__(self):
        return self.name




class Member(models.Model):
    name=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    region=models.ForeignKey(Region,on_delete=models.CASCADE)
    employee=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    email=models.EmailField()
    member_image=models.FileField(null=True,blank=True,upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
   
   
class Poster(models.Model):
    # admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    region=models.ForeignKey(Region,on_delete=models.CASCADE)
    place=models.CharField(max_length=255)
    classification=models.CharField(max_length=255)
    posts=models.CharField(max_length=1000)
    # no_Intity=models.AutoField(primary_key=True)
    poster_image=models.FileField(null=True,blank=True,upload_to='images')
    date_poster=models.DateField()
    # time_poster=models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    class Meta:
      verbose_name_plural = "posters"

    # def __str__(self):
    #     return self.admin

class NumVolunteer(models.Model):
    name=models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True)
    # age=models.IntegerField()
    gender=models.CharField(max_length=255)
    region=models.ForeignKey(Region,on_delete=models.CASCADE)
    employee=models.CharField(max_length=255)
    volunteer_image=models.FileField(null=True,blank=True,upload_to='images')
    date_Volunteer = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.name

class Comment(models.Model):
    # intity_name = models.ForeignKey(Intity,null=True, on_delete=models.CASCADE,related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    # comment_pic=models.ForeignKey(AdminHOD,on_delete=models.CASCADE)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    likes = models.ManyToManyField(CustomUser, related_name='blog_comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    @property
    def total_like(self):
        return self.likes.all.count()


    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name + ' | ' + str(self.author)

    class Meta:
        ordering = ['created_at']

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)


















# class Profile(models.Model):
#     # name=models.CharField(max_length=255,null=True)
#     # id=models.AutoField(primary_key=True)
#     # user=models.OneToOneField(CustomUser,null=True,on_delete=models.CASCADE)
#     # bio=models.TextField()
#     profile_img=models.ImageField(default='default.jpg', upload_to='profile_pics')
#     # email=models.EmailField()
#     def __str__(self):
#         return '{} profile.'.format(self.user)



#     def save(self,*args, **kwargs):
#         super().save(*args, **kwargs)
#         img = Image.open(self.profile_img.path)
#         if img.width > 300 or img.height > 300:
#             output_size =(300, 300)
#             img.thumbnail(output_size)
#             img.save(self.profile_img.path)


# def create_profile(sender,**kwarg):
#     if kwarg['created']:
#        user_profile = Profile.objects.create(user=kwarg['instance'])

# post_save.connect(create_profile, sender=CustomUser)




# class Action(models.Model):
#     admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='actions')
#     liked = models.BooleanField(null=True)

#     class Meta:
#         unique_together = ['admin','comment']




# class Profile(models.Model):
#     # name=models.CharField(max_length=255,null=True)
#     id=models.AutoField(primary_key=True)
#     profile_img=models.ImageField(default='default.jpg', upload_to='profile_pics')
#     user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
#     email=models.EmailField()
#     def __str__(self):
#         return '{} profile.'.format(self.user)



#     def save(self,*args, **kwargs):
#         super().save(*args, **kwargs)
#         img = Image.open(self.profile_img.path)
#         if img.width > 300 or img.height > 300:
#             output_size =(300, 300)
#             img.thumbnail(output_size)
#             img.save(self.profile_img.path)


# def create_profile(sender,**kwarg):
#     if kwarg['created']:
#        user_profile = Profile.objects.create(user=kwarg['instance'])

# post_save.connect(create_profile, sender=User)



# class Comment(models.Model):
#     user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
#     message = models.TextField('Message')
#     date_comment = models.DateTimeField(auto_now=True, auto_now_add=False)

    

# class Like(models.Model):
#     like = models.ManyToManyField('Comment',blank=True,related_name='likes')


















