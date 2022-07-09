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
