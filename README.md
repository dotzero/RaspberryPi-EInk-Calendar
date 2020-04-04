# RaspberryPi EInk Calendar

![RaspberryPi EInk Calendar](preview.jpg)

# Подготовка

```bash
sudo raspi-config
# Choose Interfacing Options -> SPI -> Yes  to enable SPI interface
```

# Установка

```
sudo apt-get update
sudo apt-get install python3-pip python3-pil python3-numpy
git clone https://github.com/dotzero/RaspberryPi-EInk-Calendar.git
cd RaspberryPi-EInk-Calendar
sudo pip3 install -r requirements.txt
```

# Настройка доступов

```
cp settings_example.py settings.py
nano settings.py
```

# Настройка автоматического запуска

```bash
sudo cp pi-calendar.service /lib/systemd/system/pi-calendar.service
sudo chmod 644 /lib/systemd/system/pi-calendar.service
sudo systemctl daemon-reload
sudo systemctl enable pi-calendar.service
sudo reboot
```
