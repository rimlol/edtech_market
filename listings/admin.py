from django.contrib import admin
from .models import Comment, Listing, Category, Vendor, VendorComment
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id',  'course_name','vendor', 'direction_name', 'price_full', 'course_published')
    list_display_links = ('id', 'course_name')
    list_filter = ('vendor', )
    list_editable = ('course_published',)
    search_fields = ('course_name', 'vendor', 'direction_name', 'description_full', 'format', 'specials')
    list_per_page = 25


class VendorAdmin(admin.ModelAdmin):
    list_display  = ('id', 'vendor')
    

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'listing', 'overall_rate', 'status')
    list_display_links = ('id', 'user', 'listing')
    list_editable = ('status',)
    list_filter = ('status', )


class VendorCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vendor', 'overall_rate', 'status')
    list_display_links = ('id', 'user', 'vendor')
    list_editable = ('status',)
    list_filter = ('status', )


admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(VendorComment,VendorCommentAdmin)


