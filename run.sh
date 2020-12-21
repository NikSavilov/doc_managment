#!/bin/bash
python3 manage.py runserver 127.0.0.1:8000 &
python3 doc_managment/bot.py 