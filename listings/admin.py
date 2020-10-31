from django.contrib import admin
from .models import Comment, Listing, Category, Vendor
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id',  'course_name','vendor', 'direction_name', 'price_full', 'course_published')
    list_display_links = ('id', 'course_name')
    list_filter = ('vendor', )
    list_editable = ('course_published',)
    search_fields = ('course_name', 'vendor', 'direction_name', 'description_full', 'format', 'specials')
    list_per_page = 25
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Comment)

