from django.db.models import fields
from django.forms.widgets import CheckboxInput, SelectMultiple, CheckboxSelectMultiple, TextInput, Textarea
from star_ratings.models import Rating
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
    course_name = django_filters.CharFilter(
        field_name='course_name', lookup_expr = 'icontains', label="Поиск по курсам",
        widget = TextInput,
        )
    price__lte = django_filters.NumberFilter(field_name='price_full', lookup_expr='lte', label='Стоимость до:')
    # rating__gte = django_filters.NumberFilter(field_name='rating', lookup_expr='lte', label='Оценка выше', queryset=Rating.objects.filter()

    vendor = django_filters.ModelMultipleChoiceFilter   (
        field_name = 'vendor',lookup_expr = 'exact', label='Школа', queryset=Vendor.objects.all(),
        widget=CheckboxSelectMultiple,
        # choices= {'Skillbox':'Skillbox'},
        # widgets = SelectMultiple(attrs={'class': 'custom-control custom-checkbox'})
        )
    
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='direction_name', lookup_expr = 'exact', label='Направление',
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple,
        )


    class Meta:
        model = Listing
        fields = {
            # 'vendor' : ['exact', ],
            # 'course_name' : [ 'icontains'],
            # 'price_full':['lte'],
            # 'description_full' : [ 'icontains'],
            # 'description_short': [ 'icontains'],
            # 'program_length' :['gte'],
            # 'academic_hours' : ['gte'],
            # 'is_free' : ['exact'],

        }
        widgets = {'class': 'custom-control custom-checkbox'}


class ListingCategoryFilter(django_filters.FilterSet):
    course_name = django_filters.CharFilter(
        field_name='course_name', lookup_expr = 'icontains', label="Поиск по курсам",
        widget = TextInput,
        )
    price__lte = django_filters.NumberFilter(field_name='price_full', lookup_expr='lte', label='Стоимость до:')
    # rating__gte = django_filters.NumberFilter(field_name='rating', lookup_expr='lte', label='Оценка выше', queryset=Rating.objects.filter()

    vendor = django_filters.ModelMultipleChoiceFilter   (
        field_name = 'vendor',lookup_expr = 'exact', label='Школа', queryset=Vendor.objects.all(),
        widget=CheckboxSelectMultiple,
        # choices= {'Skillbox':'Skillbox'},
        # widgets = SelectMultiple(attrs={'class': 'custom-control custom-checkbox'})
        )
    
   


    class Meta:
        model = Listing
        fields = {
            # 'vendor' : ['exact', ],
            # 'course_name' : [ 'icontains'],
            # 'price_full':['lte'],
            # 'description_full' : [ 'icontains'],
            # 'description_short': [ 'icontains'],
            # 'program_length' :['gte'],
            # 'academic_hours' : ['gte'],
            # 'is_free' : ['exact'],

        }
        widgets = {'class': 'custom-control custom-checkbox'}



ordering_choises = {
    'rating' : "По рейтингу",
    'low_price': "Сначала дешевые",
    'high_price': "Сначала дорогие",
    'duration': "Сначала короткие",
    'duration_high': "Сначала длинные",
}