#!/bin/bash

sleep 10
xdotool set_desktop 0

# Определить размеры экрана
screen_width=$(xdotool getdisplaygeometry | cut -d ' ' -f 1)
screen_height=$(xdotool getdisplaygeometry | cut -d ' ' -f 2)

# Вычислить координаты центра экрана
center_x=$((screen_width / 2))
center_y=$((screen_height / 2))

# Симулировать клик мыши в центре экрана
xdotool mousemove $center_x $center_y click 1
