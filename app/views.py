from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, get_object_or_404
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date
from django.utils import timezone
from django.db.models import Q
# from django.contrib import messages

## api method

from .serializer import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .serializer import *
from rest_framework import viewsets, mixins
from .models import Product
from .serializer import ProductSerializer
from rest_framework import generics, filters
# from rest_framework.generics import GenericAPIView


## custom_serializer
""" pk == premiere key """

class SubcategoryBYCategoryIDviewSet(ModelViewSet):
    queryset = Sub_category.objects.all()
    serializer_class = SubcategoryByCategoryIDserializer

    def retrieve(self, request, *args, **kwargs):
        category_id = kwargs['pk']
        subcategory  = Sub_category.objects.filter(category_id = category_id)

        #breakpoint()

        return Response(SubcategoryByCategoryIDserializer(subcategory,many=True).data,status=status.HTTP_200_OK)


class ProductBYSubcatgoryIDviewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductBySubcategoryIDserializer

    def retrieve(self, request, *args, **kwargs):
        subcategory_id = kwargs['pk']
        product  = Product.objects.filter(subcategory_id = subcategory_id)

        #breakpoint()

        return Response(ProductBySubcategoryIDserializer(product,many=True).data,status=status.HTTP_200_OK)


# class ProductViewSet(viewsets.GenericViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
       
# class ProductSearchView(viewsets.GenericAPIView):
#     serializer_class = ProductSerializer

#     def get(self, request):
#         query = self.request.query_perams.get('q')
#         if query:
#             products = Product.objects.filter(product_name__icontains=query)
#         return Response(serializer.data)

class ProductSerchAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    """"  This also the way filtering   """
    # search_fields = ['color','products_name','product_description']
    # filter_backends = (filters.SearchFilter,)


    """"   This is the another way of filtering    """
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('search')
        pr  = self.request.query_params.get('price_gt')
        if query:
            return queryset.filter(
                Q(product_name__incontains = query)|
                Q(product_description__incontains = query)|
                Q(color__incontains = query)|
                Q(product_price__gt = pr)
            )
        return queryset
    


## GET

class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  

class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryViewset(ModelViewSet):
    queryset = Sub_category.objects.all()
    serializer_class = SubCategorySerializer

class ProductImageViewset(ModelViewSet):
    queryset = Product_Image.objects.all()
    serializer_class = ProductImageSerializer

class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def create(self, request, *args, **kwargs):
    #     return       

# class AddToCartViewSet(ModelViewSet):
#     queryset = AddToCart.objects.all()
#     serializer_class = AddToCartSerializerfrom django.shortcuts import render


## POST

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        p = Product.objects.get(id = product_id)
        quantity = request.data.get('quantity')

        p.stock-= 1
        p.save()
        
        s_address = request.data.get('shipping_address')
        payment_method = request.data.get('payment_method')


        price = p.product_price
        delivery_date = "2025-04-29"
        user = 1

        order = Order.objects.create(
            price = price,
            quantity = quantity,
            delivery_date = delivery_date,
            status = "In process",
            shipping_address = s_address,
            payment_method = payment_method,
            user_id = user,
            product_id = product_id
        )

        order.save()
        return Response(OrderSerializer(order).data,status=status.HTTP_201_CREATED)


## Homepage


def project_name(request):
    html = "<h1>Hello Narayan Bhai -- (see_shoes project)</h1>"
    return HttpResponse (html)


def homepage(request):
    category = Category.objects.all()
    return render(request,'index.html',{'category':category, 'user':request.user})


### category 

def create_category(request):

    if request.method == 'GET':
        return render (request,'create_category.html')
    else:
        print(request.POST)
        C_N = request.POST['category_name']
        I = request.POST['image']

        category = Category.objects.create(category_name = C_N, image = I)
        category.save()

        return HttpResponse ("category is created")


def edit_category(request,id):
     
    category = get_object_or_404(Category,id=id)
     
    if request.method == 'POST':
        category.category_name = request.POST['category_name']

        if "image" in request.FILES:
            category.image = request.FILES['image']
    
        category.save()
        return redirect('/homepage')   

    return render (request, 'edit_category.html',{'category':category})


### sub category


def sub_category_page(request,id):
    category_instance = get_object_or_404(Category,id=id)
    sub_categories = Sub_category.objects.filter(category=category_instance)
    return render(request,'sub_category_page.html',{'category':category_instance, 'sub_categories':sub_categories})


def create_sub_category(request,id):
    print(request.POST)
    category_instance = Category.objects.get(id=id)

    if request.method == 'POST':

        sub_category_name  = request.POST["sub_category_name"]
        image = request.FILES.get("image")
        print(image)

        sub_category_instance = Sub_category.objects.create( 
            category = category_instance,
            sub_category_name = sub_category_name,
            image = image,
            user = request.user
        )

        sub_category_instance.save()
        return redirect ('/homepage')
    
    return render(request, 'create_sub_category.html',{'category':category_instance})


