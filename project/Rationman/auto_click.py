from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.amazon.in/AmazonBasics-15-Piece-Non-Stick-Cookware-Set/dp/B07481LPMF/ref=sr_1_1_sspa?crid=14VYD6SQU04SV&dchild=1&keywords=cooking+set+for+kitchen&qid=1605985583&sprefix=cooki%2Caps%2C456&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExUEVCNzhZNThZVVozJmVuY3J5cHRlZElkPUEwNTM2NDA2MzdKMklCS1dEN0tBTCZlbmNyeXB0ZWRBZElkPUExMDM2MzM4Mk1QRklSTVJGQ0paSSZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU="
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(url)


button = driver.find_element_by_id('add-to-cart-button')
button.click()
url = 'https://www.amazon.in/Amul-Pure-Ghee-LTR-Pack/dp/B07VD76LKZ/ref=asc_df_B07VD76LKZ/?tag=googleshopdes-21&linkCode=df0&hvadid=396985204497&hvpos=&hvnetw=g&hvrand=7143875099930389576&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9301468&hvtargid=pla-840151172544&psc=1&ext_vrnc=hi'
driver.get(url)
button = driver.find_element_by_id('add-to-cart-button')
button.click()
#driver.close()

#[WDM] - Driver has been saved in cache [C:\Users\manig\.wdm\drivers\chromedriver\win32\87.0.4280.20]
