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
import pandas as pd
import time 
#from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager




app = Flask(__name__)




@app.route("/")
def hello_bot():
    #gecko driver manager
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--window-size=1920x1080")
    firefox_options.add_argument("--disable-gpu")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    firefox_options.add_argument("--disable-extensions")
    
    #driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)

    now = datetime.now() 
    year_month_day = now.strftime("%Y-%m-%d")

    #set url feed for login
    url = 'https://network.americanexpress.com/globalnetwork/v4/sign-in/'

    payload={
        "Email": 'anastasiareyes1987',
        "Password": 'Casa1234??'
    }


    #Navigate to the page
    driver.get(url)
    driver.maximize_window()



    user_ID = driver.find_element("xpath", "//*[@id='userid']")
    user_ID.send_keys(payload['Email'])

    password = driver.find_element("xpath", "//*[@id='password']")
    password.send_keys(payload['Password'])
    print("password")
    time.sleep(2)

    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(1)

                                                
    signin_button = driver.find_element("xpath", '//*[@id="submit"]')
    signin_button.click()
    time.sleep(1)

    #Go to FraudNet Reports
    #Link only for 'Active' status reports
    new_url = "https://gnsfraudnet.americanexpress.com/fraudnet/#/ior/new"
    #implicit wait
    print("go to the url")
    driver.implicitly_wait(180)


        #send email
        # create message object instance
    recipients = ['seandaza@gmail.com']#'anastasiar@keoworld.com','carlosr@keoworld.com','carlosb@keoworld.com','ricardof@keoworld.com','armandoi@keoworld.com','luist@keoworld.com','edissonv@keoworld.com','erikab@keoworld.com', 'jhand@keoworld.com']
    for elm in recipients:
        msg = MIMEMultipart()
        # setup the parameters of the message
        password = "kvjxjjghzpqfdpcd"
        msg['From'] = "jhand@keoworld.com"
        msg['Subject'] = "FraudnetBot Alert: new report(s) found"
        msg['To'] = f"{elm}"
        
        # attach image and text to message body
        for i in range(len(indices)):
            msg.attach(MIMEText('New Report Found: '+ '\n' +
            'CM NUMBER:' + '\t' + str(valores[i][0]).replace("'",'') + '\n' +
            'TOKEN NUMBER:' + '\t' + str(valores[i][1]).replace("'",'') + '\n' +
            'TIME OF TRANSACTION:' + '\t' + str(valores[i][2]).replace("'",'') + '\n' +
            'AMOUNT (USD):' + '\t' + str(valores[i][3]).replace("'",'') + '\n' +
            'SE NUMBER:' + '\t' + str(valores[i][4]).replace("'",'') + '\n' +
            'SE NAME:' + '\t' + str(valores[i][5]).replace("'",'') + '\n' +
            'RULE NUMBER:' + '\t' + str(valores[i][6]).replace("'",'') +'\n' +
            '------------------------------------------------------------------'+
            '\n\n'))
        msg.attach(MIMEImage(open('new_report.png', 'rb').read()))
        
        # create server
        server = smtplib.SMTP('smtp.outlook.com: 587')
        server.starttls()
        
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        server.quit()
        print("Email sent successfully")


    driver.quit()



    return "Done"

