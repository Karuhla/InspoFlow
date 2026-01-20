from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import delete_image
from .views import add_image

urlpatterns = [
    path("", views.home, name="home"),
    path('category/<str:category_name>/', views.category_view, name='category'),
    path('', views.home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('like_image/<int:image_id>/', views.like_image, name='like_image'),
    path('comment_image/<int:image_id>/', views.comment_image, name='comment_image'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('profile/', views.profile, name='user_profile'),
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    path('image/<int:image_id>/save/', views.save_image_to_board, name='save_image_to_board'),
    path('create/', views.create_board, name='create_board'),
    path('update/<int:board_id>/', views.update_board, name='update_board'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
    path("image/<int:image_id>/delete/", delete_image, name="delete_image"),
    path("add-image/", add_image, name="add_image"),
    path('board/<int:board_id>/remove_image/<int:image_id>/', views.remove_image_from_board, name='remove_image_from_board'),
    path('board/<int:board_id>/delete/', views.delete_board, name='delete_board'),

]

