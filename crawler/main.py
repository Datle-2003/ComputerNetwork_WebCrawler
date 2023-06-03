import os
import time
import psycopg2
import urllib.parse as urlparse
import sys
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('database_url')
url_parsed = urlparse.urlparse(url)

try:
    with psycopg2.connect(
            host=url_parsed.hostname,
            port=url_parsed.port,
            user=url_parsed.username,
            password=url_parsed.password,
            database=url_parsed.path[1:]
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS public.items")
            conn.commit()

            cur.execute("""CREATE TABLE IF NOT EXISTS items (
                            item_id SERIAL PRIMARY KEY,
                            website TEXT,
                            name VARCHAR(255),
                            price INTEGER,
                            link TEXT,
                            type TEXT,
                            image_link TEXT,
                            UNIQUE (website, name)
                        );""")

    while True:
        status = os.system("scrapy crawl fptshop")
        if status == 0:
            print('fptshop crawling success')
            break
        else:
            print('fptshop crawling error')
            time.sleep(10)

    while True:
        status = os.system("scrapy crawl tgdd")
        if status == 0:
            print('tgdd crawling success')
            break
        else:
            print('tgdd crawling error')
            time.sleep(10)

    while True:
        status = os.system("scrapy crawl dienmayxanh")
        if status == 0:
            print('dienmayxanh crawling success')
            break
        else:
            print('dienmayxanh crawling error')
            time.sleep(10)

    while True:
        status = os.system("scrapy crawl hoanghamobile")
        if status == 0:
            print('hoanghamobile crawling success')
            break
        else:
            print('hoanghamobile crawling error')
            time.sleep(10)

    while True:
        status = os.system("scrapy crawl anphatpc")
        if status == 0:
            print('anphatpc crawling success')
            break
        else:
            print('anphatpc crawling error')
            time.sleep(10)

    while True:
        status = os.system("scrapy crawl hacom")
        if status == 0:
            print('hacom crawling success')
            break
        else:
            print('hacom crawling error')
            time.sleep(10)

    with psycopg2.connect(
            host=url_parsed.hostname,
            port=url_parsed.port,
            user=url_parsed.username,
            password=url_parsed.password,
            database=url_parsed.path[1:]
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""UPDATE items SET type ILIKE 'Macbook' WHERE type ILIKE 'Apple'""")
            conn.commit()
except psycopg2.Error as e:
    print(f"Database Error: {e}")
