#! /usr/bin/env sh

python3 manage.py db migrate -m "added report fields"
python3 manage.py db upgrade


#should be done on the first time only
python3 manage.py db init --multidb
python3 manage.py db stamp head