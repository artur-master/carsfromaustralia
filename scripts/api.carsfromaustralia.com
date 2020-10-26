server {
    listen 80;

    server_name api.carsfromaustralia.com www.api.carsfromaustralia.com;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/carsfromaustralia.sock;
    }

    access_log /var/www/carsfromaustralia/logs/nginx/access.log;
    error_log /var/www/carsfromaustralia/logs/nginx/error.log;
}
