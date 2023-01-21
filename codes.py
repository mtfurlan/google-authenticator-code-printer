#!/usr/bin/env python3

# read google authenticator database and output TOTP codes.
# /data/data/com.google.android.apps.authenticator2/databases/databases

#import qrcode
import sqlite3
import pyotp
from tabulate import tabulate
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(os.path.join(script_dir, 'databases'))
c = conn.cursor()

output = []
for idx, (email, secret, issuer) in enumerate(c.execute("SELECT email,secret,issuer FROM accounts").fetchall()):
    # if you want to make a QR code to import it elsewhere I guess this will do that?
    # https://gist.github.com/jbinto/8876658#gistcomment-1522362
    #url = 'otpauth://totp/{}?secret={}&issuer={}'.format(email, secret, issuer)
    #im = qrcode.make(url)
    #im.save('{}.png'.format(idx))
    totp = pyotp.TOTP(secret)
    code = totp.now()
    #print(f"{email}: {code}")
    output.append([email, code]);


print(tabulate(output, headers=['service', 'code']))
