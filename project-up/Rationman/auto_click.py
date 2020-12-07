from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager


def Add2Cart_Amazon(url):
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        button = driver.find_element_by_id('add-to-cart-button')
        button.click()
    except:
        print('SORRY')

#[WDM] - Driver has been saved in cache [C:\Users\manig\.wdm\drivers\chromedriver\win32\87.0.4280.20]
