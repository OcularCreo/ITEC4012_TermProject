from django.urls import path
from . import views
from .views import SearchRecipe, ShowRecipe, FavouriteRecipe, Cookbook, Favourites, BookRecipes

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    #path('search/', views.search_recipes, name='search'),
    #path('show_recipe/<recipe_id>', views.show_recipe, name='show_recipe'),
    #path('favourite_recipe/', views.favourite_recipe, name='fav_recipe'),
    #path('cookbook', views.cookbook, name='cookbook'),
    #path('recipeToBook', views.recipeToBook, name='recipe-to-book'),
    path('library/', views.library, name='library'),

    path('search/<recipe_param>/<pagenum>', SearchRecipe.as_view(), name='search-recipe'),
    path('showRecipe/<recipe_id>', ShowRecipe.as_view(), name='show-recipe'),
    path('favRecipe/<recipe_id>', FavouriteRecipe.as_view(), name='favourite-recipe'),
    path('cookbooks/', Cookbook.as_view(), name='cookbook'),
    path('favourites/', Favourites.as_view(), name='favourites'),
    path('bookRecipes/<bookname>', BookRecipes.as_view(), name='cookbook-recipes'),

]