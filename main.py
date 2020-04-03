#!/usr/bin/python
# -*- coding:utf-8 -*-

import settings
import time
import epd2in13
import humanize
import textwrap
import traceback
from datetime import timedelta
from exchangelib import DELEGATE, Account, Credentials, Configuration, EWSDateTime, EWSTimeZone
from exchangelib.errors import UnauthorizedError
from PIL import Image, ImageDraw, ImageFont

humanize.i18n.activate("ru_RU")


def main():
    epd = epd2in13.EPD()
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)

    old_delta = None

    while True:
        try:
            delta, start, subject = next_meeting()
            print('{} - {} - {}'.format(delta, start, subject))

            if old_delta != delta:
                old_delta = delta
                image = get_image(delta, start, subject)
                # image.save("image.png", "PNG")
                epd.display(epd.getbuffer(image.rotate(180)))

            time.sleep(5 * 60)
        except UnauthorizedError as err:
            print("UnauthorizedError: {0}".format(err))
            return
        except (KeyboardInterrupt, SystemExit):
            return
        except:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            time.sleep(60)


def get_image(delta, start, subject):
    image = Image.new('1', (settings.EPD_WIDTH, settings.EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(image)

    draw.rectangle([(5, 5), (settings.EPD_WIDTH - 5, settings.EPD_HEIGHT - 5)], outline=0)

    regular = ImageFont.truetype(settings.FONTS_DIR + 'Hack-Regular.ttf', 15)
    bold = ImageFont.truetype(settings.FONTS_DIR + 'Hack-Bold.ttf', 22)

    # delta
    draw.text((10, 10), delta, font=regular, fill=0)

    # time
    size = draw.textsize(start, font=regular)
    draw.text((settings.EPD_WIDTH - size[0] - 10, 10), start, font=regular, fill=0)

    # multiline subject
    lines = textwrap.wrap(subject, width=17)
    y_text = 48
    for line in lines:
        width, height = bold.getsize(line)
        draw.text((10, y_text), line, font=bold, fill=0)
        y_text += height

    return image


def next_meeting():
    credentials = Credentials(username=settings.USERNAME, password=settings.PASSWORD)
    config = Configuration(server=settings.SERVER, credentials=credentials)
    account = Account(
        primary_smtp_address=settings.EMAIL,
        autodiscover=False,
        config=config,
        access_type=DELEGATE
    )

    tz = EWSTimeZone.timezone('Europe/Moscow')
    now = tz.localize(EWSDateTime.now())

    items = account.calendar.view(start=now, end=now + timedelta(days=1))
    if len(items) == 0:
        return ("", "", "     ~(^-^)~")

    item = items[0]
    start = item.start.astimezone(tz)

    return (
        humanize.naturaltime(now - start),
        start.strftime("%H:%M"),
        item.subject
    )


if __name__ == "__main__":
    main()
