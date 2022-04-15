# IMDB Movie API

# Deploy on Heroku
[Live Demo Link](https://imdbmovie-api.herokuapp.com)


# Requirements
```shel
Python 3.6
SQLITE
Django 3.0.7
```

## Run Locally
Create a virtualenv using `virtualenv or venv`
```shell
$virtualenv movie-enev
Activate the virtual environment by running 
$source movie-env/bin/activate
- On Windows use `source movie-env\Scripts\activate`
```

Clone the project
```shell
git clone https://github.com/imdadhussain/imdb-api.git

cd imdb-api
```

Install dependencies
```shell
$pip install -r requirements.txt
```

# Run Migrations 
```shell
python manage.py makemigrations

python manage.py migrate
```

# Populate the Data by running custom command
```shell
python manage.py populate_movie_data
```

# Run the tests
```shell
python manage.py test
```

#Running the django dev server
```shell
$python3 manage.py runserver
```

# API Documentation:-

[Postman API Documentation](https://documenter.getpostman.com/view/401490/UVyyrsLs)

# Scaling Problem Documentation:-

[Scaling Documentation](https://github.com/imdadhussain/imdb-api/blob/master/scaling-practice.txt)
