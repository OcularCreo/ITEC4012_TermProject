# ITEC4012_TermProject

1. Clone git repository to desired location
2. Open pycharm and select open project
3. Setup configurations in project. attach script to manage.py in lowCarbAcademy folder and include runserver command.
4. in the terminal run the following commands

pip install django\
pip install django-import_export\
pip install psycopg2-binary

5. in the terminal run python manage.py migrate

IF DATABASE IS EMPTY 
1. download csv file
2. place the lowcarb_recipes.csv and sqlite3.exe into database
3. in a terminal run the following commands:

sqlite3.exe db.sqlite3\
.mode csv\
.import lowcar_recipes.csv discoverapp_recipe
