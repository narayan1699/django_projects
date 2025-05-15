"""
URL configuration for see_shoes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app.views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
 
# define the router path and viewset to be used

router.register(r'user', UserViewset)
router.register(r'category', CategoryViewset)
router.register(r'subcategory', SubCategoryViewset)
router.register(r'products', ProductViewset)
router.register(r'product-images', ProductImageViewset)
router.register(r'order',OrderViewSet)

## custom_serializer

router.register(r'subcategory_by_category',SubcategoryBYCategoryIDviewSet,basename='subcategory_by_category_id')
router.register(r'product_by_subcategory',ProductBYSubcatgoryIDviewSet,basename='product_by_subcategory_id')


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",project_name),
    path("homepage/",homepage),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    ## API url ###
    path('api/', include(router.urls)),
    path('api/search/',ProductSerchAPIView.as_view(), name='product_Search'),

    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # category
    path("create_category/",create_category),
    path("edit_category/<int:id>/",edit_category),
    # path("delete_category/<int:id>"),


    # sub category
    path("create_subcategory/<int:id>/",create_sub_category),
    path("sub_category/<int:id>/",sub_category_page),
    path("edit_sub_category/<int:sub_category_id>/",edit_sub_category),
    path("delete_sub_category/<int:sub_category_id>/",delete_sub_category),


    # product
    path("create_product/<int:sub_category_id>/",create_product),
    path("product_list_page/<int:sub_category_id>/",product_list_page),
    path('product_detail/<int:product_id>/', product_detail),
    path('edit_product/<int:product_id>/',edit_product),
    path('delete_product/<int:product_id>/',delete_product),
    

   # cart ##
    path('add_to_cart/<int:product_id>/', add_to_cart),
    path('cart/', view_cart, name='cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart),


    # order urls
    path('order/', proceed_order),
    path('buy_now/<int:product_id>/',buy_now),
    path('order_confirmation/<int:order_id>/',order_confirmation, name="order_confirmation"),
    path('history/', order_history),
    path('cancel_order/<int:order_id>/', cancel_order),


    # search bar
    path('search/', search_bar, name="search_bar"),


    # User Views #
    path('create_user/', createuser, name='create_user'),
    path('login/', userlogin, name="userlogin"),
    path('logout/', userlogout, name="userlogout"),
    path('profile/', get_profile, name='get_profile'),

    # Ajex #
    path('ajax_get/',ajax_get),
    path('ajax_post/',ajax_post)



] +static(settings.STATIC_URL,documents_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)