def edit_sub_category(request,sub_category_id):

    sub_category = get_object_or_404(Sub_category,id=sub_category_id)

    if request.method == 'POST':

        sub_category.sub_category_name = request.POST.get('sub_category_name')
        category_id = request.POST.get('category')
        
        if category_id:

            category = get_object_or_404(Category,id=category_id)
            sub_category.category = category
        
        if 'image' in request.FILES:
            sub_category.image = request.FILES['image']
        
        if 'delete_image' in request.POST and sub_category.image:
            sub_category.image.delete()

        sub_category.save()
        return redirect('/homepage')
    categories = Category.objects.all()

    return render(request,'edit_sub_category.htm',{
        'sub_category':sub_category,
        'categories':categories
    })


def delete_sub_category(request,sub_category_id):
    sub_category = Sub_category.objects.get(id=sub_category_id)
    
    if request.method == 'POST':
        sub_category.delete()

        return HttpResponseRedirect("/homepage")
    return render(request,'delete_sub_category.html',{"sub_category":sub_category})


# Product

def create_product(request,sub_category_id):
    sub_category = get_object_or_404(Sub_category,id = sub_category_id)
    category = sub_category.category

    if request.method == 'POST':

        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description')
        color = request.POST.get('color')
        size = request.POST.get('size')
        brand = request.POST.get('brand')
        stock = request.POST.get('stock')

        product = Product(
            product_name = product_name,
            product_price = product_price,
            product_description = product_description,
            color = color,
            size = size,
            brand = brand,
            stock = stock,
            category = category,
            sub_category = sub_category,
            # user = request.user
        )
        product.save()

        image = request.FILES.getlist('image')

        for image in image:
            Product_Image.objects.create(product = product, image = image)

        # return redirect('/product_list_page', sub_category_id = sub_category_id)
        return redirect("/homepage")
    
    return render(request, 'create_product.html', {'sub_category_id':sub_category_id, 'sub_category':sub_category})


