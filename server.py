from flask import Flask, request, jsonify
import json
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import pandas as pd

app = Flask(__name__)


@app.route("/")
def hello_world():
  return "Hello, World!"

@app.route('/new-reg', methods=['POST'])
def reg():
  request_data = request.json
  data_str = request_data['data']
  body = json.loads(data_str)
  fname = body['name'] + '_' + datetime.datetime.now().strftime("%Y-%m-%d")
  
  with open(fname, 'w', encoding='utf-8') as f:
    json.dump(body, f, ensure_ascii=False, indent=4)


  contacts = body['contactList']
  df = pd.DataFrame()
  for contact in contacts:
    df = df.append(contact, ignore_index = True)

  dct = {'name': body['name'], 'phone': body['number'], 'address': body['address']}
  df = df.append(dct, ignore_index = True)

  df.to_csv(fname + '.csv', index=False)
  send_test_mail(body['name'], fname + '.csv')
  
  resp = jsonify(success=True)
  return resp


def send_test_mail(name, fname):
    sender_email = "rdgurmeetsingh@gmail.com"
    receiver_email = "rdgurmeetsingh@gmail.com"
    password = "9855127173"

    msg = MIMEMultipart()
    msg['Subject'] = 'Contacts from - ' + name
    msg['From'] = sender_email
    msg['To'] = receiver_email

    msgText = MIMEText('Contacts from - ' + name)
    msg.attach(msgText)
        
    pdf = MIMEApplication(open(fname, 'rb').read())
    pdf.add_header('Content-Disposition', 'attachment', filename= fname)
    msg.attach(pdf)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(sender_email, password)
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(e)

app.run(host='0.0.0.0', port=5000)