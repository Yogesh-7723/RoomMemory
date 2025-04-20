from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator
from localflavor.in_.models import STATE_CHOICES

GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

class User(AbstractUser):
    title = models.CharField(max_length=50,null=True,blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=10,null=True,blank=True)
    contact = models.CharField(
    max_length=10,
    unique=True,
    validators=[RegexValidator(regex=r'^\d{10}$', message="Enter a valid 10-digit contact number.")],blank=True,null=True
    )
    date_of_birth = models.DateField(blank=True,null=True)
    state = models.CharField(choices=STATE_CHOICES,max_length=20,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ImageField(upload_to='profiles/',blank=True,null=True)
    social_link = models.URLField(blank=True)

    def __str__(self):
        return self.username




# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,max_length=50,related_name='member')
    item = models.CharField(max_length=100)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.item


class Album(models.Model):
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_photos')
    photo = models.ImageField(upload_to='album/')
    caption = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"photos of {self.user_name}"


