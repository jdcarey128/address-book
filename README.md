## Address Book 

### Front End 
The front end for this app can be found [here](https://github.com/jdcarey128/address-book-front-end)

### App in Production 
Checkout the app hosted on Heroku [here](https://address-book-frontend-lt.herokuapp.com/login)

Explore the app's functionality using the following credentials, or register your own account:  
```
email: test@example.com
password: test1234
```

### Installation 
```zsh
# create a virtual environment 
python3 -m venv ./venv

# activate virtual environment 
source venv/bin/activate

# install dependencies 
pip3 install -r requirements.txt

# Export app configuration
export FLASK_APP=run.py
export FLASK_CONFIG=development
```

### Database Setup 
If needed, download PostgreSQL from [here](https://www.postgresql.org/download/)
```zsh
# create postgres dev and test databases
# make sure postgres server is running 
createdb address_book_development
createdb address_book_test

# run migrations for development 
flask db migrate 
flask db upgrade

# run migrations for test 
export FLASK_CONFIG=testing
flask db migrate 
flask db upgrade
```
### Troubleshooting migrations (Just in case you're like me)
```zsh
# If you get the following error when running the above migrations:
Try 'flask --help' for help.

Error: No such command 'db'.

# And 'flask --help' gives you the following: 
ModuleNotFoundError: No module named 'flask_migrate'

# Try uninstalling the global flask installation 
deactivate 
pip uninstall flask 
source venv/bin/activate 
flask db migrate 

# and hopefully that works!
```

### Testing 
From terminal, run `pytest`. You should see 66 passing tests (endpoints and models). 

To see test coverage: 
```zsh
# remove any caching and previous coverage reports 
rm -rf .pytest_cache/ htmlcov .coverage 

# set configuration to testing 
export FLASK_CONFIG=testing 

# run tests with coverage 
coverage run -m pytest 

# generate coverage report 
coverage html 

# open coverage report in browser 
open htmlcov/index.html 

# filter coverage to 'api/'
```

### Running API 
```zsh
# Confirm that you are using development configuration 
env 

# If not, switch to development configuration
export FLASK_CONFIG=development

# Run local server 
python3 run.py

# Make sure the API is running along with front end server to interact with the app. 
```

### Project Highlights 
1. First time connecting Flask API to database 
1. All endpoints and resources tested: 99% test coverage
1. RESTful routes (except for user login)

### Future Additions
1. Allow contacts to have multiple addresses

### Author
**Joshua Carey** - *Turing Graduate* - [GitHub Profile](https://github.com/jdcarey128) - [Turing Alum Portfolio](https://terminal.turing.edu/profiles/595) - [LinkedIn](https://www.linkedin.com/in/carey-joshua/)
