from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Recipe
from .models import UserRecipe
from django.db.models import Q
from django.core.paginator import Paginator

from .serializers import RecipeSerializer
from .serializers import UserRecipeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
import logging


# Create your views here.
def home(request):
    return render(request, 'home.html')

def login_user(request):

    if request.method == "POST":

        # read in the user input from post request
        username = request.POST['username-input']
        password = request.POST['password-input']

        # use authenticate function to verify if the user already exists or not
        user = authenticate(request, username=username, password=password)

        # when the user does exist and the data sent isn't blank login the user otherwise do nothing
        if user is not None and username is not None and password is not None:
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
    messages.success(request, "You logged out")
    return redirect('home')

def register_user(request):

    if request.method == "POST":

        # read in the user inputs from post request
        username = request.POST['username-input']
        password1 = request.POST['password-input1']
        password2 = request.POST['password-input2']

        # make sure that the passwords sent are not the same or that the user doesn't already exist. If everything is good then make the user and log them in
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

class SearchRecipe(APIView):

    def get(self, request, recipe_param, pagenum):

        # using filter to search database
        all_recipes = Recipe.objects.filter(Q(name__contains=recipe_param) | Q(tags__contains=recipe_param))

        # Pagination
        p = Paginator(all_recipes, 10)
        page = pagenum
        recipes = p.get_page(page)

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

def search_recipes(request):

    if request.method == "GET":

        # retrive data from the request
        searched = request.GET.get("search-bar")

        # do the following when the user has searched something
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

            # return render(request, 'search.html', {'searched': searched, 'recipes': recipes, 'cookbooks': all_cookbooks})
            serializer = RecipeSerializer(all_recipes, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"success:": True})
            #return render(request, 'search.html')

    """
    else:
        return render(request, 'search.html')
    """

def show_recipe(request, recipe_id):

    # find the recipe given by recipe_id and return it
    recipe = Recipe.objects.get(pk=recipe_id)

    return render(request, 'recipe.html', {'recipe': recipe})

class ShowRecipe(APIView):

    def get(self, request, recipe_id):

        # find the recipe given by the recipe_id and return it in JSON
        recipe = Recipe.objects.get(pk=recipe_id)

        serializer = RecipeSerializer(recipe, many=False)

        return Response(serializer.data)

#class for front end
class FavouriteRecipe(APIView):

    def post(self, request, recipe_id):

        # get the id of the recipe and signed in user
        curr_user_id = 1

        # variable for existing records that will be made when the user favourites a recipe (No matter what a record will exist when this funciton is called)
        exisitngRec = None

        # search for row containing both keys/ids
        occurance = UserRecipe.objects.filter(user_id=curr_user_id, recipe_id=recipe_id).first()  # latest('user_id', 'recipe_id')

        # when there are no matches
        if not occurance:

            favourited = UserRecipe.objects.create(user_id=curr_user_id, recipe_id=recipe_id, favourite=True)
            favourited.save()
            existingRec = favourited

        # when there is a match
        else:

            existingRec = occurance

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

                # toggle or delete the record and it's favourite field, we always send the Json repsonse to say that favourite is false
                return JsonResponse({'success': True, 'favourite': False})

            else:
                # when the already existing record is not favourited, update it to be favourited
                instance = UserRecipe.objects.get(id=getattr(occurance, 'id'))
                instance.favourite = True
                instance.save()

        #return JsonReponse notifiying true or false (favourited or not)

        record = UserRecipe.objects.get(id=getattr(existingRec, 'id'))
        record_fav = record.favourite

        return JsonResponse({'success:': True, 'favourite': record_fav})

    def get(self, response, recipe_id):

        # out of time to add user validation :(
        curr_user_id = 1

        # search for row containing both keys/ids
        occurance = UserRecipe.objects.filter(user_id=curr_user_id, recipe_id=recipe_id).first()  # latest('user_id', 'recipe_id')

        # when there are no matches
        if not occurance:

            # when there is no occurance then that means the recipe has not been favourited and we send false to front
            return JsonResponse({'success:': True, 'favourite': False})

        # when there is a match
        else:

            # return true if the occurance is favourated and false if not
            if occurance.favourite:
                return JsonResponse({'success': True, 'favourite': True})
            else:
                return JsonResponse({'success': True, 'favourite': True})

class Favourites(APIView):
    def get(self, request):

        # unfortunately out of time to have front and back end authentication
        curr_user = 1

        # searching through the user recipe table as it keeps track of what recipes are favourited by the user
        recipe_userRecipe_objs = UserRecipe.objects.filter(user_id=curr_user, favourite=True)
        all_recipe_ids = recipe_userRecipe_objs.values_list('recipe_id', flat=True).distinct()

        # finding the found recipes in the recipes table
        all_recipes = Recipe.objects.filter(id__in=all_recipe_ids)

        # serializing and returning the data
        serializer = RecipeSerializer(all_recipes, many=True)
        return Response(serializer.data)

