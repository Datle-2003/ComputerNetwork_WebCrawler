from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re
import scrapy

class FptShopSpider(scrapy.Spider):
    name = 'fptshop'
    allowed_domains = ['https://fptshop.com.vn']
    start_urls = ['https://fptshop.com.vn/may-tinh-xach-tay']

    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(options=self.option)
        super(FptShopSpider, self).__init__()

    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)

    def extract_info(self, text):
        pattern = r'^(.*?)(\d{1,3}\.\d{3}\.\d{3})'

        match = re.search(pattern, text, re.DOTALL)
        if match:
            name = match.group(1).rstrip('\n')
            price = match.group(2)
            return [name, price]

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)

    # click the show more button repeatedly to load the entire content
        while True:
            try:
                show_more_button = WebDriverWait(self.browser, 15).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="root"]/main/div/div[3]/div[2]/div[3]/div/div[3]/a')))
                show_more_button.click()
                time.sleep(3)
            except TimeoutException:
                print('Cannot find the "Show More" button')
                break

    # parse the loaded content
        try:
            parent_elements = self.browser.find_elements(By.CLASS_NAME, 'cdt-product')
            for parent_element in parent_elements:
                time.sleep(1)
                try:
                    raw_info = parent_element.find_element(By.CLASS_NAME, 'cdt-product__info')
                    name_element = raw_info.find_element(By.CLASS_NAME, 'cdt-product__name')
                    name = name_element.text
                    link = name_element.get_attribute('href')
                    image_link = None
                    # Extract Type based on name
                    if name.startswith("Laptop") or name.startswith("laptop"):
                        type_value = name.split()[1]
                    else:
                        type_value = name.split()[0]
                    price_element = raw_info.find_element(By.CSS_SELECTOR, '.cdt-product__show-promo .progress')
                    price = price_element.text.split(' ')[0].strip()
                except:
                    continue

                if (type_value == "Microsoft" or type_value == "microsoft"):
                    type_value = "Surface"
                yield {
                    'website': 'fpt',
                    'name': name,
                    'image_link': image_link,
                    'type': type_value,
                    'price': self.convert_price(price),
                    'link': link
                }
        
        except Exception as e:
            print(str(e))
      

    def closed(self, reason):
        self.browser.quit()

               

class TgddSpider(scrapy.Spider):
    name = 'tgdd'
    allowed_domains = ['https://www.thegioididong.com']
    start_urls = ['https://www.thegioididong.com/laptop-ldp']

    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.option.add_argument("--incognito")
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=self.option)
        super(TgddSpider, self).__init__()

    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)

    def parse(self, response):
        self.browser.get(response.url)
        brands = self.browser.find_element(By.XPATH, "/html/body/div[7]/div")
        brand_urls = [brand.get_attribute(
            'href') for brand in brands.find_elements(By.TAG_NAME, 'a')]
        for brand_url in brand_urls:
            self.browser.get(brand_url)
            time.sleep(3)
            productls_driver = self.browser.find_element(
                By.CLASS_NAME, "listproduct")
            
            names = productls_driver.find_elements(By.TAG_NAME, 'h3')
            prices = productls_driver.find_elements(By.CLASS_NAME, "price")
            links = productls_driver.find_elements(By.CLASS_NAME, "main-contain")
            image_elements = productls_driver.find_elements(By.CLASS_NAME, "item-img")
        
            for i in range(len(names)):
                name = names[i].text
                if name == "":
                    continue
                price = self.convert_price(prices[i].text)
                link = links[i].get_attribute('href')
            
                image_element = image_elements[i].find_element(By.TAG_NAME, "img")
                image_link = image_element.get_attribute('data-src') or image_element.get_attribute('src')
                if not image_link:
                    image_link = None

                type_value = links[i].get_attribute('data-brand')

                if (type_value == "Microsoft" or type_value == "microsoft"):
                    type_value = "Surface"
            
                yield {
                    'website': 'thegioididong',
                    'name': name,
                    'price': price,
                    'link': link,
                    'image_link': image_link,
                    'type': type_value,
                }
           

    def closed(self, reason):
        self.browser.quit()


