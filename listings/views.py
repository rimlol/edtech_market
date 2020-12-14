from django.db.models import query
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.functional import empty
from .models import Category, Listing, Comment, Vendor, VendorComment
from django.contrib.auth.models import User, AnonymousUser
from .forms import CommentForm, VendorCommentForm
from django.http import HttpResponse
# from star_ratings import rating
from star_ratings.models import Rating, UserRating
from .search_choises import course_duration
import traceback
from .filters import ListingCategoryFilter, ListingFilter, ordering_choises
from taggit.models import Tag 
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
# from .dataimport import skillbox_programming_data

def index(request, tag_slug=None):
    vendors = Vendor.objects.all().filter(is_active = True)
    categories  = Category.objects.all().filter(is_active = True)

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

    # задаем метатеги
    meta = {
         'title': 'Отзывы об онлайн курсах',
         'description' : 'Отзывы пользователей об онлайн-курсах Skillbox, Geekbrains, Skillfactory, Нетологии по программированию, дизайну, менеджменту, аналитике',
         'keywords': 'Отзывы о курсах, отзывы о Skillbox, отзывы о Geekbrains, отзывы о Skillfactory, отзывы о Нетологии, отзывы о курсах по программированию, отзывы о курсах по дизайну, отзывы о курсах по маркетингу, отзывы о курсах по менеджменту',
     }

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
        'meta':meta,
        'categories': categories,
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
    



    return render(request, 'listings/listings.html', context)

def VendorSubrate(overall_rate, vendor, request):
    """
    Функция принимает вендора и юзера и осуществляет рейтингование
    должен быть внутри  POST запроса
    """

    rate_object = Rating.objects.get(object_id = vendor.pk)
    try:
        rate_exists = UserRating.objects.get(user=request.user, rating=rate_object)
    except UserRating.DoesNotExist:
        rate_exists = False

    if rate_exists:
        rate_exists.score = overall_rate
        rate_exists.save()
    else:
        user_rating = UserRating(user = request.user, score=overall_rate, rating=rate_object)
        user_rating.save()
    return ("Successful Crossrate")

def listing(request,slug):
    vendors = Vendor.objects.all().filter(is_active = True)
    categories  = Category.objects.all().filter(is_active = True)
    listing = get_object_or_404(Listing, slug=slug)
    listings = Listing.objects.filter(direction_name=listing.direction_name).filter(course_published=True) #нужно ли оно хз
    comments_all = Comment.objects.filter(listing = listing)
    comments = comments_all.filter(status= True)
    comments_total = comments.count()
    vendor = Vendor.objects.get(vendor=listing.vendor)
    # rating_all = Rating.objects.all().get(object_id=vendor.pk)
    rating_all = listing.rating
    rating = rating_all.average
    comment_status = None
    user_have_commented = True
    if request.user.is_authenticated:
        comments_of_user = comments_all.filter(user=request.user, listing=listing).last()
        if comments_of_user:
            user_have_commented = True
            comment_status = comments_of_user.status 
            
            print(comment_status)
        else:
            user_have_commented = False
    '''
    #  пока не работает
    # first get the related HitCount object for your model object
    hit_count = HitCount.objects.get_for_object(listing)
        # next, you can attempt to count a hit and get the response
    # you need to pass it the request object as well
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    '''
    kwds_tags = listing.tags.all()
    kwds_tags = [item.slug for item in kwds_tags ]
    print(kwds_tags)
    meta = {
         'title': 'Отзывы о курсе ' + '«'+ listing.course_name +'‎»' + " от " + listing.vendor.vendor,
         'description' : 'Отзывы пользователей о курсе ' +  
                        '«'+ listing.course_name + '»' + " от " + listing.vendor.vendor + '. ' +
                        'Продолжительность: ' + str(listing.program_length) + ' мес' +
                        '. Отзывов: ' + str(listing.rating.count) +
                        '. Средняя оценка:' + str(rating_all.average),
         'keywords': 'Отзывы о курсах, отзывы о ' + listing.vendor.vendor + 
                    ', отзывы о курсах по направлению - ' + 
                    listing.direction_name.russian_alias +', '+
                    ', '.join(map(str, kwds_tags)),
     }
    new_comment = None
    context = {
            'listing':listing,
            'listings': listings,
            'comments': comments,
            'vendor':vendor,
            'rating':rating,
            'user_have_commented': user_have_commented,
            'comments_total':comments_total,
            'tags': listing.tags.all(),
            'vendors':vendors,
            'meta':meta,
            'categories':categories,
            'comment_status':comment_status,
            # 'hit_count': hit_count,
            # 'hit_count_response':hit_count_response,
        }
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.listing = listing
            new_comment.save()
            rate_object = Rating.objects.get(object_id = listing.pk)
            try:
                rate_exists = UserRating.objects.get(user=request.user, rating=rate_object)
            except UserRating.DoesNotExist:
                rate_exists = False

            if rate_exists:
                rate_exists.score = new_comment.overall_rate
                rate_exists.save()
            else:
                user_rating = UserRating(user = request.user, score=new_comment.overall_rate, rating=rate_object)
                user_rating.save()

            VendorSubrate(new_comment.overall_rate, vendor, request)

        return HttpResponseRedirect(request.path_info)

    else:
        comment_form = CommentForm()

        return render(request, 'listings/listing.html', context)


