import requests
import json
import uuid


from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required



# Create your views here.
from foodie.models import *
from shopcart.models import *
from user_profile.models import *
from foodie.forms import *
from user_profile.forms import *

def index(request):
    breakfast = Meal.objects.filter(breakfast=True,display=True).order_by('-id')[:4]
    lunch = Meal.objects.filter(lunch=True,display=True).order_by('-id')[:4]
    dinner = Meal.objects.filter(dinner=True,display=True).order_by('-id')[:4]
    varieties = Variety.objects.all()  
    
    
    context = {
        'breakfast':breakfast,
        'lunch':lunch,
        'dinner':dinner,
        'varieties':varieties,
    }

    return render(request, 'index.html',context)


def meals(request):
    # if 'itemsearch' in request.GET:
    #     searched = request.GET['itemsearch']
    #     meals = Meal.objects.filter(Q(Q(meal__icontains=searched)|Q(time__icontains=searched)))
    # else:
    meals = Meal.objects.all().order_by('-created').filter(display=True)
    paginator = Paginator(meals,4)
    page= request.GET.get('page')
    paginate = paginator.get_page(page)

    context = {
        'meals':meals,
        'paginate':paginate,
    }

    return render(request, 'meals.html',context)


def searched(request):
    if  request.method == 'POST':
        searched = request.POST['itemsearch']
        searched_item = Q(Q(meal__icontains=searched)|Q(time__icontains=searched))
        searched_meals = Meal.objects.filter(meal__icontains=searched)
    else:
        searched_meals = Meal.objects.all()

    context = {
        'searched_meals':searched_meals,
        'searched':searched,
    }

    return render(request, 'searched.html',context)



def meal(request, id, slug):
    meal = Meal.objects.get(pk=id)
    
    context = {
        'meal':meal,
    }

    return render(request, 'meal.html', context)
 

def variety(request, id,slug):
    variety = Meal.objects.filter(variety_id=id) #query for single variety and its children within its immediate generation and parent generation
    single_variety = Variety.objects.get(pk=id) #query for single variety only within its immediate generation
    paginator = Paginator(variety,4)
    page= request.GET.get('page')
    paginate = paginator.get_page(page)

    context = {
        'paginate':paginate,
        # 'variety':variety,
        'single':single_variety,
    }
    return render(request, 'variety.html',context)



def contact(request):
    cform = ContactForm() #instantiate an empty form for a GET request
    if request.method == 'POST':
        cform = ContactForm(request.POST) #instantiate the form for a POST request
        if cform.is_valid():
            cform.save()
            messages.success(request, 'Thank you for contacting us! Our Customer care agent will reach you soon.')
        return redirect('index')

    context = {
        'cform':cform
    }

    return render(request, 'index.html', context)



# authentication 
def signin(request):
    varieties = Variety.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}, its good to have you here!')
            return redirect('index')
        else:
            messages.info(request, 'Username/password incorrect, kindly check your details, thank you.')
            return redirect('signin')

    return render(request, 'login.html',{'varieties':varieties})


def signout(request):
    logout(request)
    messages.success(request, 'You have now signed out of your account.')
    return redirect('signin')


def signup(request):
    form = SignupForm() 
    if request.method == 'POST': 
        phone = request.POST['phone']
        image = request.POST['image']
        form = SignupForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            profile = Profile(user = user)
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.phone = phone
            profile.image = image
            profile.save()
            login(request, user)
            messages.success(request, f'Congratulations {user.first_name} your signup is Successful!')
            return redirect('index') 
        else:
            messages.error(request, form.errors) 

    varieties = Variety.objects.all()
    context = {
        'form':form,
        'varieties':varieties,
    }

    return render(request, 'signup.html',context)

# authentication done

# profile 
@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username= request.user.username)
   
    context = {
        'profile':profile,
    }
    
    return render(request, 'profile.html',context)


@login_required(login_url='signin')
def profile_update(request):
    load_profile = Profile.objects.get(user__username= request.user.username)
    form = ProfileForm(instance= request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance= request.user.profile)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Dear {user.first_name} your profile update is successful!')
            return redirect('profile')
        else:
            messages.error(request, f'Dear {user.first_name} kindly follow the instructions {form.errors}, thank you.')
            return redirect('profile')


    context = {
        'load_profile':load_profile,
        'form':form,
    }

    return render(request, 'profile_update.html',context)



