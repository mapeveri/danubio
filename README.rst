Danubio
=======

Danubio is an open source SMS-Gateway written in Python/Flask.

Status
------

In development not suitable for production.

Features
--------

- Works with GSM modems.
- API REST for send sms and get sms received.
- Admin to see the data.

Getting started
---------------

1. Clone this repo.
2. Execute pip install -r requirements.txt.
3. Rename file conf/config_local.py.txt to conf/config_local.py and modify content file.
4. Execute in folder static npm install.
5. Run migrations.
6. For create super user execute python manage.py createsuperuser.
7. Execute python manage.py runserver and go to browser localhost:5000.
8. Execute admin localhost:5000/admin.

Migrations command
------------------

1. python manage.py db init
2. python manage.py db migrate
3. python manage.py db upgrade

Api Rest Endpoints
------------------

1. For send sms: POST to **/api/send_sms**

   Parameters:
      * number 
      * message
      * internal_id
