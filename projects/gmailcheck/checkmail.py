#!/usr/bin/env python

import imaplib

from os import getenv

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

def read_email_from_gmail():

    mail = imaplib.IMAP4_SSL(getenv('SMTP_SERVER'))
    mail.login(getenv('FROM_EMAIL'), getenv('FROM_PWD'))
    mail.select('inbox')

    unread_mails = len(mail.search(None, 'UnSeen')[1][0].split())

    print(unread_mails)

read_email_from_gmail()
