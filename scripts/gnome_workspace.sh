#!/bin/bash

# Логирование начала выполнения с отметкой времени
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting workspace selection script" >> /tmp/workspace_selection.log

# Задержка для полной загрузки рабочего стола
sleep 10

# Установка на первый рабочий стол
xdotool set_desktop 0

# Определение размеров экрана
screen_width=$(xdotool getdisplaygeometry | cut -d ' ' -f 1)
screen_height=$(xdotool getdisplaygeometry | cut -d ' ' -f 2)

# Вычисление координат центра экрана
center_x=$((screen_width / 2))
center_y=$((screen_height / 2))

# Симуляция клика мыши в центре экрана
xdotool mousemove $center_x $center_y click 1

# Логирование завершения выполнения с отметкой времени
echo "$(date '+%Y-%m-%d %H:%M:%S') - Workspace selection script completed" >> /tmp/workspace_selection.log
