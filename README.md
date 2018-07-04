# flasky
This repository contains the source code examples for the second edition of O'Reilly book Flask Web Development.

# Objective

It's only for studies proposites.


# Install

First you need create a new venv using PYTHON3.

So make sure that you have python 3 installed on your computer.

```
python3 -m venv venv
source venv/bin/active
```

After that you need install all the dependencies and third party libraries that in requirements.txt

```
pip install -r requirements.txt
```

Don't forget to set up the e-mail environment.

```
export MAIL_USERNAME=<your email>
export MAIL_PASSWORD=<your password>
```


# Running migrations

```
flask db migrate
```

# Running Application

First you must say where's the initial file endpoint of the application, in this case for porposes of study I setted up the hello.py as default (uses app.py as default application).

So you need export the default application to flask environment.

```
export FLAS_APP=hello.py
```

And running the application

```
flask run
```'
