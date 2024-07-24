#!/bin/bash

# Установка DISPLAY для доступа к X серверу
export DISPLAY=:0

source $HOME/github/goszakup/venv/bin/activate
cd $HOME/github/goszakup/
python3 signer/main.py
