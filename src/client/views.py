from django.shortcuts import render

from .models import Order

# Create your views here.

def index(request):
    print(request.user)
    return render(request, 'index.html')

def orders(request):
    user = request.user
    cart = request.user.order_set.filter(status=Order.StatusType.PENDING)
    orders = request.user.order_set.exclude(status=Order.StatusType.PENDING)
    
    for order in cart:
        print(order.restaurant.name)
        for item in order.item_set.all():
            print(item.quantity)
            print(f"{item.food.name} - {item.food.price}")
            
    return render(request, 'client/orders.html', {'user': user, 'cart': cart, 'orders': orders})