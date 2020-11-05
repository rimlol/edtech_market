from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import DO_NOTHING
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField
from uuslug import uuslug

from django.db.models.query import ModelIterable
# from django.utils.text import slugify
from uuslug import slugify

# from testimonial.models import Testimonial
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    russian_alias = models.CharField(max_length=200)
    slug = models.SlugField(max_length=70, blank=True)
    is_active	= models.BooleanField(default=True)
    def __str__(self):
        return self.category_name

    def __unicode__(self):
         return self.category_name

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = uuslug(self.category_name, instance=self)
            # super(Category, self).save(*args, **kwargs)

        super(Category, self).save(*args, **kwargs)


class Vendor(models.Model):
    vendor = models.CharField(max_length=200)
    slug = models.SlugField(max_length=70, blank=True)
    is_active	= models.BooleanField(default=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.vendor

    def __unicode__(self):
         return self.vendor

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = uuslug(self.vendor, instance=self)
            # super(Category, self).save(*args, **kwargs)

        super(Vendor, self).save(*args, **kwargs)

class Listing(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=DO_NOTHING)
    course_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=70, blank=True)
    direction_name=	 models.ForeignKey(Category,  on_delete=models.DO_NOTHING)
    price_full = models.IntegerField(blank=True, default=0)
    price_per_month	= models.IntegerField(blank=True, default=0)
    # rating	= models.DecimalField(max_digits=3, decimal_places=2, blank=True)
    # testimonials =   models.TextField(blank=True) #тут нужно понять как запросить все отзывы (по ид всех отзывов) может тут и не надо и моэно просто сослаться
    # testimonials_count	= models.IntegerField(blank=True) #тут ну
    description_full =   models.TextField(blank=True)
    description_short =  models.TextField(blank=True)
    program_length = models.IntegerField(blank=True, default=0)
    academic_hours	= models.IntegerField(blank=True, default=0)
    start_date = models.DateField(blank = True)
    format =  models.TextField(blank=True)
    specials =  models.TextField(blank=True)
    p_code	= models.CharField(max_length=100, blank=True)
    main_image	= models.ImageField(upload_to = 'course_photos/%Y/%m/%d/', blank=True)
    is_free	= models.BooleanField(default=False)
    course_published = models.BooleanField(default=True)
    link_to_product	= models.URLField(blank=True, max_length=1000)

    def __str__(self):
        return self.course_name

    def __unicode__(self):
         return self.course_name

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = uuslug(self.course_name, instance=self)

        super(Listing, self).save(*args, **kwargs)


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=DO_NOTHING)
    subject = models.CharField(max_length=100,blank=True)
    comment = models.TextField( blank=True)
    overall_rate = models.IntegerField(default=3)
    ip = models.GenericIPAddressField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(blank=True,default=0)
    dislikes = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return self.subject

class VendorComment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=DO_NOTHING)
    subject = models.CharField(max_length=100,blank=True)
    comment = models.TextField( blank=True)
    overall_rate = models.IntegerField(default=3)
    ip = models.GenericIPAddressField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(blank=True,default=0)
    dislikes = models.IntegerField(blank=True,default=0)

    def __str__(self):
        return self.subject


# class Comment(models.Model):
#     STATUS = (
#         ('New', 'New'),
#         ('True', 'True'),
#         ('False', 'False'),
#     )
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
#     user = models.ForeignKey(User,on_delete=DO_NOTHING)
#     subject = models.CharField(max_length=100,blank=True)
#     comment = models.CharField(max_length=500, blank=True)
#     rate = models.IntegerField(default=1)
#     ip = models.CharField(max_length=20, blank=True)
#     status = models.CharField(max_length=10, choices=STATUS, default='New')
#     create_at = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.subject
