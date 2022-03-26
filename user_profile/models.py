from django.db import models
from django.contrib.auth.models import User
# Create your models here.



STATUS = [
    ('New', 'New'),
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Closed', 'Closed'),
]

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    closed = models.DateTimeField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name


    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20,blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='profile', default='profile-icon.jpg', blank=True, null=True)
    cart_code = models.AutoField(primary_key=True, serialize=True)
    
    

    def __str__(self):
        return self.user.username   
    
    class Meta:
        db_table = 'profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


