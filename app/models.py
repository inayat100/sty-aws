from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
def uplo(instance,filename): 
    filename,extension = filename.split('.')
    fname = f"{instance.user}_{instance.title}"
    fname = fname.replace("/","")
    return 'media/%s.%s' % (fname,extension)  


class POST(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE )
    img = models.ImageField(upload_to=uplo,blank=True,null=True,default='media/df.jpg')
    title = models.CharField(max_length=300)
    post = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User,related_name='like',blank=True,)
    def __str__(self):
        return self.title
    def total_like(self):
        return self.like.count()
    def total_user(self):
        return self.like.all()


class user_contact(models.Model):
    your_name = models.CharField(max_length=50)
    your_email = models.EmailField()
    your_Number = models.CharField(max_length=15)
    write = models.TextField(max_length=500)
    date = models.DateField(auto_now_add=True)

class user_comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(POST,on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment
    def total_comment(self):
        return self.comment.all()

class user_reply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(POST,on_delete=models.CASCADE)
    comment = models.ForeignKey(user_comment,on_delete=models.CASCADE)
    reply = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.reply
