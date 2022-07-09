import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

url_luz = "https://tarifaluzhora.es/"

headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}

res = requests.get(url_luz, headers=headers)
if(res.status_code == 200):
  html_luz = BeautifulSoup(res.content, 'html.parser')
  date_luz = html_luz.find("input", {"name" : "date"}).get("value")
  prices = html_luz.find_all("span", {"itemprop" : "price"})
  prices = [float(price.getText().split()[0]) for price in prices]
  best_price = min(prices)
  if prices.index(min(prices)) <= 9:
   best_hour = '0' +  str(prices.index(best_price)) + ":00"
  else:
   best_hour =   str(prices.index(best_price)) + ":00"

  hours = list(range(0,24,1))
  msg_best_price = "El precio más bajo es " + str(best_price) + "€/kWh a las " +  str(best_hour) + " horas"
  print(msg_best_price)
  
plt.plot(hours,prices, marker="o")
plt.title("Precio luz (€/kWh) " + date_luz)
plt.xlabel("Horas")
plt.ylabel("€/kWh")
plt.savefig("Gráfica.jpg")
plt.show()

import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',options=options)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


url_gasolina = "https://www.dieselogasolina.com/gasolineras-en-badajoz-localidad-badajoz.html"
wd.get(url_gasolina)


select_element = wd.find_element(By.ID,'tipo_combustible')
select_object = Select(select_element)
select_object.select_by_value('1')
#Para ver la opción seleccionada
all_selected_options = select_object.all_selected_options
print(all_selected_options[0].text)

try:
  clickable  = WebDriverWait(wd, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-red.shadowover'))).click()

except TimeoutException:
    print("Se vencio el timeout")

   
try:
  precios = wd.find_elements(By.CLASS_NAME, "precio")
  rows = wd.find_elements(By.CLASS_NAME, "trgasolinera")
  data_petrol=[]
  titles = ["Dirección", "Horario", "Empresa", "Fecha", "Precio"]
  msg_petrol = '<table><thead><tr></tr></thead><tbody>'
  for el in titles:
    msg_petrol= msg_petrol + "<th style='text-align:center; padding:10px'>" + el + "</th>"
  msg_petrol = msg_petrol + '</tr></thead><tbody>'
  for row in rows:
    direction = row.find_element(By.CLASS_NAME,"direccion")
    time = row.find_element(By.CLASS_NAME, "horario")
    company = row.find_element(By.CLASS_NAME, "empresa")
    date = row.find_element(By.CLASS_NAME, "fecha_actualizacion")
    price= row.find_element(By.CSS_SELECTOR, ".precio")
    msg_petrol =  msg_petrol +  "<tr>"
    msg_petrol =  msg_petrol  + "<td style='text-align:center; padding:10px'>" + direction.text + "</td>"
    msg_petrol =  msg_petrol  + "<td style='text-align:center; padding:10px'>" + time.text + "</td>"
    msg_petrol =  msg_petrol  + "<td style='text-align:center; padding:10px'>" + company.text + "</td>"
    msg_petrol =  msg_petrol + "<tdstyle='text-align:center; padding:10px'>" + date.text + "</td>"
    msg_petrol =  msg_petrol  + "<td style='text-align:center; padding:10px'><strong>" + price.text + "</strong></td></tr>"

  msg_petrol =  msg_petrol + "</tbody>"
  print(msg_petrol)

except:
  print("Algo salió mal")
  
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io


me  = 'jorgevipo.dev@gmail.com'
recipient = 'jovivaspo@gmail.com'
subject = 'Graph Report'

email_server_host = 'smtp.gmail.com'
port = 587
email_username = me
email_password = 'glliugnpedhfthca'

email_body = "<h1>Save your fucking money!</h1>" + "<h2>Precio luz mercado regulado " + date_luz + "</h2>"  + "<p><strong>" + msg_best_price + "</strong></p>" + "<img src='cid:image1'>" + "<h2>Gasolineras más baratas hoy en Badajoz: </h2>" + msg_petrol

msg = MIMEMultipart('alternative')
msg['From'] = me
msg['To'] = recipient
msg['Subject'] = subject

msg.attach(MIMEText(email_body, 'html'))

fp = open('Gráfica.jpg','rb')
msgImage = MIMEImage(fp.read())
fp.close()
msgImage.add_header('Content-ID', '<image1>')
msg.attach(msgImage)

server = smtplib.SMTP(email_server_host, port)
server.ehlo()
server.starttls()
server.login(email_username, email_password)
server.sendmail(me, recipient, msg.as_string())
server.close()
