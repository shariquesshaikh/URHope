#!/usr/bin/python
# -*- coding: utf-8 -*-
# My virtual Env : source ../covid/covid_app/venv/Scripts/activate

from __future__ import print_function

from flask import Flask, render_template, redirect, url_for, request, g
from flask import session, abort, flash, jsonify

# from flask_sslify import SSLify
# from flask_caching import Cache
# from flask_mysqlpool import MySQLPool

import json
import os
import datetime
import pymysql
import requests
import socket
import os.path
import flask
import re
import urllib.request
import logging
import string
import random

# import regex as re

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# hst = "";
# m_hst = "";
# usr = "";
# pwd = "";

# if(ip.startswith("94.237")):
#     hst = "10.2.10.122"
#     m_hst = "10.2.9.157"
#     usr = "root"
#     pwd = "Admin.902.14"
#     app.debug = False
#     config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://10.2.2.183:6379/0'}
#     app.config['MYSQL_HOST'] = hst
#     app.config['MYSQL_PORT'] = 3306
#     app.config['MYSQL_USER'] = usr
#     app.config['MYSQL_PASS'] = pwd
#     app.config['MYSQL_DB'] = 'twitics'
#     app.config['MYSQL_POOL_NAME'] = 'mysql_pool'
#     app.config['MYSQL_POOL_SIZE'] = 32
#     app.config['MYSQL_AUTOCOMMIT'] = True
#     #sys.path.append('/root/miniconda2/lib/python2.7/site-packages') # Replace this with the place you installed facebookads using pip
#     #sys.path.append('/root/miniconda2/lib/python2.7/site-packages/facebook_business-3.0.0-py2.7.egg-info') # same as above
#     print("Running in production mode")

# else:

hst = 'localhost'
usr = 'root'
pwd = ''
app.debug = True
config = {'CACHE_TYPE': 'redis',
          'CACHE_REDIS_URL': 'redis://localhost:6379/3'}

app.secret_key = os.urandom(12)


def get_db():
    db = pymysql.connect(host='localhost', user='root', passwd='',
                         db='covid', charset='utf8mb4')
    return db


# Route for Base template

@app.route('/')
def base():
    return render_template('home.html')


@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST' and 'username' in request.form \
        and 'password' in request.form and 'role' in request.form \
        and 'confirm' in request.form:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirm']
        pincode = request.form['pincode']
        phone = request.form['phone']
        role = request.form['role']

        # address = request.form['address']

        services = request.form['services']
        govtID = request.form['govtID']
        website = request.form['website']
        social = request.form['social']
        about = request.form['about']

        print(username, password, confirmpassword, role)
        try:
            db = get_db()
            c = db.cursor()
            c.execute('select username from members where username = %s'
                      , username)
            account = c.fetchone()

            if account:
                flash('Email already exists please try again with another email!'
                      )
            else:

                if password == confirmpassword:
                    c.execute('insert into members (name, username, phone, pin, role, services, govtID, website, social, about, password ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, md5(%s))'
                              , (  # address
                        name,
                        username,
                        phone,
                        pincode,
                        role,
                        services,
                        govtID,
                        website,
                        social,
                        about,
                        password,
                        ))
                    db.commit()
                    c.close()
                    db.close()
                    return redirect(url_for('login'))
                else:
                    flash('Passwords do not match!')
        except Exception as e:

            print(e)

        return render_template('register.html')
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form \
        and 'password' in request.form:
        try:
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            c = db.cursor()
            c.execute('select id,name, username, password, role, phone, pin, regno, age, sex, currProfile, address, social, services, branch, about, govtID,website from members where username = %s and password = md5(%s)'
                      , (username, password))
            account = c.fetchone()
            if account is not None:
                session['logged_in'] = True
                session['user_id'] = account[0]
                session['username'] = account[2]
                session['name'] = account[1]
                session['role'] = account[4]
                session['pin'] = account[6]
                session['phone'] = account[5]
                session['regno'] = account[7]
                session['age'] = account[8]
                session['sex'] = account[9]
                session['currProfile'] = account[10]
                session['address'] = account[11]
                session['social'] = account[12]
                session['services'] = account[13]
                session['branch'] = account[14]
                session['about'] = account[15]
                session['govtID'] = account[16]
                session['website'] = account[17]

                return redirect(url_for('home'))
            else:
                flash('Invalid Username or Password')
                return render_template('login.html')
        except Exception as e:
            print(e)

        return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():

    # Remove session data, this will log the user out

    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)

   # Redirect to login page

    return redirect(url_for('login'))


@app.route('/<username>/', methods=['GET', 'POST'])
def profile(username):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if session['role'] == 'v':
            return render_template('volunteers_profile.html',
                                   username=session['username'])
        elif session['role'] == 'n':
            return render_template('ngo_profile.html',
                                   username=session['username'])
        else:
            return render_template('admin_profile.html',
                                   username=session['username'])


@app.route('/edit/<username>/', methods=['GET', 'POST'])
def edit_profile(username):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if session['role'] == 'v':
            return render_template('edit_profile_v.html',
                                   username=session['username'])
        elif session['role'] == 'n':
            return render_template('edit_profile_n.html',
                                   username=session['username'])
        else:
            return render_template('edit_profile_a.html',
                                   username=session['username'])


