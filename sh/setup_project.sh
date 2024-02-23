#!/bin/bash

# Запустить сервисы
nohup ./10_start_goszakup.sh > /dev/null 2>&1 &
wait
