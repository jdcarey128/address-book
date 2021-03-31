## Address Book 


### Installation 
```zsh
# create a virtual environment 
python3 -m venv venv

# activate virtual environment 
source venv/bin/activate

# install dependencies 
pip install requirements.txt

# Export app configuration
export FLASK_CONFIG=develpment
```

### Database Setup 
If needed, download PostgreSQL from [here](https://www.postgresql.org/download/).
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
### Testing 
From terminal, run `pytest`. You should see 62 passing tests (endpoints and models). 
