from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('search/', views.search_recipes, name='search'),
    path('show_recipe/<recipe_id>', views.show_recipe, name='show_recipe'),
    path('favourite_recipe/', views.favourite_recipe, name='fav_recipe'),
    path('cookbook', views.cookbook, name='cookbook'),
]