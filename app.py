#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import smtplib #to send emails
# import regex as re

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

hst = 'localhost'
usr = 'root'
pwd = ''
app.debug = True
config = {'CACHE_TYPE': 'redis',
          'CACHE_REDIS_URL': 'redis://localhost:6379/3'}

app.secret_key = os.urandom(12)


#server object creation to send emails
def serve():
    #Email Notification Setup
    server = smtplib.SMTP('smtp.gmail.com',587) #server object
    server.ehlo()
    server.starttls()
    server.ehlo()
    #Login with sender_email_address on Chrome browser. Search less secure apps on chrome browser and on less secure apps' permission page, enable permission for sender_email_address.
    #server.login('sender_email_address','password')
    server.login('urhope.ngo@gmail.com','covid19farha') #authentication
    return server



#Database Connection
# def get_db():
#     db = pymysql.connect(host='localhost', user='root', passwd='CoronaPassword1.#',
#                          db='covid', charset='utf8mb4')
#     return db




def get_db():
    db = pymysql.connect(host='localhost', user='root', passwd='CoronaPassword.1#',
                         db='covid', charset='utf8mb4')
    return db



# Route for Base template
@app.route('/')
def base():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/team')
def team():
    return render_template('team.html')



@app.route('/form')
def form():
    return render_template('form.html')



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

        try:
            db = get_db()
            c = db.cursor()
            c.execute('select username from members where username = %s'
                      , username)
            account = c.fetchone()

            if account:
                flash('Email already exists please try again with another email!')
            else:

                if password == confirmpassword:
                    c.execute('insert into members (name, username, phone, pin, role, services, password ) values (%s, %s, %s, %s, %s, %s, md5(%s))'
                              , (
                        name,
                        username,
                        phone,
                        pincode,
                        role,
                        services,
                        password,
                        ))
                    db.commit()
                    # flash('Registered Successfully, Check your mail for confirmation!')
                    flash('Registered Successfully.')
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



