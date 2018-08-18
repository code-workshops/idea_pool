# Idea Pool API

In order requirements, I implemented some customizations to for JWT. I
updated things to match API documentation as closely as possible.

Two implementations are present: Simple JWT with DRF and a JWT solution
I built manually to mirror requirements.

The particular requirements that caused me to go with custom work are:

* Refresh token
* Custom endpoints (such as /me, /access-tokens, etc)

`dev.py` is included for this demo for ease of setup, but this should usually NOT be committed to git!

# Setup

After configuring your database settings in dev.py:

```
virtualenv venv
pip install -r requirements/dev.txt
python manage.py migrate

python manage.py runserver
```