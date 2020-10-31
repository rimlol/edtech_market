from django.shortcuts import get_object_or_404, render
from .models import Listing, Comment
from django.contrib.auth.models import User
from .forms import CommentForm



def index(request):
    listings = Listing.objects.all() #.order_by('-rating').filter(course_published=True)
    context = {
        'listings': listings
    }

    return render(request, 'listings/listings.html', context)


def listing(request,slug):
    listing = get_object_or_404(Listing, slug=slug)
    listings = Listing.objects.order_by('direction_name').filter(course_published=True) #нужно ли оно хз
    comments = Comment.objects.filter(listing = listing).filter(status= True)
    new_comment = None
    context = {
            'listing':listing,
            'listings': listings,
            'comments': comments,
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