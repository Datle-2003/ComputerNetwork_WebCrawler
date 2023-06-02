import psycopg2
import urllib.parse as urlparse
from dotenv import load_dotenv
import os

load_dotenv()

class PostgreSQLPipeline(object):

    def __init__(self):
        self.url = os.getenv('database_url')
        self.conn = None
        self.cur = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        url_parsed = urlparse.urlparse(self.url)
        self.conn = psycopg2.connect(
            host=url_parsed.hostname,
            port=url_parsed.port,
            user=url_parsed.username,
            password=url_parsed.password,
            database=url_parsed.path[1:]
        )
        self.cur = self.conn.cursor()

        # Create the 'items' table if it doesn't exist
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id SERIAL PRIMARY KEY,
                website TEXT,
                name TEXT,
                price INTEGER,
                link TEXT,
                type TEXT,
                image_link TEXT,
                UNIQUE (website, name)
            );
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute("BEGIN;")
            sql = "INSERT INTO items (website, name, price, link, type, image_link) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cur.execute(sql, (item['website'], item['name'], item['price'], item['link'], item['type'], item['image_link']))
            self.cur.execute("COMMIT;")
        except Exception as e:
            print("Error processing {}: {}".format(item, e))
            self.cur.execute("ROLLBACK;")
        return item
