# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
#import image from pillow desktop
from PIL import Image
from django.template.defaultfilters import slugify


class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"people"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


class Gender(models.Model):
    id=models.AutoField(primary_key=True)
    gender=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    class Meta:
      verbose_name_plural = "genders"
    def __str__(self):
        return self.gender


class Region(models.Model):
    id=models.AutoField(primary_key=True)
    region=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    class Meta:
      verbose_name_plural = "regions"
    def __str__(self):
        return self.region

class Classification(models.Model):
    id=models.AutoField(primary_key=True)
    classification=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    class Meta:
      verbose_name_plural = "classifications"
    def __str__(self):
        return self.classification

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    # name=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    birth=models.DateField(max_length=255)
    gender=models.CharField(max_length=255)
    employee=models.CharField(max_length=255)
    region=models.CharField(max_length=255,null=False)
    profile_pic=models.ImageField(default='default.jpg', upload_to='profile_pics')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()


class People(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    # name=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    birth=models.DateField(max_length=255)
    gender=models.CharField(max_length=255)
    employee=models.CharField(max_length=255)
    region=models.CharField(max_length=255,null=False)
    profile_pic=models.ImageField(default='default.jpg', upload_to='profile_pics')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()






# class Staff(models.Model):
#     id=models.AutoField(primary_key=True)
#     admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     address=models.TextField()
#     # name=models.CharField(max_length=255)
#     phone=models.CharField(max_length=255)
#     birth=models.DateField(max_length=255)
#     gender=models.CharField(max_length=255)
#     employee=models.CharField(max_length=255)
#     region=models.CharField(max_length=255,null=False)
#     profile_pic=models.ImageField(default='default.jpg', upload_to='profile_pics')
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     fcm_token=models.TextField(default="")
    # objects=models.Manager()


class Intity(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,null=True)
    region=models.CharField(max_length=255,null=False)
    created=models.DateField(null=False)
    classification=models.CharField(max_length=255,null=False)
    works=models.TextField(default="",null=False)
    abstract=models.TextField(default="",null=False)
    # profile_pic=models.ImageField(default='default.jpg', upload_to='profile_pics')
    # region=models.ForeignKey(Region,on_delete=models.DO_NOTHING)
    # profile_pic=models.FileField(upload_to='images',null=True)
    intities_pic=models.FileField(upload_to='images',null=False)
    # classification=models.ForeignKey(Classification,on_delete=models.DO_NOTHING) 
    permission=models.FileField(upload_to='images',null=False)
    # address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    class Meta:
      verbose_name_plural = "intities"
    def __str__(self):
        return self.name









    # id=models.AutoField(primary_key=True)
    # admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    # gender=models.CharField(max_length=255)
    # profile_img=models.ImageField(default='default.jpg', upload_to='profile_pics')
    # region=models.ForeignKey(Region,on_delete=models.DO_NOTHING)
    # created_at=models.DateTimeField(auto_now_add=True)
    # updated_at=models.DateTimeField(auto_now_add=True)
    # objects = models.Manager()
    # class Meta:
    #   verbose_name_plural = "peoples"
    # # def __str__(self):
    # #     return self.admin

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
    # class Meta:
    #     ordering = ["-name","-gender","-region_name","-employee","-phone","-email","-member_image"]



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



@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance,address="",gender="",employee="",region="",birth="1994-10-07")
        if instance.user_type==2:
            People.objects.create(admin=instance,address="",gender="",employee="",region="",birth="1994-10-07")
            # birth="",gender="",employee="",region="",
            # Intity.objects.create(admin=instance)
            # Intity.objects.create(admin=instance,name="",region="",profile_pic="",intities_pic="",created="",classification="",works="",abstract="",permission="")
        # if instance.user_type==3:
        #     People.objects.create(admin=instance,address="")
            # People.objects.create(admin=instance,region=Region.objects.get(id=1),profile_pic="",gender="")
            
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        profile_pic = profile_pic.open(self.profile_pic.path)
        if profile_pic.width > 300 or profile_pic.height > 300:
            output_size =(300, 300)
            profile_pic.thumbnail(output_size)
            profile_pic.save(self.profile_pic.path)




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



