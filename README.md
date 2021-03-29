## Address Book 


### Installation 

1. Create a virtual environment: `python3 -m venv venv`
1. Activate virtual environment: `source venv/bin/activate`
1. Install dependencies: `pip install requirements.txt`
1. Export app configuration: `export FLASK_CONFIG=develpment`


### Database Setup 

```zsh
# create postgres dev and test databases
# make sure postgres server is running 
createdb address_book_development
createdb address_book_test

export FLASK_APP=run.py

# run migrations for development 
flask db migrate 
flask db upgrade

# run migrations for test 
export FLASK_CONFIG=testing
flask db migrate 
flask db upgrade
```
