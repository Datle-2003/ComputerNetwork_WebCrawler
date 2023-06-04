import psycopg2
import urllib.parse as urlparse
from dotenv import load_dotenv
import os
load_dotenv()

url = os.getenv('database_url')
url_parsed = urlparse.urlparse(url)

conn = psycopg2.connect(
        host=url_parsed.hostname,
        port=url_parsed.port,
        user=url_parsed.username,
        password=url_parsed.password,
        database=url_parsed.path[1:]
        ) 
print(conn)
cur = conn.cursor()
cur.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id SERIAL PRIMARY KEY,
                website TEXT,
                name TEXT,
                price INT,
                link TEXT,
                type TEXT,
                UNIQUE (website, name)
            );
        """)
# cur.execute("""DROP TABLE items""")

# try:
#     cur.execute("DROP TABLE IF EXISTS public.items")
#     conn.commit()
# except psycopg2.Error as e:
#     print(f"Error: {e}")

# cur.execute('''
# INSERT INTO items (website, name, price, link, type)
# VALUES ('phongvu', 'MacBook Pro 13', 210000000, 'https://www.apple.com/shop/buy-mac/macbook-pro', 'lenovo');
# INSERT INTO items (website, name, price, link, type)
# VALUES ('phongvu', 'ThinkPad X1 Carbon', 16000000, 'https://www.bestbuy.com', 'lenovo');
# INSERT INTO items (website, name, price, link, type)
# VALUES ('phongvu', 'ThinkPad X2 Carbon', 24000000, '6404022', 'lenovo');
# ''')


cur.execute("""select * from items order by item_id asc""")

results = cur.fetchall()

for row in results:
    print(row)


conn.commit()

cur.close()
conn.close()
