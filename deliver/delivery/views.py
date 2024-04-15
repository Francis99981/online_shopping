from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm
from shop.models import OrderModel
from django.utils.timezone import datetime


def Register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form =CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+user)
                return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)


def Login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):

    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        #dates
        today = datetime.today()
        orders = OrderModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)
        unshipped_orders =[]
        total_money = 0
        for order in orders:
            total_money += order.price

            if not order.is_shipped:
                unshipped_orders.append(order)

        context = {
            'orders': unshipped_orders,
            'total_money': total_money,
            'total_orders': len(orders)


           }
        return render(request, 'dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View ):
    def get(self, request, pk,  *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order

        }
        return render(request, 'order_details.html', context)

    def post(self, request, pk, *arg, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()
        context = {
            'order': order
        }
        return render(request, 'order_details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()
