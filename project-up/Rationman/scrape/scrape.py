from bs4 import BeautifulSoup
import requests 

#products = Product.objects.all()
#param = {'products': products}




def flipkart(url):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = soup.find_all("div",{"class": "_30jeq3 _16Jk6d"})
    try:
        p = prices[0].text.strip()
    except:
        p = prices.text.strip()
    price = p.strip()
    print(price)
    pricec = price.strip("₹")
    return int(pricec)



def amazon(url):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        prices = soup.find_all("span",{"id": "priceblock_ourprice"})
        p = prices[0].text.strip()
        price = p.strip()
        pricec = price[2:]
        pricex = int(float(pricec))
    except:
        try:
            prices = soup.find_all("span",{"class": "a-color-price"})
            p = prices[0].text.strip()
            price = p.strip()
            pricec = price[2:]
            pricex = int(float(pricec))
        except:
            try:
                prices = soup.find_all("span",{"id": "priceblock_saleprice"})
                p = prices[0].text.strip()
                price = p.strip()
                pricec = price[2:]
                pricex = int(float(pricec))
            except:
                pricex = 0
    print(pricex)
    return (pricex)





def bigb(url):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    prices = soup.find_all("td",{"class": "IyLvo"})
    p = prices[0].text.strip()
    price = p.strip()
    print(price)
    pricec = price.strip("Rs ")
    return int(float(pricec))


#flipkart(url_flipkart)
#amazon(url_amazon)
#bigb(url_bigb)


def comp_price(price_flipkart, price_amazon, price_bigb):
    if price_flipkart < price_amazon and price_flipkart < price_bigb:
        return price_flipkart
    elif price_amazon < price_bigb:
        return price_amazon
    else:
        return price_bigb

