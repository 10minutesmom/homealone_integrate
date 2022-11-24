import requests

def send_sms(msg) :

    API_key = '2pq3omszojd4g9838hdtczxw2lh7roo2'

    payload = {
        "key": API_key,
        "user_id": 'kys2312',
        "sender": '01046552302',
        "receiver": '01046552302',
        "msg": msg,
        "testmode_yn":'Y'
    }

    try:
        response = requests.post('https://apis.aligo.in:443', data=payload)
        print(response.json())
        if(response.json()['result_code']!='1'):
            print("alert!! message didn't sent")
    except:
        print("alert message didn't sent")