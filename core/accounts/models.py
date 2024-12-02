from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import generate_unique_customer_code

class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The email must be set."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Super user must have is_staff=True !"))
        if extra_fields.get('is_superuser') is not True :
            raise ValueError(_("Super user must hava is_superuser=True !"))
        
        return self.create_user(email,password,**extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    customer_code = models.CharField(max_length=10, unique=True, blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.customer_code:
            self.customer_code = generate_unique_customer_code()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')    
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/default.jpg')
    national_id = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    created_date = models.DateField(auto_now_add=True)
    wallet_balance = models.DecimalField(max_digits=10,decimal_places=0, default=0.00,null=True,blank=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name} - {self.national_id}"

    
@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)