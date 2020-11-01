from django.shortcuts import get_object_or_404, render
from .models import Listing, Comment, Vendor
from django.contrib.auth.models import User
from .forms import CommentForm
from django.http import HttpResponse
# from star_ratings import rating
from star_ratings.models import Rating



def index(request):
    listings = Listing.objects.all() #.order_by('-rating').filter(course_published=True)
    # rating = Rating.objects.filter(content_type='3').get(object_id='1')
    context = {
        'listings': listings,
        # 'rating': rating,
    }

    return render(request, 'listings/listings.html', context)


def listing(request,slug):
    listing = get_object_or_404(Listing, slug=slug)
    listings = Listing.objects.filter(direction_name=listing.direction_name).filter(course_published=True) #нужно ли оно хз
    comments = Comment.objects.filter(listing = listing).filter(status= True)
    vendor = Vendor.objects.get(vendor=listing.vendor)
    
    new_comment = None
    # print (ven.slug)
    context = {
            'listing':listing,
            'listings': listings,
            'comments': comments,
            'vendor':vendor,
            # 'vendor_slug': vendor_slug,
        }
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.listing = listing
            new_comment.save()
        
        return render(request, 'listings/listing.html', context)

    else:
        comment_form = CommentForm()

        return render(request, 'listings/listing.html', context)




def search(request):
    return render(request, 'listings/search.html')

def vendors(request):
    return render(request, 'listings/vendors.html')

def vendor(request,slug):
    vendor = get_object_or_404(Vendor, slug=slug)
    context = {
        'vendor':vendor,
    }

    return render(request, 'listings/vendor.html', context)