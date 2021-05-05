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