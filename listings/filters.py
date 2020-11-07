from django.db.models import fields
from django.forms.widgets import CheckboxInput, SelectMultiple
from listings.models import Category, Listing, Vendor
import django_filters

"""
переписать нормально класс фильтров или ссделать функцией

фильтр по
 категориям
 тэгам
 продолжительности
 стоимости

 глабольный поиск по полям (через инпут с просмотром по описанию заголовку категории и тд)


"""



class ListingFilter(django_filters.FilterSet):
    price__lte = django_filters.NumberFilter(field_name='price_full', lookup_expr='lte', label='Стоимость до')
    vendor = django_filters.ModelChoiceFilter(
        field_name = 'vendor',lookup_expr = 'exact', label='Школа', queryset=Vendor.objects.all(),
        # choices= {'Skillbox':'Skillbox'},
        # widgets = SelectMultiple(attrs={'class': 'custom-control custom-checkbox'})
        )
    
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='direction_name', lookup_expr = 'icontains', label='Направление', queryset=Category.objects.all() )

    class Meta:
        model = Listing
        fields = {
            # 'vendor' : ['exact', ],
            'course_name' : [ 'icontains'],
            # 'price_full':['lte'],
            'direction_name' : ['exact'],
            'description_full' : [ 'icontains'],
            'description_short': [ 'icontains'],
            'program_length' :['gte'],
            'academic_hours' : ['gte'],
            'is_free' : ['exact'],

        }
        widgets = {'class': 'custom-control custom-checkbox'}


class ListingCategoryFilter(django_filters.FilterSet):
    price__lte = django_filters.NumberFilter(field_name='price_full', lookup_expr='lte', label='Стоимость до')
    vendor = django_filters.ModelChoiceFilter(
        field_name = 'vendor',lookup_expr = 'exact', label='Школа', queryset=Vendor.objects.all(),
        # choices= {'Skillbox':'Skillbox'},
        # widgets = SelectMultiple(attrs={'class': 'custom-control custom-checkbox'})
        )
    


    class Meta:
        model = Listing
        fields = {
            # 'vendor' : ['exact', ],
            'course_name' : [ 'icontains'],
            # 'price_full':['lte'],
            'description_full' : [ 'icontains'],
            'description_short': [ 'icontains'],
            'program_length' :['gte'],
            'academic_hours' : ['gte'],
            'is_free' : ['exact'],

        }
        widgets = {'class': 'custom-control custom-checkbox'}