@app.route('/<id>/', methods=['GET', 'POST'])
def profile(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if session['role'] == 'v':
            return render_template('volunteers_profile.html',
                                   id=session['user_id'])
        elif session['role'] == 'n':
            return render_template('ngo_profile.html',
                                   id=session['user_id'])
        else:
            return render_template('admin_profile.html',
                                   id=session['user_id'])



@app.route('/edit/<id>/', methods=['GET', 'POST'])
def edit_profile(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if session['role'] == 'v':
            return render_template('edit_profile_v.html',
                                   id=session['user_id'])
        elif session['role'] == 'n':
            return render_template('edit_profile_n.html',
                                   id=session['user_id'])
        else:
            return render_template('edit_profile_a.html',
                                   id=session['user_id'])



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

                flash("Sorry! You can't update.")
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
            email = session['username']
            about = session['about']
            connect = get_db()
            exe = connect.cursor()
            exe.execute('insert into task (task, grp, website, location, phone, vol_num, task_det, t_type, abt_grp, grp_email) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                        , (
                task,
                grp,
                website,
                pincode,
                phone,
                vol_num,
                task_det,
                t_type,
				about,
				email,
                ))
            connect.commit()
            exe.close()
            connect.close()
            flash('Task has been added successfully.')
            return render_template('create_task.html')
        else:
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
            db.commit()
            c.close()
            db.close()
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
            c.execute('SELECT * FROM application WHERE task_id = %s', id)
            data=c.fetchall()
            
            if len(data)!=0:
            	c.execute('DELETE FROM applications WHERE task_id = %s', id)
            
            db.commit()
            c.close()          
            db.close()

            x="Task with ID "+str(id)+" has been deleted successfully. If you had any volunteer applied for this task their application has also been deleted."
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
        db.commit()
        c.close()          
        db.close()
        return render_template('task_list_n.html',len=len(data), data=data) 
    
    elif session['role'] == 'v':
        # pin = session['pin']
        db = get_db()
        c = db.cursor()
		# c.execute('SELECT * FROM task WHERE location = %s', pin)
        c.execute('SELECT * FROM task ORDER BY location ASC')
        data = c.fetchall()

        c.execute('SELECT task_id,vol_id FROM application ORDER BY task_id ASC')
        app_data = c.fetchall()

        id=session['user_id']
		
        db.commit()
        c.close()
        db.close()

        applied=[]
        for i in app_data:
            if i[1]==session['user_id']:
                applied.append(i[0])

        print(applied)

        return render_template('task_list_v.html', id=id,l=len(app_data),applied=applied,len=len(data),data=data, app_data=app_data)
    else:
        return redirect(url_for('login'))  



@app.route('/apply/<id>/', methods=['GET', 'POST'])
def apply_task(id):
    id=id
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    db = get_db()
    c = db.cursor()
    server=serve()

    c.execute('SELECT * FROM application WHERE vol_email=%s',session['username'])
    data = c.fetchall()
	
    if len(data) >= 2:
        db.commit()
        c.close()
        db.close()
        flash("You can't apply for this task. You can volunteer maxmimum for 2 tasks at a time."
          )
        return redirect(url_for('task_list'))

    c.execute('SELECT * FROM task where id=%s',id)
    data = c.fetchall()
	
    if data[0][11] < data[0][7]:
        
        val = data[0][11]+1

        c.execute('UPDATE task SET vol_applied=%s WHERE id=%s',(val,id))
        c.execute('INSERT INTO application(grp_email,vol_email,task_id,vol_id,grp_name,vol_name,task_name,vol_phone) values(%s,%s,%s,%s,%s,%s,%s,%s)',(data[0][12],session['username'],data[0][0],session['user_id'],data[0][3],session['name'],data[0][1],session['phone']))        
        db.commit()
        c.close()
        db.close()
        
        subject = "Notification from URHope Team"
        body="Dear "+data[0][3]+",\n\n"+ session['name'] +" has applied for the task "+ data[0][1]+" which has an ID: "+str(data[0][0])+".\n\nSo far the total number of applicaion for this task is " + str(val)+" and "+str(data[0][7]-val)+" more volunteers are required.\n\nClick on the link for more details,\nhttp://www.urhope.in\n\n\nRegards,\nURHope Team"
        msg=f"Subject: {subject}\n\n{body} "

        server.sendmail(
						'ur_hope_email_address', #email ID of URHope or use your email ID for testing
						str(data[0][12]), #email id of receiver ie. data[0][12], NGO's email ID or use any other known email ID for testing
						msg
						)
		
        if(val==data[0][7]):
            body= "Dear "+data[0][3]+",\n\nFor the task "+data[0][1]+", you have sufficient volunteers. Now you can proceed for further steps.\n\n\nRegards,\nURHope Team"
            msg=f"Subject: {subject}\n\n{body} "
            server.sendmail(
							'urhope_email_address', 
							str(data[0][12]), 
							msg
							)
        server.quit()
								
        flash("Applied Successfully")
        return redirect(url_for('task_list'))
        
    else:
        db.commit()
        c.close()
        db.close()
        x="Thank You "+session['name']+"!\nThere are sufficient volunteers available for this task. Try applying for some other task."
        flash(x)
        return redirect(url_for('task_list'))



@app.route('/notification_page/', methods=['GET', 'POST'])
def notification_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM application WHERE grp_email=%s ORDER BY id DESC',session['username'])
    data = c.fetchall()
    db.commit()
    c.close()
    db.close()
    return render_template('notification_page.html',len=len(data),data=data)



@app.route('/how_is_the_task/<id>/', methods=['GET', 'POST'])
def how_is_the_task(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id=id
    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM task WHERE id=%s',id)
    data = c.fetchall()
    db.commit()
    c.close()
    db.close()
	# print(data)

    x = "Hey "+session['name']+",for the task '"+data[0][1]+"', total number of applications are "+ str(data[0][11])+". You need "+str(data[0][7] - data[0][11])+" more volunteer to start the task."
    flash(x)

    return redirect(url_for('notification_page'))



@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        if session['role'] == 'v':
            return render_template('home.html')
        elif session['role'] == 'n':
            return render_template('home.html')
        else:
            return render_template('home.html')



@app.route('/search/<pincode>/', methods=['GET'])
def search_pincode(pincode):
    connect = get_db()
    pincode = int(pincode)
    c = connect.cursor()
    counter = 0
    where = ""
    for i in [0,-1,+1,-2,+2,-3,+3,-4,+4]:
        where += "m.pin='"+str(pincode+i) + "' OR "
    query = "select m.pin, phone, services, statename from members m join podata p on m.pin = p.pin where m.role='n' AND (" + where[:-4] +")"
    c.execute(query)
    data = c.fetchall()
    if data:
        c.close()
        connect.close()
        return render_template('home.html', data=data)
    return render_template('home.html',data={})



@app.route('/searchresult',methods=['GET','POST'])
def serch_result():
    if request.method=="POST":
        name = request.form['name']
        pin = request.form['pin']
        lpin=len(pin)
        low_name = name.lower()
        role='n'

        if lpin==6:
            pin = int(pin)
            pin=pin
            db = get_db()
            c = db.cursor()
            c.execute('SELECT * FROM members WHERE services=%s and pin=%s and role=%s ORDER BY pin ASC',(name,pin,role))
            data = c.fetchall()
            l=len(data)
            db.commit()
            c.close()
            db.close()
            if(l>0):
                return render_template('searched.html',l=l,data=data,name=low_name)
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))


@app.route('/helpline')
def helpline():
    return render_template('helpline.html')



@app.route('/test')
def test():

    return "This is a testing route"


if __name__ == '__main__':
    app.run()  # host='0.0.0.0', port=5000