import email
from email import message
from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app, flash
from flask_mail import Message
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import hashlib
import re

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# from soundclaz.models import db
from soundclaz.extensions import mail

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = "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"
api_instance_send_emails = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
api_instance_email_campaigns = sib_api_v3_sdk.EmailCampaignsApi(sib_api_v3_sdk.ApiClient(configuration))


site = Blueprint('main_site', __name__, url_prefix="/")
mailchimp = MailchimpMarketing.Client()
mailchimp.set_config({
    "api_key": "388f584c02b12c3af9678e6c2810be67-us7",
    "server": "us7"
})

list_id = "a973ee931f"


@site.route("/sitemap")
def sitemap():
    return render_template("sitemap.xml")
    

@site.route('/robots.txt')
@site.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@site.route("/")
def index():
    return render_template("site/index.html")


# @site.route("/contact")
# def contact():
#     return render_template("site/contacts.html")

@site.route("/contact/")
def contact():
    ref_code = request.args.get('ref')
    return render_template("site/contacts.html", ref_code=ref_code)


@site.route("/affiliate", methods=["GET"])
def affiliate():
    return redirect(url_for("affiliate.home"))

    

@site.route("/portfolio")
def portfolio():
    return render_template("site/portfolio.html")


@site.route("/design")
def design():
    return redirect(url_for('main_site.digital'))
#

@site.route("/video")
def video():
    return redirect(url_for('main_site.digital'))


@site.route("/advertisement")
def guerrilla():
    return render_template("site/advertisement.html")


@site.route("/product")
def product():
    return render_template("site/product-innovation.html")


@site.route("/totem")
def totem():
    return redirect(url_for('main_site.guerrilla'))


@site.route("/digital")
def digital():
    return render_template("site/digital-services.html")


@site.route("/about")
def about():
    return render_template("site/about.html")


# Methods for accepting forms :)
@site.route("/new_project", methods=["POST"])
def new_project():
    name = request.form.get("project-name")
    email = request.form.get("project_email")
    company = request.form.get("project-company")
    title = request.form.get("project-title")
    details = request.form.get("project_details")
    data = request.form.get("data-slider")
    ref_code = request.form.get("referal-code")
    subject = "Thank you for contacting us"
    html_content = "<html><body><h1>This is my first transactional email </h1></body></html>"
    sender = {"name": "no-reply", "email": "noreply@soundclaz.com"}
    to = [{"email": email, "name": name}]
    reply_to = {"email": "support@soundclaz.com", "name": "Soundclaz Support"}
    headers = {"Some-Custom-Name": "unique-id-1234"}
    params = {"parameter": "My param value", "subject": "New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, template_id=2,headers=headers,
                                                   html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance_send_emails.send_transac_email(send_smtp_email)
        print(api_response)

    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    req = {'Name': name, "Email": email, "Company": company, "Title": title, "Details": details, "Data": data, "Ref_code": ref_code}
    cond = save_to_mongo(req)

    return redirect(url_for('main_site.contact'))


def save_to_mongo(req):
    from pymongo import MongoClient

    from pprint import pprint

    client = MongoClient("mongodb+srv://soundclaz:4QKPPB51ahananD6@cluster0.jksss.mongodb.net/soundclaz_affiliates?retryWrites=true&w=majority")

    # try:
    #     print(client.server_info())
    # except Exception:
    #     print("Unable to connect to the server.")

    db = client.cluster0
    projects = db.projects

    try:
        project_id = projects.insert_one(req).inserted_id
        return project_id
    except Exception:
        return None


@site.route("/enquiries", methods=["POST"])
def enquiries():
    msg = ''
    regex_normal = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex_custom = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    name = request.form.get("enquiry-name")
    email = request.form.get("enquiry-email")
    company = request.form.get("enquiry-company")
    subject = request.form.get("enquiry-subject")
    body = request.form.get("enquiry-details")
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
    flash(msg)
    return redirect(url_for("main_site.contact"))




@site.route('/subscribe', methods=['POST'])
def subscribe():
    msg = ''
    regex_normal = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regex_custom = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    name = request.form['contactName']
    email = request.form['subscribe-email'].lower()
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
    flash(msg)
    return redirect(url_for("main_site.contact"))
