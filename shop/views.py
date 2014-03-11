from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from forms import CustRegForm
from django.template import RequestContext
from shop.models import Product, Order, Orderdetail, shipping_info, payment_info
import datetime

import OGtest.settings
# Create your views here.

def home(request):
  return render_to_response('shop/index.html', context_instance=RequestContext(request))

def register_user(request):
  if request.method == 'POST':
    form = CustRegForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/customers/register_success')
    else:
      return HttpResponseRedirect('/customers/register_invalid')
  
  reg_args={}
  reg_args.update(csrf(request))

  return render_to_response('shop/register.html', reg_args)

def register_success(request):
  return render_to_response('shop/register_success.html', context_instance=RequestContext(request))

def login(request):
  login_args = {}
  login_args.update(csrf(request))
  if "next" in request.GET:
    login_args.update({"next": request.GET["next"]})

  return render_to_response('shop/login.html', login_args)

def auth_view(request):
  username = request.POST.get('username', '')
  password = request.POST.get('password', '')
  user = auth.authenticate(username=username, password=password)

  if user is not None:
    auth.login(request, user)
    if "next" in request.GET:
      return redirect(request.GET["next"])
    else:
      return redirect('/customers/login_success')
  else:
    return redirect('/customers/login_invalid')

def login_success(request):
  return render_to_response('shop/login_success.html', context_instance=RequestContext(request))

def login_invalid(request):
  login_args = {}
  login_args.update(csrf(request))

  return render_to_response('shop/login_invalid.html', login_args)

def logout(request):
  auth.logout(request)
  return render_to_response('shop/logout.html')

def account_detail(request):
  user = request.user
  order_list = Order.objects.filter(user=user)
  return render_to_response('shop/account.html', {'orders': order_list}, context_instance=RequestContext(request))

def bookstore(request):
  return render_to_response('shop/bookstore.html', {'products': Product.objects.filter(store__name='Books'), 'repath': request.path}, context_instance=RequestContext(request))

def moviestore(request):
  return render_to_response('shop/moviestore.html', {'products': Product.objects.filter(store__name='Movies'), 'repath': request.path}, context_instance=RequestContext(request))

def drinkstore(request):
  return render_to_response('shop/drinkstore.html', {'products': Product.objects.filter(store__name='Drinks'), 'repath': request.path}, context_instance=RequestContext(request))

def addToCart(request, quantity=1):
  # ajax request to update the session
  cart = request.session.get('cart', {})
  product_id = request.GET['product_id']
  if product_id in cart:
    if int(cart[product_id]) != 0:
      cart[product_id] = int(cart[product_id]) + quantity
  else:
    cart[product_id] = quantity
  request.session['cart'] = cart
  return HttpResponse("add ok")

# helper function  
def update_cart(request):
  # called by the 'update' button on the cart page
  cart = request.session.get('cart', {})
  newcart = {}
  for product_id in cart:
    cart[product_id] = request.POST.get(product_id) 
    # delete product which quantity == 0 in the update cart
    if int(cart[product_id]) != 0:
      newcart[product_id] = cart[product_id]
  request.session['cart'] = newcart

def view_cart(request):
  if request.method == 'POST':
    ### UPDATE CART INFO FIRST if directed from the update submit form    
    update_cart(request)

  cartsummary = get_cart_summary(request)
  if "checkout" in request.POST:
    return redirect("/checkout")
  else:
    return render_to_response('shop/cart.html', {'carts': cartsummary}, context_instance=RequestContext(request))

@login_required(login_url ='/customers/login/')  # Ask user to login before they checkout
def checkout(request):
  cartsummary = get_cart_summary(request)
  return render_to_response('shop/checkout.html', {'carts': cartsummary}, context_instance=RequestContext(request))

# helper function
def get_cart_summary(request):
  cart = request.session.get('cart', {})
  cartsummary = []
  for product_id in cart:
    p = Product.objects.get(id=product_id)
    el = {}
    el.update({"product": p,
               "quantity": cart[product_id],
               "total_price": float(p.dollar_price) * int(cart[product_id])
              })
    cartsummary.append(el)
  return cartsummary

def order_process(request):
  if request.method == 'POST':
    ### UPDATE CART INFO FIRST
    update_cart(request)
    newcart = request.session.get('cart', {})

    if len(newcart) == 0:
      return redirect("/order_invalid")
    else:
      # create an order object first
      user = request.user
      curdate = datetime.datetime.now()
      order = Order(user = user, date = curdate)
      order.save()

      # create a list of order detail objects with PK = order, product
      for product_id in newcart:
        p = Product.objects.get(id=product_id)
        quantity = newcart[product_id]
        orderdetail = Orderdetail(order = order, product = p, quantity = quantity)
        orderdetail.save()

      if shipValidate(request):
        # then a shipping_info object with FK order
        recipient = request.POST['recipient']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        postal_code = request.POST['postalcode']
        shippinginfo = shipping_info(order = order, 
                                  recipient = recipient, 
                                  street = street, 
                                  city = city, 
                                  state = state, 
                                  postal_code = postal_code)
        shippinginfo.save()
      else:
        return redirect("/order_invalid")

      if paymentValidate(request):
        # then a payment_info object with FK order
        card_holder = request.POST['cardholder']
        card_num = request.POST['cardnum']
        expire_date = request.POST['expiredate']
        paymentinfo = payment_info(order = order, 
                                card_holder = card_holder, 
                                card_num = card_num, 
                                expire_date = expire_date)
        paymentinfo.save()
      else:
        return redirect("/order_invalid")

      # clean the cart info stored in the session    
      request.session['cart'] = {}
      return render_to_response('shop/order_success.html', context_instance=RequestContext(request))

def order_invalid(request):
  return render_to_response('shop/order_invalid.html', context_instance=RequestContext(request))

def shipValidate(request):
  ship_list = ["recipient", "street", "city", "state", "postalcode"]
  for k in ship_list:
    if k in request.POST:
      if not request.POST[k]:
        return False
  return True

def paymentValidate(request):
  ship_list = ["cardholder", "cardnum", "expiredate"]
  for k in ship_list:
    if k in request.POST:
      if not request.POST[k]:
        return False
  return True