@app.route('/update/<uname>/', methods=['GET', 'POST'])
def update_pro(uname):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
            username = session['username']
            role = session['role']

            if role == 'V' or role == 'v':

                if request.method == 'POST' and 'name' in request.form \
                    and 'pin' and request.form and 'phone' in request.form \
                    and 'address' in request.form and 'about' in request.form:
                    name = request.form['name']
                    pincode = request.form['pin']
                    phone = request.form['phone']
                    address = request.form['address']
                    about = request.form['about']

                    connect = get_db()
                    exe = connect.cursor()

                    exe.execute('UPDATE members SET name=%s,pin=%s, phone=%s,address=%s,about=%s WHERE username = %s '
                                , (
                        name,
                        pincode,
                        phone,
                        address,
                        about,
                        username,
                        ))
                    connect.commit()

                    exe.close()
                    connect.close()
                    return redirect(url_for('logout'))
                else:
                    flash('Profile was not updated')
                    return redirect(url_for('home'))
            elif role == 'n' or role == 'N':

                if request.method == 'POST' and 'name' in request.form \
                    and 'website' in request.form and 'social' in request.form \
                    and 'services' in request.form and 'address' \
                    in request.form and 'regno' in request.form and 'branch' \
                    in request.form and 'phone' in request.form and 'pin' \
                    in request.form and 'about' in request.form:
                    name = request.form['name']
                    website = request.form['website']
                    social = request.form['social']
                    services = request.form['services']
                    address = request.form['address']
                    regno = request.form['regno']
                    branch = request.form['branch']
                    phone = request.form['phone']
                    pin = request.form['pin']
                    about = request.form['about']

                    connect = get_db()
                    exe = connect.cursor()

                    exe.execute('UPDATE members SET name=%s,website=%s, social=%s,services=%s,address=%s,regno=%s,branch=%s,phone=%s,pin=%s,about=%s WHERE username = %s '
                                , (
                        name,
                        website,
                        social,
                        services,
                        address,
                        regno,
                        branch,
                        phone,
                        pin,
                        about,
                        username,
                        ))
                    connect.commit()

                    exe.close()
                    connect.close()

                    return redirect(url_for('logout'))
                else:
                    flash('Profile was not updated')
                    return redirect(url_for('home'))
            else:

                    # flash("Unrecognized User")

                return redirect(url_for('login'))


@app.route('/create-task', methods=['GET', 'POST'])
def create_task():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif session['role'] == 'n':
        if request.method == 'POST':
            task = request.form['task']
            grp = request.form['grp']
            website = request.form['website']
            phone = request.form['phone']
            vol_num = request.form['vol_num']
            pincode = request.form['pin']
            task_det = request.form['task_det']
            t_type = request.form['t_type']
            connect = get_db()
            exe = connect.cursor()
            exe.execute('insert into task (task, grp, website, location, phone, vol_num, task_det, t_type) values (%s, %s, %s, %s, %s, %s, %s, %s)'
                        , (
                task,
                grp,
                website,
                pincode,
                phone,
                vol_num,
                task_det,
                t_type,
                ))
            connect.commit()
            exe.close()
            connect.close()
            flash('Task has been added')
            return render_template('create_task.html')
        else:
            flash("Task was not added. Try again")
            return render_template('create_task.html')
    else:
            flash("Task was not added. Try again")
            return render_template('create_task.html')


@app.route('/edit-task/<id>/', methods=['GET', 'POST'])
def edit_task(id):
    id=id
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif session['role'] == 'n':
        if request.method == 'POST':
            task = request.form['task']
            grp = request.form['grp']
            website = request.form['website']
            phone = request.form['phone']
            vol_num = request.form['vol_num']
            pincode = request.form['pin']
            task_det = request.form['task_det']
            t_type = request.form['t_type']

            connect = get_db()
            exe = connect.cursor()
            exe.execute('UPDATE task SET task=%s, grp=%s, website=%s, location=%s, phone=%s, vol_num=%s, task_det=%s, t_type=%s where id= %s'
                        , (
                task,
                grp,
                website,
                pincode,
                phone,
                vol_num,
                task_det,
                t_type,
                id,

                ))
            connect.commit()
            exe.close()
            connect.close()
            flash('Task has been updated')
            return redirect(url_for('task_list'))
        else:
            db = get_db()
            c = db.cursor()
            c.execute('SELECT * FROM task WHERE id = %s', id)
            data = c.fetchall()
            c.close()
            db.close()
            print(data)
            return render_template('edit_task.html',data=data)
    else:
        return redirect(url_for('home'))


@app.route('/delete-task/<id>/')
def delete_task(id):
    id=id
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif session['role'] == 'n':
            db = get_db()
            c = db.cursor()
            c.execute('DELETE FROM task WHERE id = %s', id)
            c.close()          
            db.close()

            x="Task with ID "+str(id)+" has been deleted successfully"
            flash(x)

            return redirect(url_for('task_list'))
    else:
            flash("Task was not deleted")
            return redirect(url_for('task_list'))
 

@app.route('/task_list')
def task_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    elif session['role'] == 'n':    
        grp_name = session['name']
        db = get_db()
        c = db.cursor()
        c.execute('select * from task where grp = %s', grp_name)
        data = c.fetchall()
        c.close()          
        db.close()
        return render_template('task_list_n.html', len=len(data),data=data) 
    
    elif session['role'] == 'v':

        pin = session['pin']
        db = get_db()
        c = db.cursor()
        c.execute('SELECT * FROM task WHERE location = %s', pin)
        data = c.fetchall()
        c.close()
        db.close()

        return render_template('task_list_v.html', len=len(data), data=data)
    else:
        return redirect(url_for('login'))  


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if session['role'] == 'v':
            return render_template('volunteers_home.html')
        elif session['role'] == 'n':
            return render_template('ngo_home.html')
        else:
            return render_template('admin_home.html')


@app.route('/test')
def test():
    return "It is a test function"

if __name__ == '__main__':
    app.run()  # host='0.0.0.0', port=5000
