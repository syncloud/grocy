#!/bin/bash -e

apt-get update
apt-get install -y sshpass openssh-client netcat file build-essential libz-dev curl
pip install -r requirements.txt