class DienMayXanhSpider(scrapy.Spider):
    name = 'dienmayxanh'
    allowed_domains = ['https://www.dienmayxanh.com']
    start_urls = ['https://www.dienmayxanh.com/laptop']

    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.option.add_argument("--incognito")
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=self.option)
        super(DienMayXanhSpider, self).__init__()

    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)

    def extract_info(self, text):
        name_pattern = r'^(.+)\nRAM'
        name_match = re.search(name_pattern, text, re.MULTILINE)
        name = name_match.group(1)

        price_pattern = r"(\d[\d\.]*)₫"
        prices_match = re.findall(price_pattern, text)

        price = 0
        if len(prices_match) == 1:
            price = prices_match[0]
        else:
            price = prices_match[len(prices_match) - 2]
        price = self.convert_price(price)

        return [name, price]

    def parse(self, response):
        self.browser.get(response.url)
    # click the show more button repeatly to load the entire content
        while True:
            try:
                show_more_button = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@class="cate-main-container"]/section/div[3]/div[2]/a')))
                show_more_button.click()
                time.sleep(3)
            except TimeoutException:
                break
    # parse the loaded content
        try:
            raw_infos = self.browser.find_elements(By.CSS_SELECTOR, ".item.__cate_44")
            for raw_info in raw_infos:
                try:
                    name = raw_info.find_element(By.TAG_NAME, "h3").text
                    price = raw_info.find_element(By.CLASS_NAME, "price").text
                    link = raw_info.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    image_link = raw_info.find_element(By.CLASS_NAME, "item-img").find_element(By.TAG_NAME, "img").get_attribute("data-src")
                    type = raw_info.find_element(By.TAG_NAME, "a").get_attribute("data-brand")
                    
                    if (type == "Microsoft" or type == "microsoft"):
                        type = "Surface"
                    yield {
                    'website': 'dienmayxanh',
                    'name': name,
                    'price': self.convert_price(price),
                    'link': link,
                    'image_link': image_link,
                    'type': type,
                    }

                except Exception as e:
                    continue
               
        except Exception as e:
            print(str(e))

    def closed(self, reason):
        self.browser.quit()


class HoangHaMobileSpider(scrapy.Spider):
    name = 'hoanghamobile'
    allowed_domains = ['hoanghamobile.com']
    start_urls = ['https://hoanghamobile.com/laptop']
    
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--disable-extensions')
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.option.add_argument("--incognito")
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=self.option)
        super(HoangHaMobileSpider, self).__init__()

    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)

        # Close pop-ups
        try:
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.close-modal.icon-minutes'))
            ).click()
        except TimeoutException:
            print("Pop-up close button not found")

        brand_links = response.css('.menu.g1 ul li a::attr(href)').getall()
        laptop_links = [link for link in brand_links if '/laptop/' in link]
        laptop_links = laptop_links[:-5]
        for laptop_link in laptop_links:
            content_url = 'https://hoanghamobile.com' + laptop_link
            self.browser.get(content_url)
            time.sleep(5)
            
            while True:
                try:
                    show_more_button = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="page-pager"]/a'))
                    )
                    show_more_button_text = show_more_button.text
                    if show_more_button_text != "Không còn sản phẩm nào.!":
                        show_more_button.click()
                        time.sleep(2)
                        print("Clicked 'Show more'")
                    else: 
                        print("No more products available")
                        break
                except TimeoutException:
                    break

                # Close pop-ups
            try:
                WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.close-modal.icon-minutes'))
                ).click()
                time.sleep(5)
            except TimeoutException:
                print("Pop-up close button not found")

            try:
                type = self.browser.find_element(By.CSS_SELECTOR, '.list-product h1').text
                contents = self.browser.find_elements(By.CSS_SELECTOR, ".col-content.lts-product")
                for content in contents:
                    raw_infos = content.find_elements(By.CLASS_NAME, 'item')
                
                    for raw_info in raw_infos:
                        time.sleep(0.5)
                        info = raw_info.find_element(By.CLASS_NAME, 'info')
                        name = info.find_element(By.CLASS_NAME, 'title').text.strip()
                        price = info.find_element(By.CSS_SELECTOR, '.price strong').text.strip()

                        link = raw_info.find_element(By.CLASS_NAME, 'info').find_element(By.TAG_NAME, 'a').get_attribute('href')
                        image_link = raw_info.find_element(By.CLASS_NAME, 'img').find_element(By.TAG_NAME, 'img').get_attribute('src')
                        if (type == "Microsoft" or type == "microsoft"):
                            type = "Surface"
                        yield {
                            'website': 'hoanghamobile',
                            'name': name,
                            'price': self.convert_price(price),
                            'link': link,
                            'image_link': image_link,
                            'type': type,
                        }
            except Exception as e:
                print(str(e))

    def closed(self, reason):
        self.browser.quit()
  
