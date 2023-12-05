# ITEC4012_TermProject Backend Instructions

git repository: https://github.com/OcularCreo/ITEC4012_TermProject.git

1. Clone git repository to desired location
2. Open pycharm and select open project
3. Setup configurations in project. attach script to manage.py in lowCarbAcademy folder and include runserver command.


    a. in pycharm, at the top right of area of the project click the dropdown.\
    b. select the edit configurations and choose python in the left window\
    c. Fill out fields with runserver commands and name it that same if you wish, other field inputs will vary 
     depending on the location of the documents in your project\


4. in the pycharm terminal run the following commands

pip install django\
pip install django-import_export\
pip install psycopg2-binary\
pip install django-cors-headers\
pip install djangorestframework\

5. in the pycharm terminal run python manage.py migrate

TO POPULATE DATABASE 
1. download csv file and sqlite.exe (lowcarb_recipes.csv)
2. place the lowcarb_recipes.csv and sqlite3.exe into database
3. in a windows or other kind of terminal run the following commands:

sqlite3.exe db.sqlite3\
.mode csv\
.import lowcarb_recipes.csv discoverapp_recipe\

Note: on my end I needed to run these commands twice for it to fill out the whole table. 
When it does fill the table it may print a bunch of error messages about filling out a
field. Those messages shouldn't really cause any problems and the table should fill out.


Justifications: 

Due to a heavy work-load from the many courses that I have been registered in this semester, the implementation of
user accounts/authorization needed to be dropped while creating the connection between the front and back end.

While reviewing the frontend proposal, you may recall that the data-base used for the backend is missing key data such
as ingredient quantities, recipe images, and so on. Because of this recipes either use placeholder information or simple
do not provide the information.