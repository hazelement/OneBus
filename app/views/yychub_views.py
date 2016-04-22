from __future__ import print_function
import sys
import smtplib
import pandas as pd
import os

from app import app
from flask import render_template, jsonify, request, abort

#######
# functional urls

@app.route('/www.yychub.com.html', methods=['GET', 'POST'])
def ssl_check():
    return render_template('www.yychub.com.html')

@app.route('/site_map', methods=['GET', 'POST'])
def sitemap():
    print('getting sitemap', file=sys.stderr)
    return app.send_static_file('sitemap.xml')

#######



@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('yychub/index.html')

@app.route('/email/contact_me', methods=['GET', 'POST'])
def email():

    result={}
    result['success']=0
    result['message']='posting data error'

    try:
        post_data = request.get_json()


        name = post_data['name']
        email = post_data['email']  # it has gps data
        phone = post_data['phone']
        message = post_data['message']

        print(name, file=sys.stderr)
        print(email, file=sys.stderr)
        print(phone, file=sys.stderr)
        print(message, file=sys.stderr)

        send_email(name, email, phone, message)

        result['success']=1
        result['message']='success'

    except Exception, e:
        print(e, file=sys.stderr)
        abort(500)


    return jsonify(result)


def send_email(name, email, phone_number, message):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()

    msg = "\r\n".join([
                      "From: " + email,
                      "Subject: Feedback from " + email,
                      "",
                      "Name: " + name,
                      "Phone_number: " + phone_number,
                      message
                      ])

    email_config_file = os.path.dirname(os.path.realpath(__file__)) + '/email.config'
    email_config = pd.read_csv(email_config_file)
    user_email = email_config['email'].values[0]
    password = email_config['password'].values[0]

    server.login(user_email,password)
    server.sendmail(user_email, user_email, msg)
    server.quit()

if __name__ == "__main__":
    send_email("test","test@gmail.com", "123123", "this is a test message")