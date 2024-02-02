import requests
from bs4 import BeautifulSoup
import time

bot_token = '6900081755:AAHSq_cmm_CvA21-3i72XqiSavvvksJcPDs'  
chat_id = '1184553885'
message_count = 0

def find_megamenu_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', id='sm_megamenu_97')

    if links:
        for link in links:
            href = link.get('href')
            if href and not href.startswith('javascript:void(0)'):
                print(f"Scraping data from: {href}")
                web_scrape_product_info(href)
    else:
        print("No links found with the specified class or id!")

def send_to_telegram(bot_token, chat_id, message, link=None, img_url=None):
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    if img_url:
        api_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    if link:
        data["text"] += f"\nLink: {link}"

    if img_url:
        data["photo"] = img_url

    try:
        response = requests.post(api_url, data=data)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def web_scrape_product_info(url):
    global message_count
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', class_='product-item-info')

    if products:
        for product in products:
            image_tag = product.find('img', class_='product-image-photo')
            title_tag = product.find('a', class_='product-item-link')
            price_tag = product.find('span', class_='price')
            link_tag = title_tag.get('href')

            if image_tag and title_tag and price_tag:
                image_url = image_tag.get('src')
                title = title_tag.text.strip()
                price = price_tag.text.strip()

                message = f"{title}\nPrice: {price}"
                send_to_telegram(bot_token, chat_id, message, link_tag, image_url)
                message_count += 1

                if message_count % 15 == 0:
                    print("Waiting for 30 seconds...")
                    time.sleep(30)
    else:
        print("No Product Information Found!")

if __name__ == '__main__':
    website_url = 'https://shega.com/'
    find_megamenu_links(website_url)