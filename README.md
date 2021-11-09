If using docker after installing docker desktop downoad code and run from application folder.

docker-compose up --build

to access the mssql on the mysql docker use:

docker exec -it gym_managment_db_1 mysql -ugym -p

you will be prompted for the gym users password.  Once entered you can run sql commands against the mysql database.


If you are not going to use docker you can use the instructions in https://flask.palletsprojects.com/en/2.0.x/installation/ to setup your dev env.

Once you install mysql run the init.sql in the db folder to create the database.

go to the folder the application is and run

python3 app.py

I did not get this to work because I had issues installing the mysql module on my laptop.  

This should work if you can install all the modules in requirements.txt

in app.py line 16 you should change the database hostname to localhost.
