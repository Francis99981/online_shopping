from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django .db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


class Index(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'Index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')


class Order(View):
    def get(self, request, *args, **kwargs):

        fruits = Product.objects.filter(category__name__contains='Fruit')
        vegetables = Product.objects.filter(category__name__contains='Vegatable')
        tubers = Product.objects.filter(category__name__contains='Tuber')
        cereals = Product.objects.filter(category__name__contains='Cereal')
        spices = Product.objects.filter(category__name__contains='Spice')

        context = {
            'fruits': fruits,
            'vegetables': vegetables,
            'tubers': tubers,
            'cereals': cereals,
            'spices': spices,
        }
        return render(request, 'store.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        location = request.POST.get('location')
        phone_number = request.POST.get('phone_number')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        for item in items:

            # product = Product.objects.get(pk__contains=int(item))
            product = Product.objects.get(pk=int(item))

            item_data = {
                'id': product.pk,
                'name': product.name,
                'price': product.price
            }
            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            location=location,
            phone_number=phone_number
        )
        order.items.add(*item_ids)

        body = ('Thank you for your order!, order is being processed and will be delivered soon\n'
                 f'Your total:{price}\n'
                 'Thank you')

        send_mail(
            'Thank you For your Order',
            body,
            'frade@gmail.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('checkout', pk=order.pk,)


class Checkout(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }
        return render(request, 'checkout.html', context)

    def post(self, request, pk, *args, **kwargs):
        print(request.body)


class PayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pay_confirmation.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, 'menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):

        query = self.request.GET.get("q")

        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )
        context = {
            'products': products
        }
        return render(request, 'menu.html', context)