def category(request,slug):
    category = Category.objects.get(slug=slug)
    vendors = Vendor.objects.all().filter(is_active = True)
    categories  = Category.objects.all().filter(is_active = True)
    listings = Listing.objects.filter(direction_name=category.pk)
    ratings = Rating.objects.all().filter(object_id__range=[10000,100000])
    rates = [ratings.get(object_id=listing.pk).average for listing in listings]
    

    myFilter = ListingCategoryFilter(request.GET, queryset=listings)
    listings = myFilter.qs
    zipped = zip(listings, rates)
    zipped_tabs = zip(listings, rates)
    # прописсать тут метатеги
    meta = {}
    context = {
        'listings': listings,
        'ratings': ratings,
        'zipped':zipped,
        'zipped_tabs':zipped_tabs,
        'myFilter' : myFilter,
        'vendors': vendors,
        'categories':categories,

    }

    
    return render(request, 'listings/category.html', context)




def search(request):
    return render(request, 'listings/search.html')


# Тут надо сделать страницы с выбором курсов для категорий
'''
Для направлений делаем по аналогии с вендорами
Для страницы одного напавления делаем страницу аналогичную поиску
'''
def categories(request):
    vendors = Vendor.objects.all().filter(is_active = True)
    categories = Category.objects.all().filter(is_active = True)
    all_categories_courses_count = {}
    for category in categories:
        slug = category.slug
        category_courses_count = Listing.objects.filter(course_published=True).filter(direction_name = category).count()
        # category_slug = category.slug # тут нужно подумать, не очется заводить отделььную категорию по аналитике - хочется редиректить на страницу отфильтрованную
        all_categories_courses_count[category.russian_alias] = {
            'category_courses_count': category_courses_count,
            'slug':slug,
            # 'vendor_slug': vendor_slug,
            'vendors':vendors,

        }

    context = {
        'categories':categories,
        'all_categories_courses_count': all_categories_courses_count,
    }

    return render(request, 'listings/categories.html', context)


# def directions(request, slug):
#     return render(request, 'listings/directions/direction.html')


def vendors(request):
    vendors = Vendor.objects.all().filter(is_active = True)
    categories  = Category.objects.all().filter(is_active = True)

    all_vendor_courses_count = {}
    for vendor in vendors:
        vendor_courses_count = Listing.objects.filter(course_published=True).filter(vendor = vendor).count()
        vendor_slug = vendor.slug
        vendor_rating = Rating.objects.get(object_id = vendor.pk).average
        all_vendor_courses_count[vendor.vendor] = {
            'vendor_course_count':vendor_courses_count,
            'vendor_rating': vendor_rating,
            'vendor_slug': vendor_slug,

        }

    context = {
        'vendors':vendors,
        'all_vendor_courses_count': all_vendor_courses_count,
        'categories':categories,
    }

    return render(request, 'listings/vendors.html', context)

def vendor(request,slug): # допилить
    vendors = Vendor.objects.all().filter(is_active = True)
    categories  = Category.objects.all().filter(is_active = True)

    vendor = get_object_or_404(Vendor, slug=slug)
    vendor_rate = Rating.objects.get(object_id = vendor.pk).average
    vendor_courses = Listing.objects.filter(course_published=True).filter(vendor = vendor) #нужно ли оно хз
    directions = Category.objects.all()
    vendor_comments_all = VendorComment.objects.filter(vendor = vendor)
    vendor_comments = vendor_comments_all.filter(status= True)
    comments_total = vendor_comments.count()
    all_vendor_directions_count = {}

    for direction in directions:
        count_vendor_courses = vendor_courses.filter(direction_name= directions.get(category_name=direction)).count()
        all_vendor_directions_count[direction.category_name] = {
            'count_vendor_courses':count_vendor_courses,
            'vendor_id': vendor.pk,
            'direction_slug': direction.slug,
            
            }

    user_have_commented = True
    if request.user.is_authenticated:
        comments_of_user = vendor_comments_all.filter(user=request.user, vendor=vendor)

        if comments_of_user.exists():
            user_have_commented = True
        else:
            user_have_commented = False
    # прописсать тут метатеги
    meta = {}
    new_comment = None
    context = {
        'vendor':vendor,
        'vendor_rate':vendor_rate,
        'vendor_courses': vendor_courses,
        'all_vendor_directions_count': all_vendor_directions_count,
        'vendor_comments':vendor_comments,
        'comments_total':comments_total,
        'user_have_commented': user_have_commented,
        'vendors':vendors,
        'categories':categories,
    }

    if request.method == 'POST':
        comment_form = VendorCommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.vendor = vendor
            new_comment.save()
            rate_object = Rating.objects.get(object_id = vendor.pk)
            try:
                rate_exists = UserRating.objects.get(user=request.user, rating=rate_object)
            except UserRating.DoesNotExist:
                rate_exists = False
            print(rate_exists)
            if rate_exists:
                rate_exists.score = new_comment.overall_rate
                rate_exists.save()
            else:
                user_rating = UserRating(user = request.user, score=new_comment.overall_rate, rating=rate_object)
                user_rating.save()


        return HttpResponseRedirect(request.path_info)

    else:
        comment_form = VendorCommentForm()

        return render(request, 'listings/vendor.html', context)




