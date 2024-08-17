Создать пользователя asus:  
sudo adduser asus  
sudo usermod -aG sudo asus  

Предоставить asus доступ без пароля:
sudo visudo
asus ALL=(ALL) NOPASSWD: ALL

Доступ к asus через ssh  
ssh-copy-id asus@185.23.108.189  

Установить Gnome:
sudo apt update
sudo apt install vim htop tmux git
sudo apt upgrade -y  
sudo reboot

tmux new -t pk
sudo apt update  
sudo apt install ubuntu-gnome-desktop -y && sudo reboot
tmux attach -t pk

Установить noMachine:
wget https://download.nomachine.com/download/8.13/Linux/nomachine_8.13.1_1_amd64.deb
sudo dpkg - i no

Установить chrome:
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg - i go

Установить gnome-software:
sudo apt install gnome-software

Отключить системные звуки:
gsettings set org.gnome.desktop.sound event-sounds false
