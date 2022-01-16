# Ferry DB App... developed for University Databases Course 
# Project Setup
* Clone Repo 
* In Terminal: Run the follow commands in terminal to install the modules that are used 
* Windows

  Download Python 3.8.10 from https://www.python.org/downloads/ and run installation.
  Once Python is installed run the follow commands in a new Terminal.
  ```
  pip install sqlite3
  pip install faker
  pip install pandas
  ```
* Linux

  Install Python:
  ```
  sudo apt install python3.8
  ```
  Confirm the installation: 
  ```
  python3.8 --version
  ```
  Once Python is installed run the follow commands in a new Terminal.
  ```
  pip3 install sqlite3
  pip3 install faker
  pip3 install pandas
  ```

* Once you have all dependencies installed open  ```/src/seed.py ``` and in an interactive Python Shell run the ``` migrate.migrate()``` method to create the database tables. When tables are created in the same Shell run ```Seed()``` to insert fake data in the database.

Now you are ready to open  ```/src/app.py ``` in an interactive Python Shell and run the app. 
TIP: Type  ```book ``` to Start!

# Note
In the following files check if the  ```dbfile ``` variable points right at the path that your database want to be created.

# Contributors 
* Mitakidis Anestis, Undergrad Student of ECE at the University of Patras. 
: https://github.com/L4Limbo 
* Alejandro Matinopoulos Lopez, Undergrad Student of ECE at the University of Patras. 
# Useful links 
* Github Repo: https://github.com/L4Limbo/ferry_db
