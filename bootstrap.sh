#!/usr/local/bin/zsh
export FLASK_APP=microblog.py
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export FLASK_DEBUG=0 # must be 0 for email
export MAIL_SERVER=localhost
export MAIL_PORT=8025
source ~/.virtualenvs/microblog/bin/activate
#flask run
