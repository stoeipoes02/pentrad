git clone https://github.com/stoeipoes02/pentrad.git
cd pentrad
chmod +x githubpull.sh
git config pull.rebase true

# add cronjob to automatically pull every minute
(crontab -l ; echo "* * * * * /usr/bin/sh /home/pi/pentrad/githubpull.sh 2>/home/pi/pentrad/error.log") | crontab -


pip install django
django-admin startproject pentrad .

# databse setup
python3 manage.py inspectdb
python3 manage.py makemigrations
python3 manage.py migrate


# start server at local
python3 manage.py runserver 8000
