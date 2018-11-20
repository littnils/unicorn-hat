#!/usr/bin/env python3

import imaplib

import threading

from random import randint

import time

import unicornhat as unicorn


# setup the unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.brightness(0.4)

# get the width and height of the hardware
width, height = unicorn.get_shape()


MAIL_REFRESH_INTERVAL = 10
BLINK_REFRESH_INTERVAL = 1

MIN_RGB = 40
MAX_RGB = 255

SMTP_SERVER = "imap.gmail.com"
FROM_EMAIL = ""
FROM_PWD = ""

mails = 0

def read_email_from_gmail():
    global mails
    while True:
        print("checking gmail...")
        for attempt in range(20):
            try:
                mail = imaplib.IMAP4_SSL(SMTP_SERVER)
                mail.login(FROM_EMAIL, FROM_PWD)
                mail.select('inbox')
                unread_mails = len(mail.search(None, 'UnSeen')[1][0].split())
            except:
                print("attempt " + str(attempt) + " failed, trying again...")
            else:
                break
        print(unread_mails)
        mails = unread_mails
        time.sleep(MAIL_REFRESH_INTERVAL)


def bootup():
    for y in range(height):
        for x in range(width):
            r = randint(MIN_RGB, MAX_RGB)
            g = randint(MIN_RGB, MAX_RGB)
            b = randint(MIN_RGB, MAX_RGB)
            unicorn.set_pixel(x, y, r, g, b)
            unicorn.show()
            time.sleep(0.1)
    time.sleep(2)
    clean_screen()


def clean_screen():
    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(x, y, 0, 0, 0)
            unicorn.show()


def random_blinks():
    global mails
    print("starting random blinks")
    while True:
        print("mails is " + str(mails))
        for i in range(mails):
            r = randint(MIN_RGB, MAX_RGB)
            g = randint(MIN_RGB, MAX_RGB)
            b = randint(MIN_RGB, MAX_RGB)
            y = randint(0, height)
            x = randint(0, width)
            unicorn.set_pixel(x, y, r, g, b)
            unicorn.show()
        clean_screen()
        time.sleep(BLINK_REFRESH_INTERVAL)


if __name__ == "__main__":
    bootup()
    t1 = threading.Thread(target = random_blinks)
    t2 = threading.Thread(target = read_email_from_gmail)

    t1.start()
    t2.start()


