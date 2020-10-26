#!/bin/bash

sudo su

cd /var/www/carsfromaustralia/backend/

. /var/www/carsfromaustralia/backend/env/bin/activate

pip install -r /var/www/carsfromaustralia/backend/requirements.txt
chown -R www-data:www-data /var/www/carsfromaustralia/

service carsfromaustralia stop
cp -f /var/www/carsfromaustralia/backend/scripts/carsfromaustralia.service /etc/systemd/system/
systemctl daemon-reload
service carsfromaustralia restart

service nginx restart
