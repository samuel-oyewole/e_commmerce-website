from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guessOrder


def store(request):
    data = cookieCart(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'BUY/store.html', context)

def cart(request):

    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'BUY/cart.html', context)

def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'BUY/checkout.html', context)

def updateItem(request):
   data = json.loads(request.body)
   productId = data['productId']
   action = data['action']

   print('productId:', productId)
   print('action,', action)

   customer = request.user.customer
   product = Product.objects.get(id=productId)
   order, created = Order.objects.get_or_create(customer=customer, complete=False)

   orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

   if action == 'add':
       orderItem.quantity += 1

   elif action == 'remove':
       orderItem.quantity -= 1

   orderItem.save()

   if orderItem.quantity <= 0:
       orderItem.delete()

   return JsonResponse('item was added', safe=False)

def processOrder(request):
    # print('Data', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guessOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id


    # to check if the total passed on the front end = total on the backend
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete', safe=False)