#!/usr/bin/env python3

import calendar
import configparser
import datetime
import imaplib
import os
import smtplib
import ssl
import sys
import time
from argparse import ArgumentParser
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    mailserver = config['mailserver']
    outbound = config['outbound']

    parser = ArgumentParser(description="""\
Send the mp3 that, when combined, make up the audio of a service for FBC.
""")
    parser.add_argument('-d', '--directory', required=True,
                        help="Mail the mp3's in the specified directory.")
    parser.add_argument('-c', '--count', type=int, required=True,
                        help='The number of parts the audio was split into.')
    parser.add_argument('-t', '--to_addresses',
                        default=outbound['to_addresses'],
                        help='Override the default destination')

    args = parser.parse_args()
    directory = args.directory
    to_addresses = args.to_addresses.split(",")
    no_of_files = args.count
    digits = len(str(no_of_files))

    if not os.path.isdir(directory):
        print("'%s' was not found" % (directory), file=sys.stderr)
        sys.exit(1)

    email_account = mailserver['email_account']
    password = mailserver['password']
    from_address = mailserver['from_address']
    imap_server = mailserver['imap_server']
    smtp_server = mailserver['smtp_server']

    today = datetime.date.today()
    sunday = today + datetime.timedelta((calendar.SUNDAY-today.weekday()) % 7)
    date_string = sunday.strftime('%B %d, %Y')
    base_filename = sunday.strftime('%Y-%m-%d') + ' Service Audio_'

    for file_number in range(no_of_files):
        filename = base_filename + str(file_number + 1).zfill(digits) + '.mp3'
        path = os.path.join(directory, filename)

        if not os.path.isfile(path):
            print(
                path + ' was not found... check that the file name is formatted correctly', file=sys.stderr)
            sys.exit(1)

    print("All %d files were found, about to email these addresses:" % (no_of_files))
    print(", ".join(to_addresses))
    print('pausing for second thoughts...')
    time.sleep(10)
    print()

    for file_number in range(no_of_files):
        filename = base_filename + str(file_number + 1).zfill(digits) + '.mp3'
        path = os.path.join(directory, filename)

        print("Sending '%s' now..." % (filename))

        subject = "FBC Service for %s - part %s of %s" % (
            date_string, str(file_number + 1), str(no_of_files))

        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = ", ".join(to_addresses)
        msg["Subject"] = subject

        body = "Part %s the mp3 of this week's service is attached." % str(
            file_number + 1)

        msg.attach(MIMEText(body, 'plain'))

        with open(path, 'rb') as attachment:
            payload = MIMEBase("application", "octet-stream")
            payload.set_payload(attachment.read())

        encoders.encode_base64(payload)  # encode the attachment

        # add payload header with filename
        payload.add_header('Content-Disposition',
                           'attachment', filename=filename)

        msg.attach(payload)

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
            server.login(email_account, password)
            server.send_message(msg, from_address, to_addresses)

        # Save the message to my sent folder
        with imaplib.IMAP4_SSL(imap_server, 993) as imap:
            imap.login(email_account, password)
            imap.append('Sent', '\\Seen', imaplib.Time2Internaldate(
                time.time()), msg.as_string().encode('utf8'))
            imap.logout()

        time.sleep(30)

    print('All files sent.')


if __name__ == '__main__':
    main()
