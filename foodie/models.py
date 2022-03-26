from django.db import models



# Create your models here.
class Variety(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=False)
    image = models.ImageField(upload_to= 'variety', default= 'variety.jpg', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name 

    class Meta:
        db_table = 'variety'
        managed = True
        verbose_name = 'Variety'
        verbose_name_plural = 'Varieties'



class Meal(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    meal = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=False)
    menu = models.TextField()
    image = models.ImageField(upload_to= 'meal', default= 'meal.jpg', blank=True, null=True)
    time = models.CharField(max_length=50)
    price = models.IntegerField()
    discount = models.FloatField(blank=True, null=True)
    min_order  = models.IntegerField(default=1)
    max_order  = models.IntegerField(default=20)
    breakfast = models.BooleanField()
    lunch = models.BooleanField()
    dinner = models.BooleanField()
    display = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meal
    
    class Meta:
        db_table = 'meal'
        managed = True
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'





