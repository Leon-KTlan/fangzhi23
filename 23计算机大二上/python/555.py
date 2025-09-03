import requests
from bs4 import BeautifulSoup
import time
import random

def fetch_webpage(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_webpage(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 这里添加您的解析逻辑
    # 例如：找到所有图片标签
    images = soup.find_all('img')
    return [img.get('src') for img in images if img.get('src')]

def main():
    url = "https://www.zstu.edu.cn/"  # 替换为您想要爬取的网页
    html = fetch_webpage(url)
    if html:
        image_urls = parse_webpage(html)
        print(f"Found {len(image_urls)} images")
        for img_url in image_urls[:5]:  # 只打印前5个URL
            print(img_url)
            time.sleep(random.uniform(1, 3))  # 随机延迟

if __name__ == "__main__":
    main()
