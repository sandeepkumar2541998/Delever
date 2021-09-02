from django.shortcuts import render,redirect
from .models import MenuItem,Category,OrderModel
from django.core.mail import send_mail
# Create your views here.
from django.views import View
from django.db.models import Q

class Index(View):
    def get(self,request,*args, **kwargs):
        return render(request,'customer/index.html')

class About(View):
    def get(self,request,*args, **kwargs):
        return render(request,'customer/about.html')

class Order(View):
    def get(self,request,*args, **kwargs):

        # getting every item from categeory

        sweets = MenuItem.objects.filter (category__name__contains='Sweets')
        breakfasts = MenuItem.objects.filter (category__name__contains='Breakfast')
        recommendeds = MenuItem.objects.filter (category__name__contains='Recommended')
        thalicombos = MenuItem.objects.filter (category__name__contains="Thali, Combos and Meals")
        soups = MenuItem.objects.filter (category__name__contains='Soups and Salad')
        starters = MenuItem.objects.filter (category__name__contains='Starters')
        maincourses = MenuItem.objects.filter (category__name__contains='Main Course')
        breads = MenuItem.objects.filter (category__name__contains='Breads')
        rices = MenuItem.objects.filter (category__name__contains='Rice')
        southindians = MenuItem.objects.filter (category__name__contains='South Indian')
        friedrices = MenuItem.objects.filter (category__name__contains='Fried Rice and Noodles')
        accompaniments = MenuItem.objects.filter (category__name__contains='Accompaniments')
        desserts = MenuItem.objects.filter (category__name__contains='Desserts and Beverages')
        todayspecials = MenuItem.objects.filter (category__name__contains="Today's Special")

        # pass into context
        context = {
            'sweets': sweets,
            'breakfasts': breakfasts,
            'recommendeds': recommendeds,
            'thalicombos': thalicombos,
            'soups': soups,
            'starters': starters,
            'maincourses': maincourses,
            'breads': breads,
            'rices': rices,
            'southindians': southindians,
            'friedrices': friedrices,
            'accompaniments': accompaniments,
            'desserts': desserts,
            'todayspecials' : todayspecials,
        }

        return render(request,'customer/order.html',context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            # menu_item = MenuItem.objects.filter(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            name = name,
            contact = contact,
            email = email,
            price = price,
        )
        order.items.add(*item_ids)

        # send confirmation mail to the user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)

class Menu(View):
    def get(self, request, *args, **kwargs):
        recommendeds = MenuItem.objects.filter(category__name__contains='Recommended')
        sweets = MenuItem.objects.filter(category__name__contains='Sweets')
        breakfasts = MenuItem.objects.filter(category__name__contains='Breakfast')
        thalicombos = MenuItem.objects.filter(category__name__contains='Thali, Combos and Meals')
        soups = MenuItem.objects.filter(category__name__contains='Soups and Salad')
        starters = MenuItem.objects.filter(category__name__contains='Starters')
        maincourses = MenuItem.objects.filter(category__name__contains='Main Course')
        breads = MenuItem.objects.filter(category__name__contains='Breads')
        rices = MenuItem.objects.filter(category__name__contains='Rice')
        southindians = MenuItem.objects.filter(category__name__contains='South Indian')
        friedrices = MenuItem.objects.filter(category__name__contains='Fried Rice and Noodles')
        accompaniments = MenuItem.objects.filter(category__name__contains='Accompaniments')
        desserts = MenuItem.objects.filter(category__name__contains='Desserts and Beverages')
        todayspecials = MenuItem.objects.filter(category__name__contains="Today's Special")

        # menu_items = MenuItem.objects.all()

        context = {
            'recommendeds': recommendeds,
            'sweets': sweets,
            'breakfasts': breakfasts,
            'thalicombos': thalicombos,
            'soups': soups,
            'starters': starters,
            'maincourses': maincourses,
            'breads': breads,
            'rices': rices,
            'southindians': southindians,
            'friedrices': friedrices,
            'accompaniments': accompaniments,
            'desserts': desserts,
            'todayspecials' : todayspecials,
            # 'menu_items' : menu_items
        }

        return render(request, 'customer/menu.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            # menu_item = MenuItem.objects.filter(pk__contains=int(item))
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            name = name,
            contact = contact,
            email = email,
            price = price,
        )
        order.items.add(*item_ids)

        # send confirmation mail to the user
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)

        

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(quality__icontains=query)
            # Q(category__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)