from __future__ import print_function

from app import app
from flask import render_template



@app.route('/www.yychub.com.html', methods=['GET', 'POST'])
def ssl_check():
    return render_template('www.yychub.com.html')

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('yychub/index.html')

