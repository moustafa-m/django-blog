# Django Blog App

Blogging website made with Django and Bootstrap5, developed and tested on an Ubuntu 22.04 system.

## Dependencies

- django5
- crispy Forms
- bootstrap5
- django-summernote
- pillow

## Running

```
$ mkdir django-blog && cd django-blog
$ git clone https://github.com/moustafa-m/django-blog.git
```
Create virtual environment:
```
$ python3 -m venv <env-name>
$ source <env-name>/bin/activate
```

Install dependencies:
```
$ cd django-blog
$ pip install -r requirements.txt
```

Migrations:
```
$ python manage.py migrate
```

Run:
```
$ python manage.py runserver
```
