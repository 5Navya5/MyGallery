from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns=[
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.product_create, name='product_create'),
     # Product operations
    path('create/',views.product_create,name='product_create'),
    path('products/',views.product_list,name='product_list'),
    path('<int:pk>/',views.product_detail,name='product_detail'),
    path('<int:pk>/edit/',views.edit_product,name='edit_product'),
    path('<int:pk>/delete/',views.delete_product,name='delete_product'),
     # Comments operations
    path('products/<int:product_id>/comments/',views.comments,name='comments'),
    path('comments/<int:comment_id>/edit/',views.edit_comment,name='edit_comment'),
    path('comments/<int:comment_id>/delete/',views.delete_comment,name='delete_comment'),
    # shared_product
    path('<int:pk>/share/', views.share_product, name='share_product'),

    
    
   

]