from django.urls import path
from .views.user_view import *
from .views.admin_view import *
from .views.auth_view import *
from .views.category_view import *
from .views.product_view import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # User Panel

    path('', home_view, name='home'),

    # Auth
    path('login/', user_login_view, name='user_login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='user_logout'),

    path('product/<int:id>/', product_detail_view, name='product_detail'),
    path('product/<int:id>/add-to-cart/', add_to_cart_view, name='add_to_cart'),


    path('profile/', profile_view, name='user_profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/change-password/', change_password_view, name='change_password'),


    # Admin Panel
    # Category management
    path('admin/categories/', category_list, name='admin_categories'),
    path('admin/categories/add/', add_category, name='add_category'),
    path('admin/categories/edit/<int:pk>/', update_category, name='edit_category'),
    path('admin/categories/delete/<int:pk>/', delete_category, name='delete_category'),

    path('admin/products/', list_products, name='admin_products'),
    path('admin/products/add/', add_product, name='add_product'),
    path('admin/products/edit/<int:pk>/', edit_product, name='edit_product'),
    path('admin/products/delete/<int:pk>/', delete_product, name='delete_product'),



    # Panels
    path('admin/', admin_dashboard, name='admin_dashboard'), 
    path('admin/login/', admin_login_view, name='admin_login'),
    path('admin/logout/', admin_logout_view, name='admin_logout'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)