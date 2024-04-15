from django.urls import path
from .views import Index, About, Order, Checkout, PayConfirmation, Menu, MenuSearch
from delivery.views import Register, Login, logoutUser, Dashboard

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('register', Register, name='register'),
    path('login/', Login, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('index', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search', MenuSearch.as_view(), name='menu_search'),
    path('store/', Order.as_view(), name='store'),
    path('checkout/<int:pk>', Checkout.as_view(), name='checkout'),
    path('pay_confirmation/', PayConfirmation.as_view(), name='pay_confirmation'),
]