def product_list_page(request, sub_category_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    sub_category = get_object_or_404(Sub_category, id=sub_category_id)
    products = Product.objects.filter(sub_category=sub_category)

    
    for product in products:
        first_image = Product_Image.objects.filter(product=product).first()
        product.image_url = first_image.image.url if first_image and first_image.image else None

    page_number = request.GET.get("page")
    paginator = Paginator(products, 3)
    page_obj = paginator.get_page(page_number)

    return render(request, 'product_list.html', {
        'sub_category': sub_category,
        'products': products,
        'page_obj': page_obj
    })


def product_detail(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    # image = product.image.first()

    if request.user.is_authenticated:
        is_in_cart = Add_To_Cart.objects.filter(user=request.user, product=product).exists()
    else:
        is_in_cart = False

    return render(request,'product_detail.html',{
        'product':product,
        # 'image':image,
        'is_in_cart':is_in_cart
    })


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        product.product_name = request.POST.get("product_name")
        product.product_price = request.POST.get("product_price")
        product.product_description = request.POST.get("product_description")
        product.color = request.POST.get("color")
        product.size = request.POST.get("size")
        product.brand = request.POST.get("brand")
        product.stock = request.POST.get("stock")


        delete_images = request.POST.getlist("delete_images") 
        for image_id in delete_images:
            image = get_object_or_404(Product_Image, id=image_id)
            image.delete()

       
        for image_id in product.images.all():
            new_image = request.FILES.get(f"new_image_{image_id.id}")
            if new_image:
               
                image_id.image = new_image
                image_id.save()

       
        new_images = request.FILES.getlist("new_images")
        for new_image in new_images:
            Product_Image.objects.create(product=product, image=new_image)

        product.save()
        # return redirect("product_detail",product_id=product.id)
        return HttpResponseRedirect(f'/product_detail/{product.id}')

    return render(request, "edit_product.html", {'product':product})


def delete_product(request,product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        product.delete()

        return HttpResponseRedirect("/homepage")
    return render(request,'delete_product.html',{"product":product})
        


## Cart

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST.get('quantity', 1)) 

    if product.stock == 0:
        return HttpResponse("this product is out of stock")

    if quantity > product.stock:
        
        return HttpResponse(f"Only {product.stock} items are available.")

   
    cart_item, created = Add_To_Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        
        cart_item.quantity += quantity
    else:
      
        cart_item.quantity = quantity
    
   
    cart_item.save()
    return redirect('/cart') 
    

def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Add_To_Cart.objects.filter(user=request.user)
                
        for item in cart_items:
            item.product_images = item.product.images.first() 
            item.total_price = item.product.product_price * item.quantity  

        total_amount = sum(item.total_price for item in cart_items)
       
        return render(request, 'add_to_cart.html', {'cart_items': cart_items, 'total_amount': total_amount})
    else:
        
        return redirect('/login')
    
    
def remove_from_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect('/login')
    
    cart_item = Add_To_Cart.objects.filter(user=request.user, product_id=product_id).first()
    
    if cart_item:

        cart_item.delete()
    return redirect('/cart')

# Oder

def proceed_order(request):
    cart_items = Add_To_Cart.objects.filter(user=request.user)

    if not cart_items:
        return HttpResponse("Your cart is emptyy.")
    
    total_amount = 0
    for item in cart_items:
        product = item.product
        quantity = item.quantity
        total_amount += product.product_price * quantity
        item.total_price = product.product_price *quantity

    if request.method == "POST":
        for item in cart_items:
            product = item.product
            quantity = item.quantity

            if product.stock >= quantity:

                product.stock -= quantity
                product.save()

                delivery_date = request.POST.get('delivery_date')
                order = Order.objects.create(
                    user = request.user,
                    product = product,
                    price = product.product_price,
                    quantity = quantity,
                    shipping_address = request.POST.get('shipping_address'),
                    payment_method = request.POST.get('payment_method'),
                    delivery_date = delivery_date,
                    status = 'confirmed'
                )
                order.save()
        cart_items.delete()

        return HttpResponseRedirect(f'/order_confirmation/{order.id}')
        # return redirect('order_confirmation', order_id=order.id)
    
    return render(request,'proceed_order.html',{'cart_items':cart_items, 'total_amount':total_amount})


def buy_now(request, product_id):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    product = get_object_or_404(Product,id=product_id)

    if product.stock <= 0:
        return HttpResponse("This product is out of stock")
    
    if request.method == "POST":
        quantity = int(request.POST.get('quantity',1))
        if quantity > product.stock:
            return HttpResponse("Not enough stock available now. Please try later ")
        
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        delivery_date = request.POST.get('delivery_date', timezone.now() + timezone.timedelta(days=7))


        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            price=product.product_price,
            shipping_address=shipping_address,
            payment_method=payment_method,
            delivery_date=delivery_date,
            status='confirmed'
        )

        # return redirect('order_confirmation', order_id = order.id)
        return HttpResponseRedirect(f'/order_confirmation/{order.id}')
    
    return render(request, 'proceed_order.html',{
        'product':product,
        'is_buy_now':True
    })


def order_confirmation(request,order_id):

    order = get_object_or_404(Order,id=order_id)

    total_price = order.quantity * order.price 
    return render(request,"order_confirmation.html",{'order':order, 
    'total_proce':total_price,
    'delivery_date':order.delivery_date})


def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-booking_date')

   
    for order in orders:
        order.total_price = order.quantity * order.price
        order.is_delivered = order.delivery_date <= date.today()  

    paginator = Paginator(orders, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'order_history.html', {'page_obj': page_obj})


def cancel_order(request,order_id):
    
    if not request.user.is_authenticated:
        return redirect('userlogin')

    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'cancelled':
        return HttpResponse('this order has been cancelled')

    order.status = 'cancelled' 
    order.save()

    product = order.product
    product.stock += order.quantity
    product.save()

    return HttpResponse('Your order has been successfully canceled.') 


#n Sreach bar

def search_bar(request):
    query = request.GET.get('q', '') 
    
    data = Product.objects.none() 
    
    if query:
       
        data = Product.objects.filter(
            Q(product_name__icontains=query) | Q(product_price__icontains=query) 
            
        )   
    return render(request, 'search.html', {'products': data, 'query':query})
                                           
#       ~~~   ~~~
#        @  |  @  DEEPAK OH  DEEPAK KISI BHANCHOD KI NAZAR LAGAI
#         -----

## USer

def createuser(request):
    if request.method == "POST":

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST['email']
        phone_no = request.POST['phone_number']
        is_vendor = request.POST['is_vendor' ]

        if User.objects.filter(username=username).exists():
            return HttpResponse("Error: Username already exists. Please enter another username.")
        
    

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(
            phone_no = phone_no,
            is_vendor = is_vendor,
            # image = profile_img,
            user = user

        )
        profile.save()

       
        return redirect('/login')
    return render(request, "create_user.html")


def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/homepage')
        else:
            return render(request, "login.html")

    return render(request, "login.html")


def userlogout(request):
    logout(request)
    return redirect('/homepage')


def get_profile(request):
    if request.user.is_authenticated:
        try:
            profile_instance = request.user.profile
            is_vendor = profile_instance.is_vendor
        except Profile.DoesNotExist:
            is_vendor = False

        return render(request, "profile.html",{'user': request.user,'is_vendor':is_vendor})
    else:
        return redirect('/login')
    
def edit_profile(request):
    if request.user.is_authenticated:
        try:
            profile_instance = request.user.profile
            is_vendor = profile_instance.is_vendor
        except Profile.DoesNotExist:
            is_vendor = False

        if request.method == "POST":
          
            profile_instance.first_name = request.POST.get('first_name', profile_instance.first_name)
            profile_instance.last_name = request.POST.get('last_name', profile_instance.last_name)
            profile_instance.email = request.POST.get('email', profile_instance.email)
            profile_instance.is_vendor = request.POST.get('is_vendor') 
            
            
            if 'profile_picture' in request.FILES:
                profile_instance.profile_picture = request.FILES['profile_picture']
            
           
            profile_instance.save()
            
            return redirect('profile') 

        return render(request, "edit_profile.html", {
            'user': request.user,
            'is_vendor': is_vendor,
            'profile_instance': profile_instance 
        })
    else:
        return redirect('/login')        
    

## ajax_page ##


def ajax_get(request):
    return render (request, 'ajax_get.html')


def ajax_post(request):
    return render (request, 'ajax_post.html')