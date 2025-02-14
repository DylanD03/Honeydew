rm -r -f honeydew/migrations
rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py makemigrations honeydew
python3 manage.py migrate
