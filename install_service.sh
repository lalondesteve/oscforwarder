#!/bin/bash

# install the requirements
echo "Installing requirements"
pip3 install -r $PWD/requirements.txt

# set variables
export THISUSER=$SUDO_USER THISFILE=$PWD/telnet_osc_forwarder.py
HERE=$PWD/oscforwarder.service

# create service file
SERVVARS='$THISUSER:$THISFILE'
envsubst "$SERVVARS" <service_template >oscforwarder.service
#
# check if link exists
THERE=/etc/systemd/system/oscforwarder.service
if [ -f "$THERE" ]; then
	echo "Removing exisiting link"
	rm "$THERE"
fi
# #
# create link
echo "creating service symlink"
ln -s "$HERE" "$THERE"
# echo "$HERE" "$THERE"
# initiate service
systemctl daemon-reload
service oscforwarder start
# make service persistent
echo "making service persistent"
systemctl enable oscforwarder
echo "installation complete"
# 