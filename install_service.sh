#!/bin/bash

# install the requirements
echo "Installing requirements"
pip3 install -r $PWD/requirements.txt

# set variables
export THISUSER=$SUDO_USER THISFILE=$PWD/telnet_osc_forwarder.py HERE=$PWD/scripts/oscforwarder.service

# create service file
SERVVARS='$THISUSER:$THISFILE'
envsubst "$SERVVARS" <$PWD/scripts/service_template >$HERE
#
# check if link exists
export THERE=/etc/systemd/system/oscforwarder.service
if [ -L "$THERE" ]; then
	echo "Removing exisiting link"
	rm "$THERE"
fi
# #
# create link
echo "creating service symlink and making service persistent"
ln -s "$HERE" "$THERE"
# echo "$HERE" "$THERE"
# initiate service
systemctl daemon-reload
service oscforwarder start
# make service persistent
systemctl enable oscforwarder
echo "installation script complete"
# 