from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import os
import random

# 设置 Chrome 驱动路径
chrome_driver_path = 'D:/zhulibo/software/chromedriver-win64/chromedriver.exe'

# 设置 Chrome 浏览器选项
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式，不弹出浏览器界面
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('window-size=1920x1080')

# 使用 Service 指定 ChromeDriver 路径
service = Service(chrome_driver_path)

# 创建一个保存数据的函数
def save_to_csv(weather_data, city, year, month):
    # 定义 CSV 文件的列名，将“城市”字段放在最前面
    fieldnames = ['城市', '日期', '最高气温', '最低气温', '天气', '风力']
    
    # 创建保存目录
    output_dir = 'weather_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # CSV 文件名（所有数据保存到同一个文件）
    file_name = f"{output_dir}/weather_data.csv"

    # 判断文件是否存在，若不存在，则写入表头
    file_exists = os.path.exists(file_name)

    # 保存数据到 CSV 文件
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # 如果文件不存在，写入表头
        if not file_exists:
            writer.writeheader()

        # 写入数据
        for data in weather_data:
            writer.writerow(data)

    print(f"{year}年{month}月的数据已成功保存到 '{file_name}'")

# 使用 Chrome 浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)

# 读取城市信息
cities = {}
with open('cities.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cities[row['City Name']] = row['URL']

# 遍历每个城市和每个月的天气数据
for city_name, city_url in cities.items():
    # 如果城市 URL 不存在，则跳过该城市
    if not city_url:
        print(f"城市 {city_name} 没有 URL，跳过此城市。")
        continue
    
    for year in range(2011, 2025):  # 从 2011 到 2024 年
        for month in range(1, 13):  # 每年 12 个月
            # 格式化月份（补零）
            month_str = str(month).zfill(2)

            # 拼接 URL
            url = f'https://lishi.tianqi.com/{city_url}/{year}{month_str}.html'
            print(f"正在抓取 {city_name} {year} 年 {month_str} 月的数据，URL: {url}")
            
            try:
                # 打开目标网页
                driver.get(url)

                # 等待页面加载完成，适当的等待时间（0.5 到 1 秒之间的随机时间）
                time.sleep(random.uniform(0.5, 1))

                # 查找并点击“查看更多”按钮
                try:
                    more_button = driver.find_element(By.CLASS_NAME, 'lishidesc2')
                    more_button.click()  # 点击查看更多按钮
                    time.sleep(random.uniform(0.5, 1))  # 等待页面加载更多内容
                    print("查看更多按钮已点击，正在加载更多数据...")
                except Exception as e:
                    print(f"点击查看更多按钮失败: {e}")

                # 获取完整的网页内容
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                # 解析天气数据
                ul_tag = soup.find('ul', class_='thrui')

                if ul_tag:
                    # 创建一个空列表来存储每天的数据
                    weather_data = []

                    # 遍历每个 <li> 标签，提取天气信息
                    for li in ul_tag.find_all('li'):
                        day_data = {}
                        try:
                            # 提取具体的数据
                            date = li.find('div', class_='th200').text.strip()  # 日期
                            max_temp = li.find_all('div', class_='th140')[0].text.strip()  # 最高气温
                            min_temp = li.find_all('div', class_='th140')[1].text.strip()  # 最低气温
                            weather = li.find_all('div', class_='th140')[2].text.strip()  # 天气情况
                            wind = li.find_all('div', class_='th140')[3].text.strip()  # 风力

                            # 如果数据不完整，跳过
                            if not date or not max_temp or not min_temp or not weather or not wind:
                                continue

                            # 填充数据
                            day_data['日期'] = date
                            day_data['最高气温'] = max_temp
                            day_data['最低气温'] = min_temp
                            day_data['天气'] = weather
                            day_data['风力'] = wind
                            day_data['城市'] = city_name  # 使用城市名称字段

                            # 将每一天的数据添加到列表中
                            weather_data.append(day_data)
                        except AttributeError:
                            # 如果某一天的标签解析失败，跳过该条数据
                            continue

                    # 保存数据到 CSV 文件
                    if weather_data:
                        save_to_csv(weather_data, city_name, year, month)
                    else:
                        print(f"{city_name} {year}年{month_str}月的数据为空，跳过保存。")
                else:
                    print(f"未找到 ul 标签，无法解析 {city_name} {year} 年 {month_str} 月的数据。")

            except Exception as e:
                print(f"抓取 {city_name} {year} 年 {month_str} 月的数据时出现错误: {e}")

# 关闭浏览器
driver.quit()
