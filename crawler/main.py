import os
import time
import psycopg2
import urllib.parse as urlparse
from dotenv import load_dotenv

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

cur = conn.cursor()
try:
    cur.execute("DROP TABLE IF EXISTS public.items")
    conn.commit()
except psycopg2.Error as e:
     print(f"Error: {e}")


conn.commit()

cur.close()
conn.close()




while True:
    # Run the command
    status = os.system("scrapy crawl fptshop")

    # Check the exit status
    if status == 0:
        print('success')
        # The command succeeded, so break out of the loop
        break
    else:
        print('error')
        # The command failed, so wait for a bit and try again
        time.sleep(10)


# Run the second command
while True:
    # Run the command
    status = os.system("scrapy crawl tgdd")

    # Check the exit status
    if status == 0:
        # The command succeeded, so break out of the loop
        break
    else:
        # The command failed, so wait for a bit and try again
        time.sleep(10)


while True:
    # Run the command
    status = os.system("scrapy crawl dienmayxanh")


    # Check the exit status
    if status == 0:
        # The command succeeded, so break out of the loop
        break
    else:
        # The command failed, so wait for a bit and try again
        time.sleep(10)


        
        
while True:
    # Run the command
    status = os.system("scrapy crawl hoanghamobile")

    # Check the exit status
    if status == 0:
        # The command succeeded, so break out of the loop
        break
    else:
        # The command failed, so wait for a bit and try again
        time.sleep(10)


while True:
    # Run the command
    status = os.system("scrapy crawl anphatpc")

    # Check the exit status
    if status == 0:
        # The command succeeded, so break out of the loop
        break
    else:
        # The command failed, so wait for a bit and try again
        time.sleep(10)

while True:
    # Run the command
    status = os.system("scrapy crawl hacom")

    # Check the exit status
    if status == 0:
        # The command succeeded, so break out of the loop
        break
    else:
        # The command failed, so wait for a bit and try again
        time.sleep(10)