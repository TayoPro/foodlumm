from django.urls import path 
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('meals', views.meals, name='meals'),
    path('searched', views.searched, name='searched'),
    path('meal/<str:id>/<slug:slug>', views.meal, name='meal'),
    path('variety/<str:id>/<slug:slug>', views.variety, name='variety'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('signup', views.signup, name='signup'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('profile-update', views.profile_update, name='profile-update'),
    path('password-update', views.password_update, name='password-update'),
    path('addtocart', views.addtocart, name='addtocart'),
    path('cart', views.cart, name='cart'),
    path('remove_item', views.remove_item, name='remove_item'),
    path('checkout', views.checkout, name='checkout'),
    path('placeorder', views.placeorder, name='placeorder'),
    path('paidorder', views.paid_order, name='paidorder'),
]  