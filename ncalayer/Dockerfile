FROM dorowu/ubuntu-desktop-lxde-vnc:focal
ENV TZ=Asia/Almaty

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E88979FB9B30ACF2
RUN apt-get update 
RUN apt-get install -y default-jre
COPY ncalayer/ /ncalayer/
RUN apt-get install -y vim-common bsdmainutils libnotify-bin dunst dbus-x11


# /ncalayer/ncalayer/ncalayer.sh --run