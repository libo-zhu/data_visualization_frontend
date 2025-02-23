from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

# 设置 WebDriver，使用 Service 来指定 ChromeDriver 路径
service = Service(executable_path="D:/zhulibo/software/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# 请求 URL
url = "https://lishi.tianqi.com/"
driver.get(url)

# 等待页面加载
time.sleep(3)

# 获取网页内容
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 找到所有包含城市信息的 <ul> 标签
ul_tags = soup.find_all('ul', class_='table_list')

# 存储结果的列表
cities_data = []

# 遍历每个 <ul> 标签
for ul_tag in ul_tags:
    # 提取所有 <li> 标签
    li_tags = ul_tag.find_all('li')

    # 遍历每个 <li> 标签，提取城市名字和链接
    for li in li_tags:
        city_name = li.get_text(strip=True)
        
        # 检查是否存在 <a> 标签并获取 href
        a_tag = li.find('a')
        if a_tag:
            city_url = a_tag['href']
            city_url = city_url.split('/')[0]  # 获取第一个 / 前的部分
            cities_data.append([city_name, city_url])

# 保存到 CSV 文件
with open('cities_all.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['City Name', 'URL'])
    writer.writerows(cities_data)

print("数据已成功保存到 cities.csv 文件中。")

# 关闭浏览器
driver.quit()
