#!/bin/bash

echo "Starting workspace selection script" >> /tmp/workspace_selection.log
sleep 10
xdotool set_desktop 0

screen_width=$(xdotool getdisplaygeometry | cut -d ' ' -f 1)
screen_height=$(xdotool getdisplaygeometry | cut -d ' ' -f 2)

center_x=$((screen_width / 2))
center_y=$((screen_height / 2))

xdotool mousemove $center_x $center_y click 1
echo "Workspace selection script completed" >> /tmp/workspace_selection.log
