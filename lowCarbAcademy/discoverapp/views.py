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

"""
def favourite_recipe(request):

    if request.method == "POST":
        return render(request, 'home.html')
    else:
        return render(request, 'home.html')
        
"""

def search_recipes(request):

    if request.method == "GET":

        #retrive data from the request
        searched = request.GET.get("search-bar")

        #do the following when the user has searched something
        if searched:

            # using filter to search database
            all_recipes = Recipe.objects.filter(Q(name__contains=searched) | Q(tags__contains=searched))

            # Pagination
            p = Paginator(all_recipes, 50)
            page = request.GET.get('page')
            recipes = p.get_page(page)

            #find all cookbooks the user might have
            user_userRecipe_objs = UserRecipe.objects.filter(user_id=request.user.id)
            all_cookbooks = user_userRecipe_objs.values("playlist_name").distinct()
            print(all_cookbooks)

            return render(request, 'search.html', {'searched': searched, 'recipes': recipes, 'cookbooks': all_cookbooks})
        else:
            return render(request, 'search.html')
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
        occurance = UserRecipe.objects.filter(user_id=curr_user_id, recipe_id=recipe_id).first() # latest('user_id', 'recipe_id')

        # when there are no matches
        if not occurance:
            print("no matches")

            favourited = UserRecipe.objects.create(user_id=request.user.id, recipe_id=recipe_id, favourite=True)
            favourited.save()

        # when there is a match
        else:

            # determine if the already existing recipe is favourited
            if occurance.favourite:

                # when it is already favourited check if it is saved as a cookbook
                existing_book = getattr(occurance, 'playlist_name')

                # Only delete the record if it is not already saved as a playlist
                if not existing_book:
                    instance = UserRecipe.objects.get(id=getattr(occurance, 'id'))
                    instance.delete()
                else:
                    # if it is saved as a playlist then just updated the favourite column of the record
                    instance = UserRecipe.objects.get(id=getattr(occurance, 'id'))
                    instance.favourite = False
                    instance.save()
            else:
                # when the already existing record is not favourited, update it to be favourited
                instance = UserRecipe.objects.get(id=getattr(occurance, 'id'))
                instance.favourite = True
                instance.save()

    else:
        print("hello")

    return render(request, 'search.html')

def cookbook(request):

    if request.method == "POST":

        # verify that the cookbook doesn't already exist

        # identify current user, get the submitted cookbook name and recipe ID
        curr_user = request.user.id
        new_book_name = request.POST["new-book"]
        recipe_id = request.POST["new-book-recipe"]

        # search for any occurances of the cookbook
        existing_books = UserRecipe.objects.filter(user_id=curr_user, playlist_name=new_book_name)

        if not existing_books:

            # check if recipe and user already have a record in the junction table
            existing_rec = UserRecipe.objects.filter(user_id=curr_user, recipe_id=recipe_id).first()

            # if there is a record that already exists
            if existing_rec:

                # get the record's value in the favourite column
                existing_fav = UserRecipe.objects.get(id=getattr(existing_rec, 'id'))

                if not existing_fav.favourite:
                    new_book = UserRecipe.objects.create(user_id=request.user.id, recipe_id=recipe_id, favourite=False, playlist_name=new_book_name)
                    new_book.save()
                else:
                    # just update the playlist name field if recipe is already saved as a favourite
                    existing_fav.update(playlist_name=new_book_name)

            else:
                # if a record does not exist
                new_book = UserRecipe.objects.create(user_id=request.user.id, recipe_id=recipe_id, favourite=False, playlist_name=new_book_name)
                new_book.save()

        else:
            print("book name already exists")

            #find out if the existing books already contain the recipe
            existing_contain_recipe = UserRecipe.objects.filter(user_id=curr_user, playlist_name=new_book_name, recipe_id=recipe_id).first()

            #if it does not already contain the recipe then add the recipe to the cookbook
            if not existing_contain_recipe:
                # if a record does not exist
                new_book = UserRecipe.objects.create(user_id=request.user.id, recipe_id=recipe_id, favourite=False, playlist_name=new_book_name)
                new_book.save()
            else:
                print("already exists in book")



    else:
        print(request)

    # get id of user

    return render(request, 'search.html')

def library(request):

    # get all favourited recipes
    faved_UserRecipes = UserRecipe.objects.filter(user_id=request.user.id, favourite=True).values("recipe_id")
    faved_recipes = []

    for recipe in faved_UserRecipes:
        faved_recipes.append(Recipe.objects.filter(id=recipe['recipe_id']).first())

    # get all cookbooks
    user_bookNames = UserRecipe.objects.filter(user_id=request.user.id).values("playlist_name").distinct()
    user_cookbooks = []

    for book in user_bookNames:

        currentBook = UserRecipe.objects.filter(user_id=request.user.id, playlist_name=book['playlist_name']).values("recipe_id")
        book_recipes = []

        for recipe in currentBook:
            book_recipes.append(Recipe.objects.filter(id=recipe['recipe_id']).first())

        user_cookbooks.append({'bookData': book_recipes, 'bookName': book["playlist_name"]})

    return render(request, 'library.html', {'favourited': faved_recipes, 'cookbooks': user_cookbooks})

def recipeToBook(request):

    """
    if request.method == "POST":
        cookbook = request.POST["book"]
        recipe_id = request.POST["recipe-id"]
        curr_user = request.user.id

        # check if recipe and user already have a record in the junction table
        existing_rec = UserRecipe.objects.filter(user_id=curr_user, recipe_id=recipe_id).first()

        print(existing_rec)

        # if there is a record that already exists
        if existing_rec:

            print("RECORD FOUND")

            # get the record's value in the favourite column
            existing_fav = UserRecipe.objects.get(id=getattr(existing_rec, 'id'))

            print("EXISTING RECORD ID: " + str(getattr(existing_rec, 'id')))

            if not existing_fav.favourite:
                new_book = UserRecipe.objects.create(user_id=request.user.id, recipe_id=recipe_id, favourite=False, playlist_name=cookbook)
                new_book.save()
            else:
                # just update the playlist name field if recipe is already saved as a favourite
                existing_fav.update(playlist_name=new_book_name)

        else:
            # if a record does not exist
            print("NO RECORD FOUND")
            #new_book = UserRecipe.objects.create(user_id=request.user.id, recipe_id=recipe_id, favourite=False, playlist_name=cookbook)
            #new_book.save()

    """

    return redirect('search/?search-bar=food')
    #return render(request, 'search.html')