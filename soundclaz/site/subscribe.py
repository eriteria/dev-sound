from flask import Flask, render_template, url_for, request
from flask_mail import Message
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import hashlib
import re

from soundclaz.extensions import mail
from soundclaz.site.routes import site

mailchimp = MailchimpMarketing.Client()
mailchimp.set_config({
    "api_key": "388f584c02b12c3af9678e6c2810be67-us7",
    "server": "us7"
})

list_id = "a973ee931f"


@site.route('/subscribe', methods=['POST'])
def subscribe():
    msg = ''
    regex_normal = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex_custom = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    name = request.form['contactName']
    email = request.form['contactEmail'].lower()
    subject = request.form['contactSubject']
    body = request.form['contactMessage']
    if len(name) < 2:
        msg = "Please enter your full name."
    if not (re.search(regex_normal, email) or re.search(regex_custom, email)):
        msg = "Please enter a valid email address."
    if len(body) < 15:
        msg = "Please enter your message. It should have at least 15 characters."
    if not subject:
        subject = "Contact Form Submission"

    mess = Message(subject=subject, body=f"From {name} \n {email} \n" + body, sender="support@soundclaz.com",
                   recipients=["support@soundclaz.com"])

    member_info = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": {
            "CONNAME": name,
            "CONSUBJECT": subject,
            "CONBODY": body
        }
    }
    # save_user_t(name, email, body)
    hash_email = hashlib.md5(email.encode('utf-8')).hexdigest()
    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        if response['id'] == hash_email:
            msg = 'OK'
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        print("An exception occurred: {}".format(error.text))
        msg = f"An exception occurred: {error.text}"
    try:
        response = mailchimp.lists.update_list_member_tags(list_id, hash_email, body={
            "tags": [{
                "name": "Client",
                "status": "active"
            }]
        })
        response = mailchimp.lists.update_list_member_tags(list_id, hash_email, body={
            "tags": [{
                "name": "Subscriber",
                "status": "inactive"
            }]

        })
        if response is None:
            msg = "OK"
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        msg = f"An exception occurred: {error.text}"
    mail.send(mess)
    return msg

