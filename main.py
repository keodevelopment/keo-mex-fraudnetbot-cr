import time
import smtplib
from flask import Flask
from datetime import datetime
from selenium import webdriver
from email.mime.text import MIMEText
from selenium.webdriver import ActionChains
from email.mime.image import MIMEImage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
#import chromedriver_autoinstaller
#from pyvirtualdisplay import Display  



app = Flask(__name__)




@app.route("/")
def hello_bot():
    opts = Options()
    opts.add_argument("user-agent=Chrome/95.0.4638.54")
    opts.add_argument("--headless")
    opts.add_argument("--window-size=1920x1080")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-extensions")
    #opts.add_extension(r'C:\Users\jhand\Buster-Captcha-Solver-for-Humans.crx')
    #driver de tipo headless
    #opts.headless = True
    #chromedriver_autoinstaller.install() 
    #gecko driver manager
    #firefox_options = FirefoxOptions()
    #firefox_options.add_argument("--headless")
    #firefox_options.add_argument("--window-size=1920x1080")
    #firefox_options.add_argument("--disable-gpu")
    #firefox_options.add_argument("--no-sandbox")
    #firefox_options.add_argument("--disable-dev-shm-usage")
    #firefox_options.add_argument("--disable-extensions")
    
    #driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=opts)
    now = datetime.now() 
    year_month_day = now.strftime("%Y-%m-%d")
    driver = webdriver.Chrome('./chromedriver.exe',options=opts)

    #set url feed for login
    url = 'https://network.americanexpress.com/globalnetwork/v4/sign-in/'
    print("ubicando url")
    payload={
        "Email": 'anastasiareyes1987',
        "Password": 'Casa1234???'
    }


    #Navigate to the page
    driver.get(url)
    driver.maximize_window()



    user_ID = driver.find_element("xpath", "//*[@id='userid']")
    user_ID.send_keys(payload['Email'])

    password = driver.find_element("xpath", "//*[@id='password']")
    password.send_keys(payload['Password'])
    print("pasando credenciales")
    time.sleep(2)

    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(1)

                                                
    signin_button = driver.find_element("xpath", '//*[@id="submit"]')
    signin_button.click()
    time.sleep(1)
    print("clicking")

    #Go to FraudNet Reports
    #Link only for 'Active' status reports
    new_url = "https://gnsfraudnet.americanexpress.com/fraudnet/#/ior/new"
    #implicit wait
    print("go to the url")
    driver.implicitly_wait(120)

    driver.get(new_url)
    print("navegando a  nueva url")
    time.sleep(2)
    driver.save_screenshot('prueba.png')

    #xpaths of the reports
    try:
        element = WebDriverWait(driver,600).until(
            EC.presence_of_element_located((By.XPATH, "//tbody[@class='selectable']"))
        )
        print("elemento encontrado")
        tbody = driver.find_element("xpath", '//tbody[@class="selectable"]')
        print("trying to find the reports")
        #driver.save_screenshot('firefox5.png')
    except:
        print('No reports!!')
        driver.quit()
        breakpoint

    table = driver.find_element("xpath", '//*[@id="responsiveWrapper_sub"]/div[3]/div[2]/div/div/div[2]/div[2]/div/div[2]/table').get_attribute('outerHTML')

    df = pd.read_html(table)[0]  # Convert the table to a dataframe
    print(df)

    crm = df['CM Number'].tolist()  # ....... Listamos los numeros de tarjetas de credito y los convertimos a string
    crm = [str(i) for i in crm]
    print("CM Numbers: ", crm)

    valores = df.values.tolist()    # ........ Listamos los valores de cada renlgon de la tabla
    print("valores: ", valores)

    indices = []                                                         # Recorremos cada uno de los numeros de tarjeta 
    for i in range(len(crm)):                                            # y verificamos cuales de ellas comienza con los 
        if crm[i][0:6] == '379542' and valores[i][2] == year_month_day:  # digitos '379542' y ademas no son del dia de hoy
            indices.append(i)
    print("indices: ", indices)

    for elm in indices:             # Mostramos datos particulares de cada reporte con las condiciones anteriores
        print(valores[elm][3])

    if len(indices) > 0:
        print("Hay reportes nuevos")
        #Send email with the new reports
        #screen shot and save in local
        driver.save_screenshot('new_report.png')

        #send email
        # create message object instance
        recipients = ['seandaza@gmail.com','anastasiar@keoworld.com','carlosr@keoworld.com','carlosb@keoworld.com','ricardof@keoworld.com','armandoi@keoworld.com','luist@keoworld.com','edissonv@keoworld.com','erikab@keoworld.com', 'jhand@keoworld.com']
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