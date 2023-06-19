git clone https://github.com/stoeipoes02/pentrad.git
cd pentrad
chmod +x githubpull.sh
git config pull.rebase true

# add cronjob to automatically pull every minute
(crontab -l ; echo "* * * * * /usr/bin/sh /home/pi/pentrad/githubpull.sh") | crontab -


pip install django
django-admin startproject pentrad .

python3 manage.py runserver 8000