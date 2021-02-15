#! /usr/bin/env sh

python manage.py db migrate -m "one"
python manage.py db upgrade head


#should be done on the first time only
#python manage.py db init --multidb
# python3 python manage.py db stamp head