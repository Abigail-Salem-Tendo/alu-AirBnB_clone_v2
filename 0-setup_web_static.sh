#!/usr/bin/env bash
#SEts up the web servers for the deployment

#install nginx if not already installed
apt-get -y update
apt-get -y install nginx

#create required directories
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared/

#create an html file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

#Delete and existing symbolic link if it exists
rm -rf /data/web_static/current

ln -s /data/web_static/releases/test/ /data/web_static/current
#give ownership to user and group
chown -R ubuntu:ubuntu /data/

#configure Nginx
sed -i '/listen 80 default_server;/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

#restart nginx
service nginx restart