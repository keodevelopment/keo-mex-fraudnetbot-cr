from flask import Flask
from selenium import webdriver
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import smtplib
from email.mime.multipart import MIMEMultipart
import time 
import pandas as pd
#from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager




app = Flask(__name__)


@app.route("/")
def hello_bot():
    recipients = ['seandaza@gmail.com']
    msg = MIMEMultipart()
    # setup the parameters of the message
    password = "kvjxjjghzpqfdpcd"
    msg['From'] = "jhand@keoworld.com"
    msg['Subject'] = "FraudnetBot Alert: new report(s) found"
    msg['To'] = "seandaza@gmail.com"

    msg.attach(MIMEText('New Report Found: '))


    # create server
    server = smtplib.SMTP('smtp.outlook.com: 587')
    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)

    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    return "Done"
