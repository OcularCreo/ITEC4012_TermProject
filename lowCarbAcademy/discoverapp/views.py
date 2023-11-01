from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Recipe
from .models import UserRecipe
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_user(request):

    if request.method == "POST":
        username = request.POST['username-input']
        password = request.POST['password-input']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #messages.success(request, ("login sucessful"))
            return redirect('home')
        else:
            #messages.success(request, ("Incorrect login"))
            return redirect('login')

    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You logged out"))
    return redirect('home')

def register_user(request):

    if request.method == "POST":
        username = request.POST['username-input']
        password1 = request.POST['password-input1']
        password2 = request.POST['password-input2']

        if password1 != password2:
            print("password not matching - new")
        elif User.objects.filter(username=username).exists():
            print("username already taken")
        else:
            user = User.objects.create_user(username=username, password=password1)
            user.save()

            login(request, user)

        return redirect('home')

    else:
        return render(request, 'register.html')

def favourite_recipe(request):

    if request.method == "POST":
        return render(request, 'home.html')

    else:
        return render(request, 'home.html')

def search_recipes(request):

    if request.method == "GET":
        searched = request.GET.get("search-bar")

        # using filter to search data base
        all_recipes = Recipe.objects.filter(Q(name__contains=searched) | Q(tags__contains=searched))

        # Pagination
        p = Paginator(all_recipes, 50)
        page = request.GET.get('page')
        recipes = p.get_page(page)

        return render(request, 'search.html', {'searched': searched, 'recipes': recipes})
    else:
        return render(request, 'search.html')

def show_recipe(request, recipe_id):

    recipe = Recipe.objects.get(pk=recipe_id)

    return render(request, 'recipe.html', {'recipe': recipe})

def favourite_recipe(request):

    if request.method == "POST":

        # get the id of the recipe and signed in user
        curr_user_id = request.user.id
        recipe_id = request.POST['faved']

        # search for row containing both keys/ids
        occurance = UserRecipe.objects.filter(user_id=curr_user_id, recipe_id=recipe_id).latest('user_id', 'recipe_id')

        #when there are no matches
        if not occurance:
            print("no matches")

            favourited = UserRecipe.objects.create(user_id=request.user.id, recipe_id=recipe_id, favourite=True)
            favourited.save()

        #when there is a match
        else:

            instance = UserRecipe.objects.get(id=getattr(occurance, 'id'))
            instance.delete();

    else:
        print("hello")

    return render(request, 'search.html')

def cookbook(request):

    # get id of user

    return render(request, 'search.html')