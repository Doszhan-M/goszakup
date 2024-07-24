#!/bin/bash

source $HOME/github/goszakup/venv/bin/activate
cd $HOME/github/goszakup/
nohup python3 signer/main.py &
