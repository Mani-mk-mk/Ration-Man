import sqlite3
from scrape import scrape as wb


conn = sqlite3.connect("db.sqlite3")
conn.row_factory = lambda c, row: row
c = conn.cursor()
c.execute("""SELECT product_flipkart_url, product_amazon_url, product_bigb_url
             FROM store_product""")
database_urls = c.fetchall()


for rows in database_urls:
    for url in rows:
        if "flipkart.com" in url:
            flipkart_price = wb.flipkart(url)
            c.execute("""UPDATE store_product
                         SET price_flipkart=?
                         WHERE product_flipkart_url=?""", (flipkart_price, url))

        elif "amazon" in url:
                amazon_price = wb.amazon(url)
            # print(sainsburys_price)
                c.execute("""UPDATE store_product
                             SET price_amazon = ?
                             WHERE product_amazon_url=?""", (amazon_price, url))

        elif "bigbasket.com" in url:
            bigb_price = wb.bigb(url)
            # print(tesco_price)
            c.execute("""UPDATE store_product
                         SET price_bigb=?
                         WHERE product_bigb_url=?""", (bigb_price, url))

        else:
            print("FLAG: Is the following url correct? {}".format(url))

conn.commit()
c.close()
conn.close()
