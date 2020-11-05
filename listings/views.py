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

def index(request):
    listings = Listing.objects.all() #.order_by('-rating').filter(course_published=True)
    ratings = Rating.objects.all().filter(object_id__range=[10000,100000])
        # print(ratings.get(object_id=listing.pk).average)
    rates = [ratings.get(object_id=listing.pk).average for listing in listings]
    # print(rates[0])
    zipped = zip(listings, rates)
    zipped_tabs = zip(listings, rates)

    # Фильтры (не работают)
    if 'course_duration' in request.GET:
        course_dur = request.GET['course_duration']
        print(course_dur)
    # queryset_list = Listing.objects.order_by('-price_full').filter


    context = {
        'listings': listings,
        'ratings': ratings,
        'zipped':zipped,
        'zipped_tabs':zipped_tabs,
        'course_duration': course_duration,
    }

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
    listing = get_object_or_404(Listing, slug=slug)
    listings = Listing.objects.filter(direction_name=listing.direction_name).filter(course_published=True) #нужно ли оно хз
    comments_all = Comment.objects.filter(listing = listing)
    comments = comments_all.filter(status= True)
    comments_total = comments.count()
    vendor = Vendor.objects.get(vendor=listing.vendor)
    rating = Rating.objects.all().get(object_id=vendor.pk).average

    user_have_commented = True
    if request.user.is_authenticated:
        comments_of_user = comments_all.filter(user=request.user, listing=listing)

        if comments_of_user.exists():
            user_have_commented = True
        else:
            user_have_commented = False


    new_comment = None
    context = {
            'listing':listing,
            'listings': listings,
            'comments': comments,
            'vendor':vendor,
            'rating':rating,
            'user_have_commented': user_have_commented,
            'comments_total':comments_total,
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


def search(request):
    return render(request, 'listings/search.html')


# Тут надо сделать страницы с выбором курсов для категорий
'''
Для направлений делаем по аналогии с вендорами
Для страницы одного напавления делаем страницу аналогичную поиску
'''
def categories(request):
    categories = Category.objects.all().filter(is_active = True)
    all_categories_courses_count = {}
    for category in categories:
        category_courses_count = Listing.objects.filter(course_published=True).filter(direction_name = category).count()
        # category_slug = category.slug # тут нужно подумать, не очется заводить отделььную категорию по аналитике - хочется редиректить на страницу отфильтрованную
        all_categories_courses_count[category.russian_alias] = {
            'category_courses_count': category_courses_count,
            # 'vendor_slug': vendor_slug,

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
    }

    return render(request, 'listings/vendors.html', context)

def vendor(request,slug): # допилить
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
        all_vendor_directions_count[direction.category_name] = count_vendor_courses

    user_have_commented = True
    if request.user.is_authenticated:
        comments_of_user = vendor_comments_all.filter(user=request.user, vendor=vendor)

        if comments_of_user.exists():
            user_have_commented = True
        else:
            user_have_commented = False

    new_comment = None
    context = {
        'vendor':vendor,
        'vendor_rate':vendor_rate,
        'vendor_courses': vendor_courses,
        'all_vendor_directions_count': all_vendor_directions_count,
        'vendor_comments':vendor_comments,
        'comments_total':comments_total,
        'user_have_commented': user_have_commented,
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




