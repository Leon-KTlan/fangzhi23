import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

# 设置保存路径
SAVE_DIR = "thumbnails"
os.makedirs(SAVE_DIR, exist_ok=True)

# 百度图片搜索的基础 URL
BASE_URL = "https://image.baidu.com/search/index?tn=baiduimage&word="

# 搜索关键词
SEARCH_KEYWORD = "python"
SEARCH_URL = BASE_URL + quote(SEARCH_KEYWORD)  # 处理中文或特殊字符

# 设置请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_image_urls(search_url):
    """ 爬取百度图片搜索结果中的图片网址 """
    print(f"正在请求: {search_url}")
    try:
        response = requests.get(search_url, headers=HEADERS)
        if response.status_code != 200:
            print("请求失败，状态码：", response.status_code)
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        # 找到所有包含图片地址的标签，这里可能需要根据实际页面结构调整
        image_tags = soup.find_all("img", {"src": True})

        # 提取图片 URL
        image_urls = [img['src'] for img in image_tags if img.get('src')]
        return image_urls

    except Exception as e:
        print(f"请求失败: {e}")
        return []

def download_thumbnail(image_url, save_dir):
    """ 下载图片缩略图 """
    try:
        print(f"正在下载图片: {image_url}")
        response = requests.get(image_url, headers=HEADERS, stream=True, timeout=10)
        if response.status_code == 200:
            # 获取图片文件名
            filename = os.path.join(save_dir, os.path.basename(image_url))
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"图片已保存: {filename}")
        else:
            print(f"下载失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"下载失败: {e}")

def main():
    # 1. 获取图片 URL 列表
    image_urls = fetch_image_urls(SEARCH_URL)
    print(f"共找到 {len(image_urls)} 张图片。")

    if image_urls:
        # 2. 下载缩略图
        for i, img_url in enumerate(image_urls[:10]):  # 只保存前10张图片
            print(f"正在处理第 {i + 1} 张图片.")
            download_thumbnail(img_url, SAVE_DIR)
    else:
        print("未能找到任何图片")

if __name__ == "__main__":
    main()
