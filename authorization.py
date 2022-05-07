# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 22:14:29 2022

@author: Naresh Babu Nimmala
"""

import sqlite3
import hmac, base64, struct, hashlib, time
import os,json



class SQLiteDB(object):
  def __init__(self, db):
    self.conn = sqlite3.connect(db)
    self.conn.commit()
    self.cur = self.conn.cursor()

  def query(self, arg, vals = None):
    if (vals is not None) and (isinstance(vals,tuple)):
      self.cur.execute(arg, vals)
    else:
      self.cur.execute(arg)
    self.conn.commit()
    return self.cur

  def __del__(self):
    self.conn.close()


def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_dict_with_otp():
    auth_info = get_auth_info()
    result_dict = {}
    for item in auth_info:
        user_id = item['userid']
        password = item['password']
        secret = item['secret']
        if item['totp'] == 1:
            otp = get_hotp_token(secret, intervals_no=int(time.time())//30)
        else:
            otp = secret
        result_dict[user_id]={'password':password,'otp':otp}
    return result_dict

def get_auth_info():
    import os
    dbobj = SQLiteDB(os.path.join(config['db_path'],'main.db'))
    c = dbobj.query('select * from auth')
    records = list(c.fetchall())
    column_names = [item[0].lower() for item in c.description]
    result = [dict(zip(column_names, row)) for row in records]
    return result
with open("C:\\Users\\elp238\\OneDrive - Corteva\\Personal\\Algo_reengineered\\settings_app.json") as jf:
    config = json.loads(jf.read())
user_info = get_dict_with_otp()
print('user_info',user_info)