# class Comment(models.Model):
#     admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     message = models.TextField('Message')
#     # message_reply = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()


# class Like(models.Model):
#     like = models.ManyToManyField('Comment',blank=True,related_name='likes')


# from django.db import models
# import datetime
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# #import image from pillow desktop
# from PIL import Image

# class CustomUser(models.Model):
#     user_type_data=((1,"Intities"),(2,"Staffs"))
#     user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

# class AdminHOD(models.Model):
#     admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()

# class Staffs(models.Model):
#     admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     address=models.TextField()
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()

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


# class Region(models.Model):
#     region=models.CharField(max_length=255)
#     class Meta:
#       verbose_name_plural = "regions"
#     def __str__(self):
#         return self.region



# class Classification(models.Model):
#     classification=models.CharField(max_length=255)
#     def __str__(self):
#         return self.classification


# class Intity(models.Model):
#     id=models.AutoField(primary_key=True)
#     user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
#     name=models.CharField(max_length=255,null=True)
#     region=models.CharField(max_length=255,null=True)
#     # region=models.ForeignKey(Region,on_delete=models.CASCADE)
#     intities_pic=models.FileField(upload_to='images',null=True)
#     created=models.DateField(null=True)
#     classification=models.CharField(max_length=255,null=True)
#     works=models.TextField(default="",null=True)
#     abstract=models.TextField(default="",null=True)
#     permission=models.FileField(upload_to='images',null=True)

#     class Meta:
#       verbose_name_plural = "intities"
#     def __str__(self):
#         return self.name

# # class Region(models.Model):
# #     Ar = 'اربيل'
# #     An = 'الانبار'
# #     region = [
# #         (Ar, 'اربيل'),
# #         (An, 'الانبار'),
# #     ]
# #     region = models.CharField(
# #         max_length=255,
# #         choices=region,
# #         default=Ar,
# #     )
# #     # class Meta:
# #     #   verbose_name_plural = "region"
# #     def __str__(self):
# #         return self.region

#     # def is_upperclass(self):
#     #     return self.year_in_school in {self.JUNIOR, self.SENIOR}





# class Member(models.Model):
#     name=models.CharField(max_length=255)
#     gender=models.CharField(max_length=255)
#     region=models.ForeignKey(Region,on_delete=models.CASCADE)
#     employee=models.CharField(max_length=255)
#     phone=models.CharField(max_length=255)
#     email=models.EmailField()
#     member_image=models.FileField(null=True,blank=True,upload_to='images')
#     def __str__(self):
#         return self.name
#     # class Meta:
#     #     ordering = ["-name","-gender","-region_name","-employee","-phone","-email","-member_image"]



# class Poster(models.Model):
#     name=models.CharField(max_length=255)
#     region=models.ForeignKey(Region,on_delete=models.CASCADE)
#     place=models.CharField(max_length=255)
#     classification=models.CharField(max_length=255)
#     posts=models.CharField(max_length=1000)
#     # no_Intity=models.AutoField(primary_key=True)
#     poster_image=models.FileField(null=True,blank=True,upload_to='images')
#     date_poster=models.DateField()
#     # time_poster=models.TimeField()
#     class Meta:
#       verbose_name_plural = "posters"

#     def __str__(self):
#         return self.name


# class NumVolunteer(models.Model):
#     name=models.CharField(max_length=255)
#     age=models.IntegerField()
#     gender=models.CharField(max_length=255)
#     region=models.ForeignKey(Region,on_delete=models.CASCADE)
#     employee=models.CharField(max_length=255)
#     volunteer_image=models.FileField(null=True,blank=True,upload_to='images')
#     date_Volunteer = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.name