# helper function to extract recipes from the userrecipe table based on a given user, search field, and search field filter value
def extractRecipes(curr_user, search_field, filter_value):

    #dynamically create the filter for searching for the recipe in the userrecipe table
    filter = {search_field: filter_value, 'user_id': curr_user}

    # searching through the user recipe table as it keeps track of what recipes are favourited by the user
    recipe_userRecipe_objs = UserRecipe.objects.filter(**filter)
    all_recipe_ids = recipe_userRecipe_objs.values_list('recipe_id', flat=True).distinct()

    # finding the found recipes in the recipes table
    all_recipes = Recipe.objects.filter(id__in=all_recipe_ids)

    # serializing and returning the data
    serializer = RecipeSerializer(all_recipes, many=True)
    return Response(serializer.data)

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


class Cookbook(APIView):

    def get(self, request):

        # no time to add authentication for front and back end so have to include on global user : (
        userID = 1

        # find all cookbooks the user might have
        user_userRecipe_objs = UserRecipe.objects.filter(user_id=userID)
        all_cookbooks = user_userRecipe_objs.values("playlist_name").distinct()

        return JsonResponse({'cookbooks': list(all_cookbooks)})

    def post(self, request):

        curr_user = 1

        new_book_name = request.data['book_name']
        recipe_id = request.data['recipeId']

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
                    new_book = UserRecipe.objects.create(user_id=curr_user, recipe_id=recipe_id, favourite=False, playlist_name=new_book_name)
                    new_book.save()
                else:
                    # just update the playlist name field if recipe is already saved as a favourite
                    #existing_fav.update(playlist_name=new_book_name)
                    existing_fav.playlist_name = new_book_name
                    existing_fav.save()

            else:
                # if a record does not exist
                new_book = UserRecipe.objects.create(user_id=curr_user, recipe_id=recipe_id, favourite=False, playlist_name=new_book_name)
                new_book.save()

        else:

            # find out if the existing books already contain the recipe
            existing_contain_recipe = UserRecipe.objects.filter(user_id=curr_user, playlist_name=new_book_name, recipe_id=recipe_id).first()

            # if it does not already contain the recipe then add the recipe to the cookbook
            if not existing_contain_recipe:
                # if a record does not exist
                new_book = UserRecipe.objects.create(user_id=curr_user, recipe_id=recipe_id, favourite=False, playlist_name=new_book_name)
                new_book.save()

        # at the end we want to send the updated list of cookbooks back to the front end
        # find all cookbooks the user might have
        user_userRecipe_objs = UserRecipe.objects.filter(user_id=curr_user)
        all_cookbooks = user_userRecipe_objs.values("playlist_name").distinct()

        # Convert the QuerySet to a list
        cookbooks_list = list(all_cookbooks)

        return JsonResponse({'cookbooks': cookbooks_list})

    def delete(self, request):

        # get the book name and user id
        curr_user = 1
        book_name = request.data['book_name']

        # get all the records that contain the user's id and associated book name
        user_recipe_objs = UserRecipe.objects.filter(user_id=curr_user, playlist_name=book_name)

        # loop through all the filtered objects
        for records in user_recipe_objs:

            # if it is saved as a favourite just change the playlist name field to none in the record
            # otherwise delete the record as there is no relationship between the two anymore
            if records.favourite:
                records.playlist_name = None
                records.save()
            else:
                records.delete()

        return Response({'success': True})


class BookRecipes(APIView):
    def get(self, request, bookname):

        return extractRecipes(1, 'playlist_name', bookname)


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
    faved_recipes = []  # variable used to store all favourited recipes | faved_recipes = [recipe1, recipe2, ...]

    # loop through all favourited recipes found by filter & store the id of each favourited recipe into a list
    for recipe in faved_UserRecipes:
        faved_recipes.append(Recipe.objects.filter(id=recipe['recipe_id']).first())

    # get all cookbooks
    user_bookNames = UserRecipe.objects.filter(user_id=request.user.id).values("playlist_name").distinct()
    user_cookbooks = []     # list used to store list of recipes | [book1, book2, ...] book1 = [recipe1, recipe2, ...]

    # loop through all distinctly found book names
    for book in user_bookNames:

        # find all recipes that belong to the book the loop current has
        currentBook = UserRecipe.objects.filter(user_id=request.user.id, playlist_name=book['playlist_name']).values("recipe_id")
        book_recipes = []   # variable to store all recipes in the cookbook | book_recipes = [recipe1, recipe2, ...]

        # loop through all recipes in the current book found at current loop iteration & store recipe id into a list
        for recipe in currentBook:
            book_recipes.append(Recipe.objects.filter(id=recipe['recipe_id']).first())

        # add the list created into the user_cookbooks variable
        user_cookbooks.append({'bookData': book_recipes, 'bookName': book["playlist_name"]})

    # send the list of cookbooks and favourited recipes to the library page
    return render(request, 'library.html', {'favourited': faved_recipes, 'cookbooks': user_cookbooks})