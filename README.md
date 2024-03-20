## Setup

The first thing to do is to clone the repository:

```sh
$ git@github.com:Zhmurik/LittleLemonAPI.git
$ cd littlelemon
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Start Django project
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/restaurant/`.
navigate to menu api `http://127.0.0.1:8000/restaurant/menu/`.
