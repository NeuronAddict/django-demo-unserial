# neuronaddict - Unserial demo for django

## Installation

### docker-compose method (faster but debug will be harder)

```
cd django-demo-unserial
mkdir -p .secret
echo 'mysecret' > .secret/password.txt
echo 'mysecret' > .secret/django-key.txt
docker compose up --build
```

And go to http://localhosty:8000

### django code

```
cd django-demo-unserial
mkdir -p .secret
echo 'mysecret' > .secret/password.txt
echo 'mysecret' > .secret/django-key.txt
python3 -m venv venv
source venv/bin/activate
pip install -r dev-requirements.txt
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```


