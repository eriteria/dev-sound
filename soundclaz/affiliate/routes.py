# -*- coding: utf-8 -*-

from flask import Flask,render_template,request,redirect, Blueprint, url_for, flash, session, abort, jsonify
import sqlite3 as sql
import requests

# from site.routes import affiliate

affiliate = Blueprint('affiliate', __name__, url_prefix='/affiliate', template_folder='templates')


@affiliate.route('/',methods=['GET'])
def home():
    return render_template("site/affiliate.html")


@affiliate.route("/affiliate", methods=["POST"])
def affiliate_post():
    firstname = request.form.get("fname_aff")
    lastname = request.form.get("lname_aff")
    email_aff = request.form.get("email_aff")
    phone = request.form.get("phone_aff")
    username = request.form.get("username_aff")
    password = request.form.get("password_aff")
    confirm_password = request.form.get("c_password_aff")
    url = short(username)
    
    return f"{url}"



@affiliate.route('/shortener/<username>',methods=['GET','POST'],)
def short(username):
    custom = username
    longurl = "https://www.soundclaz.com"
    conn = sql.connect('urls.db')
    cursor = conn.cursor()
    #print cursor.execute("SELECT * FROM urls;")
    try:
        cursor.execute("INSERT INTO urls(longurl,custom) VALUES (?,?);", (str(longurl),str(custom)))
    except sql.Error as e:
        try:
            print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            return None
        except IndexError:
                print("MySQL Error: %s" % str(e))
                if str(e) == "no such table: urls":
                    cursor.execute("CREATE TABLE urls(longurl text not null, custom text primary key, clicks integer default 0);")
                    cursor.execute("INSERT INTO urls(longurl,custom) VALUES (?,?);", (str(longurl),str(custom)))
                    conn.commit()
                    return redirect(url_for('affiliate.home'))
                return None
        except TypeError as e:
            print(e)
            return None
        except ValueError as e:
            print(e)
            return None
    conn.commit()
    conn.close()
    url = "http://www.soundclaz.com/affiliate/"+custom

    return url

@affiliate.route('/affiliate/<custom>',methods=['GET','POST'])
def final(custom):

    conn = sql.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM urls WHERE custom=?;', (str(custom),))
    #return_this = cursor.fetchall()
    #return_this = [[str(item) for item in results] for results in cursor.fetchall()]
    for row in cursor.fetchall():
        # return_this= f"{request.host_url}affiliate/affiliate/{row[1]}"
        return_this = f"{request.host_url}contact/?ref={row[1]}"
        increment_click(row[1])

    return redirect(return_this,code=302)

# Increment the click count
def increment_click(ref_code):
    conn = sql.connect('urls.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM urls WHERE custom=?;', (str(ref_code),))
    for row in cursor.fetchall():
        clicks = row[2]
        clicks += 1
        cursor.execute('UPDATE urls SET clicks=? WHERE custom=?;', (clicks,ref_code))
    conn.commit()
    conn.close()




# if __name__ == '__main__':
#     app.run(port=5000)
