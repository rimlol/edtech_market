from django.db.models import query
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.functional import empty
from listings.models import Category, Listing, Comment, Vendor, VendorComment
from django.contrib.auth.models import User, AnonymousUser
from listings.forms import CommentForm, VendorCommentForm
from django.http import HttpResponse
# from star_ratings import rating
from star_ratings.models import Rating, UserRating
from listings.search_choises import course_duration
import traceback
from listings.filters import ListingCategoryFilter, ListingFilter, ordering_choises
from taggit.models import Tag 
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
# from .dataimport import skillbox_programming_data


def index(request, tag_slug=None):
    vendors = Vendor.objects.all().filter(is_active = True)
    categorys = Category.objects.all()
    # задать фильтрацию  листингов на основе запроса пользователя
    listings = Listing.objects.all() #.order_by('-rating').filter(course_published=True)
    ratings = Rating.objects.all().filter(object_id__range=[10000,100000])
    rates = [ratings.get(object_id=listing.pk).average for listing in listings]

    # print(Category.objects.get(category_name='Programming').pk)


    myFilter = ListingFilter(request.GET, queryset=listings)
    listings = myFilter.qs

    # тут можно дописать фильтр по рейтингу (делаем запрос с фильтрацией average > {input_rating})
    # надо только вспомнить как передавать input rating choises
    # и после этого надо как-то включить это в форму запроса минуя форму листингов (возможно фильтруя листинги до того как это сделает основной фильтр  )

    tag = None  
    if tag_slug:  
        tag = get_object_or_404(Tag, slug=tag_slug)  
        listings = listings.filter(tags__in=[tag])  

    # добавляем сортировку
    if 'sort_by' in request.GET:
        sort_by = request.GET['sort_by']
        if sort_by:
            # прописать тут статусы и вписать изменение на активный если он мэтчится с кеем
            # active_state = {
            #     'low_price': 'false',
            #     'high_price': 'false',
            #     'duration': 'false',
            #     'duration_high': 'false',
            #     'rating': 'false',
            # }
            if sort_by == 'low_price':
                listings = listings.order_by('price_full')
            elif sort_by == 'high_price':
                listings = listings.order_by('-price_full')
            elif sort_by == 'duration':
                listings = listings.order_by('program_length')
            elif sort_by == 'duration_high':
                listings = listings.order_by('-program_length')
            # есть баг - меняется отображение звезд при сортировке
            # надо связать все курсы с рейтингами / потом переписать темплейт, уйти от зипа 
            # и  уйти от переменной rates
            # остается проблема ручного привязывания курсов - трудно будет привязать
            elif sort_by == 'rating':
                listings = listings.order_by('-rating__average')
                


    zipped = zip(listings, rates)
    zipped_tabs = zip(listings, rates)
    len_listiings = len(listings)

    context = {
        'listings': listings,
        'ratings': ratings,
        'zipped':zipped,
        'zipped_tabs':zipped_tabs,
        'myFilter' : myFilter,
        'tag': tag,
        'len_listiings':len_listiings,
        'vendors': vendors,
        'ordering_choises' : ordering_choises,
        'categorys': categorys,
    }

    """
    очень хуевый способ импорта, но работает
    """
    # def data_import(data):
    #     for elem in data:
    #         vendor = Vendor.objects.get(id= elem[0])
    #         cat = Category.objects.get(id= elem[2])

    #         new_listing = Listing(
    #             vendor = vendor,
    #             course_name = elem[1],
    #             direction_name=	 cat,
    #             program_length = elem[4],
    #             link_to_product	= elem[3]
    #         )
    #         new_listing.save()
    #         print("Success adding", new_listing)
    #  тут нужно еще создавать рейтинг при добавлении нового листинга Rating(object_id = listing.pk).save()

    # data_import(skillbox_programming_data)
    



    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')
