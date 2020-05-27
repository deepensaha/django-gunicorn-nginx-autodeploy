#!/bin/bash

# Starting Socket
echo "Starting Socket..."
sudo systemctl start $1.socket

# Enabling Socket
echo "Enabling Socket..."
sudo systemctl enable $1.socket

# Reload Daemon
echo "Reloading Daemon..."
sudo systemctl daemon-reload

# Restarting Socket and Service
echo "Restarting Socket and Service"
sudo systemctl restart $1

# Reload Nginx Config
echo "Reloading Nginx"
sudo /etc/init.d/nginx reload