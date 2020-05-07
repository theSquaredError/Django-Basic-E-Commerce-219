from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('contact', views.contact_form, name='contact'),
    path('kategoriler', views.show_category),
    path('login', views.login_form),  # View de login adında bir fonkdiyon oluşturmayınız
   # path('accounts/login/', views.login_form),  # View de login adında bir fonkdiyon oluşturmayınız
    path('join', views.user_signup,name='join'),
    path('logout', views.login_out),
    path('category/<int:catid>', views.category),
    path('product/<int:proid>', views.product,name='product'),
    path('addcomment/<int:proid>', views.comment_add, name='addcomment'),
    path('deletecomment/<int:id>', views.comment_delete, name='deletecomment'),
    path('comments', views.comment_list, name='comments'),
    path('userchangepassword', views.user_change_password, name='userchangepassword'),
    path('profile', views.user_profile, name='profile'),
    path('userupdate', views.user_update, name='userupdate'),
]