class AnPhatPCSpider(scrapy.Spider):
    name = 'anphatpc'
    allowed_domains = ['anphatpc.com.vn']
    start_urls = ['https://www.anphatpc.com.vn/laptop-theo-hang.html']

    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.option.add_argument("--incognito")
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=self.option)
        super(AnPhatPCSpider, self).__init__()

    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)
        brand_links = [link.get_attribute('href') for link in self.browser.find_element(By.CLASS_NAME, 'filter-list').find_elements(By.TAG_NAME, 'a')]
        for brand_link in brand_links:
            self.browser.get(brand_link)
            time.sleep(5)
            
            parent_element = self.browser.find_element(By.CLASS_NAME, 'paging').find_elements(By.TAG_NAME, 'a')
            links = [link.get_attribute('href') for link in parent_element]

            for link in links:
                type = self.browser.find_element(By.CLASS_NAME, 'filter-list').find_element(By.CLASS_NAME, 'current').text
                content = self.browser.find_element(By.CSS_SELECTOR, '.p-list-container.d-flex.flex-wrap')
                raw_infos = content.find_elements(By.CLASS_NAME, 'js-p-item')
                for raw_info in raw_infos:
                    name = raw_info.find_element(By.CLASS_NAME, 'p-name').text
                    price = raw_info.find_element(By.CLASS_NAME, 'p-price').text
                    link = raw_info.find_element(By.CLASS_NAME, 'p-img').get_attribute('href')
                    image_link = raw_info.find_element(By.CLASS_NAME, 'p-img').find_element(By.TAG_NAME, 'img').get_attribute('data-src')
                    if (type == "Microsoft" or type == "microsoft"):
                        type = "Surface"
                    yield {
                        'website': 'anphatpc',
                        'name': name,
                        'price': self.convert_price(price),
                        'link': link,
                        'image_link': image_link,
                        'type': type,
                    }
    def closed(self, reason):
        self.browser.quit()

        

class HacomSpider(scrapy.Spider):
    name = 'hacom'
    start_urls = ['https://hacom.vn/laptop']

    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.option.add_argument("--incognito")
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=self.option)
        super(HacomSpider, self).__init__()

    def convert_price(self, price_txt):
        price_txt = re.sub(r"[^\d]", "", price_txt)
        if not re.search(r"\d", price_txt):
            return 0
        return int(price_txt)

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5)

        elements = self.browser.find_elements(By.CSS_SELECTOR, '.list-brand-check li a')
        links = [element.get_attribute('href') for element in elements if element.get_attribute('href') != 'https://hacom.vn/laptop?brand=hacom' and element.get_attribute('href').startswith('https://hacom.vn/laptop?brand=')]
        for link in links:
            self.browser.get(link)
            time.sleep(5)
            split_parts = link.split("=")
            type = split_parts[1]
            href_list = []
            try:
                pages = self.browser.find_element(By.CLASS_NAME, ".paging").find_elements(By.TAG_NAME, "a")
                href_list = [page.get_attribute("href") for page in pages]
            except Exception as e:
                href_list = [link]
            for href in href_list:
                self.browser.get(href)
                time.sleep(5)
                content = self.browser.find_element(By.CSS_SELECTOR, '.cate-prod-bottom.cate-list-prod ')
                raw_infos = content.find_elements(By.CLASS_NAME, 'p-component.item.loaded')
                for raw_info in raw_infos:
                    name = raw_info.find_element(By.CSS_SELECTOR, "h3.p-name a").text
                    price = raw_info.find_element(By.CSS_SELECTOR, "span.p-price.js-get-minPrice").text
                    link = raw_info.find_element(By.CSS_SELECTOR, "h3.p-name a").get_attribute("href")
                    image_link = raw_info.find_element(By.CSS_SELECTOR, "div.p-img img").get_attribute("data-src")
                    if (type == "microsoft" or type == "Microsoft"):
                        type = "Surface"
                    yield {
                        'website': 'hacom',
                        'name': name,
                        'price': self.convert_price(price),
                        'link': link,
                        'image_link': image_link,
                        'type': type,
                    }

    def closed(self, reason):
        self.browser.quit()
