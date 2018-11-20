#!/usr/bin/env python3

import imaplib

from os import getenv

from random import randint
import time
from time import sleep

import unicornhat as unicorn


# setup the unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.brightness(0.4)

# get the width and height of the hardware
width, height = unicorn.get_shape()


MAIL_REFRESH_INTERVAL = 10
BLINK_REFRESH_INTERVAL = 0.1

SMTP_SERVER = "imap.gmail.com"
FROM_EMAIL = ""
FROM_PWD = ""

def read_email_from_gmail():
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')
    unread_mails = len(mail.search(None, 'UnSeen')[1][0].split())
    return unread_mails


def clean_screen():
    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(x, y, 0, 0, 0)
            unicorn.show()


def random_blinks(blink_amount):
    for i in range(blink_amount):
        r = randint(30, 255)
        g = randint(30, 255)
        b = randint(30, 255)
        y = randint(0, height)
        x = randint(0, width)
        unicorn.set_pixel(x, y, r, g, b)
        unicorn.show()
    clean_screen()


if __name__ == "__main__":
    while True:
        unreadMails = read_email_from_gmail()
        now = int(time.time())
        stop_at = now + MAIL_REFRESH_INTERVAL
        while int(time.time()) < stop_at:
            random_blinks(unreadMails)
            sleep(BLINK_REFRESH_INTERVAL)
