from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from home.forms import SignUpForm, UserUpdeteForm
from home.models import ContactForm, Contact, CommentForm, Comment
from order.models import ShopCartForm, ShopCart
from products.models import Category, Product, Images


def index(request):
    catlist = Category.objects.all()
    sliderlist = Product.objects.all()[:5]
    products =Product.objects.all()[:6]

    #Sepet Ürün Sayısını Bulma
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()

    context = {'page': 'home',
               'catlist': catlist,
               'sliderlist': sliderlist,
               'products': products,
               }

    return render(request, "index.html",context)

def category(request,catid):
    products = Product.objects.filter(category_id=catid)
    context = {'page': 'products',
               'products': products,
               }

    return render(request, "products.html",context)


def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    category_queryset = list(Category.objects.all())
    all_slugs = [ x.slug for x in category_queryset ]
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Category,slug=slug,parent=parent)
        else:
            instance = get_object_or_404(Category, slug=slug)
            breadcrumbs_link = instance.get_cat_list()
            category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
            breadcrumbs = zip(breadcrumbs_link, category_name)
            return render(request, "postDetail.html", {'instance':instance,'breadcrumbs':breadcrumbs})

    return render(request,"categories.html",{'post_set':parent.post_set.all(),'sub_categories':parent.children.all()})


def product(request,proid):

    product = Product.objects.get(pk=proid)
    images= Images.objects.filter(product=proid)
    comments = Comment.objects.filter(product=proid,status=1).order_by('-id')
    form = ShopCartForm()
    cform = CommentForm()
    context = {'page': 'products',
               'product': product,
               'comments': comments,
               'images': images,
               'form':form,
               'cform': cform,
               }

    return render(request, "product_detail.html",context)

def login_form(request):

    if request.method=="POST":
        next_url = request.POST['next'] #get previous url
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.

            if next_url:
                return redirect(next_url)
            else:
                return redirect('/')
        #   HttpResponse(user.username)
        else:
            context = {'hata': 'Username or password incorrect',
                       }
            # Return an 'invalid login' error message.
            return render(request, "login.html",context)
    else:
        return render(request, "login.html")


def login_out(request):
    logout(request)
    return redirect('/home')



def contact_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            contactdata=Contact()
            contactdata.name =  form.cleaned_data['name']
            contactdata.email = form.cleaned_data['email']
            contactdata.subject = form.cleaned_data['subject']
            contactdata.message = form.cleaned_data['message']
            contactdata.save()

            messages.success(request, "Your message has been sent. Thank You for your interest ")
            return HttpResponseRedirect('/contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


@login_required(login_url='/login')
def comment_add(request,proid):
    # if this is a POST request we need to process the form data

    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            current_user = request.user
            data=Comment()
            data.product_id = proid
            data.user_id    = current_user.id
            data.subject    = form.cleaned_data['subject']
            data.rating     = form.cleaned_data['rating']
            data.message    = form.cleaned_data['message']
            data.save()

            messages.success(request, "Your review has been sent. Thank You for your interest ")
            return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url)

@login_required(login_url='/login')
def comment_list(request):
    current_user = request.user
    comments = Comment.objects.filter(user=current_user.id).order_by('-id')
    context = {'page': 'comments',
               'comments': comments,
               }
    return render(request, "comment_list.html",context)

@login_required(login_url='/login')
def comment_delete(request,id):
    url = request.META.get('HTTP_REFERER')  # Bir önceki adresi alır
    Comment.objects.filter(id=id).delete()
    messages.success(request, "Comment successfully deleted...")
    return HttpResponseRedirect(url)


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #Save user form data to user table
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) #login after registration
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'user_signup.html', {'form': form})


@login_required(login_url='/login')
def user_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('userchangepassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = {'page': 'user',
               'form':form,
               }
    return render(request, "user_change_password.html",context)

@login_required(login_url='/login')
def user_profile(request):
    context = {'page': 'user',}
    return render(request, "user_detail.html", context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        form = UserUpdeteForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your Profile was successfully updated!')
            return HttpResponseRedirect('profile')
    else:
        form = UserUpdeteForm(instance=request.user)
    context = {'page': 'user',
               'form': form,
              }
    return render(request, "user_update.html", context)