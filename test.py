import requests
import os,time
import authorization
from datetime import datetime
import subprocess

login_info = authorization.user_info
temp_path = authorization.config['temp_path']
print('path',temp_path)
chat_token = authorization.config['chat_token']
chat = authorization.config['chat']
to_date_st=datetime.now()
token = authorization.config['NiftyToken']
try:
    for key,value in login_info.items():
        for filename in os.listdir(temp_path):
            if filename.startswith(key):
                with open(os.path.join(temp_path,filename), 'r') as tf:
                    authorization = tf.read()
        if token:
            api_st = "https://kite.zerodha.com/oms/instruments/historical/{0}/{1}?user_id={2}&oi=1&from={3}&to={4}&ciqrandom={5}"
            api_st=api_st.format(token,"15minute",key,to_date_st.strftime("%Y-%m-%d"),to_date_st.strftime("%Y-%m-%d"),time.time())
            response = requests.get(api_st,headers={'Content-Type':'application/json','authorization':authorization})
            chat_message = "response " + str(response.status_code)
            chat_url = f'https://api.telegram.org/bot{chat_token}/sendMessage?chat_id={chat}&text={chat_message}'
            requests.get(chat_url)
            if response.status_code == 403:
                chat_message = "token expired or lost, regenerating"
                os.system("python login.py")
                chat_url = f'https://api.telegram.org/bot{chat_token}/sendMessage?chat_id={chat}&text={chat_message}'
                chat_message = "token successfully regenerated, reexecuting the current script"
                chat_url = f'https://api.telegram.org/bot{chat_token}/sendMessage?chat_id={chat}&text={chat_message}'
                os.system("python test.py")

        else:
            print('inside else')

except Exception as e:
    print(str(e))
    chat_message = "Exception Reason : " + str(e)
    chat_url = f'https://api.telegram.org/bot{chat_token}/sendMessage?chat_id={chat}&text={chat_message}'