@login_required(login_url='signin')
def password_update(request):
    load_profile = Profile.objects.get(user__username= request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Dear {user.first_name} your request for password change is successful!')
            return redirect('profile')
        else:
            messages.error(request, f'Dear {user.first_name} kindly follow the instrustions herein {form.errors}, thank you!')
            return redirect('password-update')

    context = {
        'load_profile':load_profile,
        'form':form,
        'varieties':varieties
    }

    return render(request, 'profile_password.html',context)
# profile done


# shopcart
@login_required(login_url='signin') 
def addtocart(request):
    # cart_code = str(uuid.uuid4())
    cartno = Profile.objects.get(user__username=request.user.username)
    cart_code = cartno.cart_code
    if request.method == 'POST':
        addquantity =  int(request.POST['quantity'])
        addspice =  request.POST['how_spicey']
        addid =  request.POST['mealid'] 
        mealid = Meal.objects.get(pk=addid)
        

        # instantiate the cart for prospective users 
        cart = ShopCart.objects.filter(user__username=request.user.username,item_paid=False)
        
        if cart:    # instantiate the cart for a selected item 
            more =ShopCart.objects.filter(meal_id=mealid.id,quantity=addquantity,how_spicey=addspice,user__username=request.user.username).first()
            if more:
                more.quantity = addquantity
                more.how_spicey = addspice
                more.save()
                messages.success(request, "Product added to Shopcart")
                return redirect('meals')

            else: #add new items 
                newitem = ShopCart()
                newitem.user = request.user
                newitem.meal = mealid
                newitem.quantity = addquantity
                newitem.how_spicey = addspice
                newitem.order_no = cart_code
                newitem.item_paid = False
                newitem.save()
                messages.success(request, "Product added to Shopcart")
                return redirect('meals')

        else: # create a cart
            newcart = ShopCart()
            newcart.user = request.user
            newcart.meal = mealid
            newcart.quantity = addquantity
            newcart.how_spicey = addspice
            newcart.order_no = cart_code
            newcart.item_paid = False
            newcart.save()
            messages.success(request, 'Item has been added to your shopcart!')

    return redirect('meals')


@login_required(login_url='signin')
def cart(request):   
    shopcart = ShopCart.objects.filter(user__username = request.user.username, item_paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for item in shopcart:
        if item.meal.discount:
            subtotal += item.meal.discount * item.quantity
        else:
            subtotal += item.meal.price * item.quantity

    #vat is at 7.5% of the subtotal, that is 7.5/100 * subtotal
    vat = 0.075 * subtotal

    # addition of vat and subtotal gives the total value to be charged
    total = subtotal + vat

    context = {
        'shopcart':shopcart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }

    return render(request, 'cart.html',context)
    

#delete items from shopcart
@login_required(login_url='signin')
def remove_item(request):
    deleteitem = request.POST['deleteitem']
    ShopCart.objects.filter(pk=deleteitem).delete()
    messages.success(request, 'Item successfully deleted from your Shopcart!')
    return redirect('meals')

#delete items from shopcart done

@login_required(login_url='signin')
def checkout(request):
    shopcart = ShopCart.objects.filter(user__username = request.user.username, item_paid=False)
    profile = Profile.objects.get(user__username = request.user.username)

    subtotal = 0
    vat = 0
    total = 0

    for item in shopcart:
        if item.meal.discount:
            subtotal += item.meal.discount * item.quantity
        else:
            subtotal += item.meal.price * item.quantity

    #vat is at 7.5% of the subtotal, that is 7.5/100 * subtotal
    vat = 0.075 * subtotal

    # addition of vat and subtotal gives the total value to be charged
    total = subtotal + vat

    context = {
        'profile':profile,
        'shopcart':shopcart,
        'total':total,
    }

    return render(request, 'checkout.html',context)



# integrate to payment gateway, in this instance paystack 
@login_required(login_url='signin')
def placeorder(request):
    if request.method == 'POST':
        # collect data to send to paystack 
        api_key = 'sk_test_0c3bb25f14513ee95dcbe057e8b007f8b8480aa1'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://3.86.39.183/paidorder'
        # cburl = 'http://54.227.95.171/paidorder'
        cburl = 'http://127.0.0.1/paidorder'
        # cburl = 'http://localhost:8000/paidorder'
        ref_num = str(uuid.uuid4())
        total =    float(request.POST['get_total']) * 100
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        last_name = request.POST['last_name']
        cartno = Profile.objects.get(user__username=request.user.username)
        order_num = cartno.cart_code
        user = User.objects.get(username = request.user.username)
        
        headers = {'Authorization': f'Bearer {api_key}'}
        data ={'refrence':ref_num, 'order_number': order_num, 'amount': int(total),'email':user.email, 'callback_url': cburl,'currency':'NGN'}
        
        # collect data to send to paystack done
        
        # call to paystack 
        try:
            r = requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy. Please try again in few minutes. Thank You!')
        else:
            # create an order 
            transback = json.loads(r.text)
            rd_url = transback['data']['authorization_url']

            # take record of transactions made
            paidorder = PaidOrder()
            paidorder.user = user
            paidorder.total = total/100
            paidorder.cart_no = order_num
            paidorder.payment_code = ref_num
            paidorder.paid_item = True
            paidorder.first_name = user.first_name
            paidorder.last_name = user.last_name
            paidorder.save()

            
            shipping = Shipping()
            shipping.user = user
            shipping.shipping_no = order_num
            shipping.paid_cart = True
            shipping.fname = user.first_name
            shipping.lname = user.last_name
            shipping.address = address
            shipping.phone = phone
            shipping.state = state
            shipping.save()
            # take record of transactions made done
            return redirect(rd_url)
        # call to paystack done, when transaction is successful it redirects to the callback page

    # if transaction error occurs it redirects to checkout 
    return redirect('checkout')



def paid_order(request):
    profile = Profile.objects.get(user__username = request.user.username)
    cart = ShopCart.objects.filter(user__username = request.user.username, item_paid=False)
    for item in cart:
        item.item_paid = True
        item.save()

    context = {
        'profile':profile
    }

    return render(request, 'cart_paid.html',context)
# shopcart done 


