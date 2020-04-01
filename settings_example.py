import platform

# Microsoft Exchange Server
SERVER = 'exchange.domain.ru'
USERNAME = 'domain\\login'
PASSWORD = 'secretP@$$'
EMAIL = 'login@domain.ru'

# Display resolution
EPD_HEIGHT = 122
EPD_WIDTH = 250

# Fonts
FONTS_DIR = '/usr/share/fonts/truetype/hack/'
if platform.system() == 'Darwin':
    FONTS_DIR = './ttf/'
