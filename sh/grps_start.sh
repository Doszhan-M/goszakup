#!/bin/bash

source ~/github/goszakup/venv/bin/activate
cd ~/github/goszakup/
nohup python3 signer/main.py &
