# Course-catalog
## Python/Flask REST API for Yalantis
### Steps to set up the project
- Select the folder where to clone repository
- Clone the repository 
  >git clone https://github.com/Vlad-Magdysh/Course-catalog.git
- **Create virtual environment:** 
  >python3 -m venv .venv
- **Activate virtual environment**: 
  >Windows 
  >>.venv\scripts\activate
  >
  >Linux 
  >>source .venv/bin/activate
  
- **Install requirements**
  >pip install -r requirements.txt
  
- **Create .env file and write**
  > DEBUG=True 
  > FLASK_ENV=development 
  > FLASK_APP=app.py
   
### Before starting the application, you need to initialize the database
- **Command to initialize database**
  >flask init_database
  
### Command to run application
  > flask run
   
### Command to run unit tests
  > python -m unittest

## ENDPOINTS
- **Add course to the database**
  > /add-course
  > >Parameters:
  >  - title (str) : course title
  >  - start_date(str) : course start date in format YYYY-MM-DD
  >  - end_date(str) : course end date in format YYYY-MM-DD
  >  - lectures (int) : number of course lectures
  
- **Get a list of course titles**
  > /get-titles-courses
  > >Parameters:
  > - None

- **Get a course from the database by unique id**
  > /get-course
  > >Parameters:
  >  - id (int) : course unique id
  
- **Search for a course by title in a specified date range**
  > /get-filtered-courses
  > >Parameters:
  >  - title (str) : course title
  >  - start_date(str) : course start date in format YYYY-MM-DD
  >  - end_date(str) : course end date in format YYYY-MM-DD
  
- **Update course attributes by the unique ID**
  > /change-attributes
  > >Parameters:
  >  - title (str) : course title
  >  - start_date(str) : course start date in format YYYY-MM-DD
  >  - end_date(str) : course end date in format YYYY-MM-DD
  >  - lectures (int) : number of course lectures
  
- **Delete a course from the database by unique id**
  > /delete-course
  > >Parameters:
  >  - id (int) : course unique id