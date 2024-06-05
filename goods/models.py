from django.db import models

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=150,unique=True,verbose_name='Название')
    slug = models.SlugField(max_length=200,unique=True,blank=True,null=True,verbose_name='URL')
    
    class Meta:
        db_table = 'category'
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'