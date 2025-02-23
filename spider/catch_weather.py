import requests
import csv
from bs4 import BeautifulSoup

# 设置自定义User-Agent头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 读取城市列表并存储在字典中
cities = []
with open('cities_all.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        cities.append(row)

# 处理每个城市数据
for city in cities[:]:  # 使用复制的列表来迭代，避免修改原列表时出现问题
    city_name, city_url = city
    # 构建目标URL
    url = f"https://www.tianqi.com/{city_url}/"
    
    # 发起请求，加入headers
    response = requests.get(url, headers=headers)

    # 确保响应成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析网页
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找class为"weather_info"的<dl>元素
        weather_info = soup.find('dl', class_='weather_info')
        
        # 提取各个天气相关信息
        if weather_info:
            week = weather_info.find('dd', class_='week').get_text(strip=True)
            temperature = weather_info.find('dd', class_='weather').find('p', class_='now').get_text(strip=True)
            weather_condition = weather_info.find('dd', class_='weather').find('span').get_text(strip=True)
            humidity = weather_info.find('dd', class_='shidu').find_all('b')[0].get_text(strip=True)
            wind_direction = weather_info.find('dd', class_='shidu').find_all('b')[1].get_text(strip=True)
            uv_index = weather_info.find('dd', class_='shidu').find_all('b')[2].get_text(strip=True)
            air_quality = weather_info.find('dd', class_='kongqi').find('h5').get_text(strip=True)
            pm_value = weather_info.find('dd', class_='kongqi').find('h6').get_text(strip=True)
            
            # 提取日出和日落时间
            sun_times = weather_info.find('dd', class_='kongqi').find('span')

            # 设置默认值
            sunrise = "N/A"  # 默认值
            sunset = "N/A"   # 默认值
            
            if sun_times:
                sun_text = sun_times.get_text(strip=True)
                sun_parts = sun_text.split("日出:")
                if len(sun_parts) > 1:
                    sunrise = sun_parts[1].split("日落:")[0].strip()  # 日出时间
                    sunset = sun_parts[1].split("日落:")[1].strip()  # 日落时间

            # 打印提取的数据
            print(f"城市: {city_name}")
            print(f"日期: {week}")
            print(f"温度: {temperature}")
            print(f"天气: {weather_condition}")
            print(f"湿度: {humidity}")
            print(f"风向: {wind_direction}")
            print(f"紫外线: {uv_index}")
            print(f"空气质量: {air_quality}")
            print(f"PM值: {pm_value}")
            print(f"日出: {sunrise}")
            print(f"日落: {sunset}")
            
            # 保存到CSV文件
            with open('weather_data.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # 写入标题行（如果文件为空）
                if file.tell() == 0:
                    writer.writerow(['城市', '日期', '温度', '天气', '湿度', '风向', '紫外线', '空气质量', 'PM值', '日出', '日落'])
                writer.writerow([city_name, week, temperature, weather_condition, humidity, wind_direction, uv_index, air_quality, pm_value, sunrise, sunset])
    elif response.status_code == 403:
        # 如果返回403状态码，删除该城市记录
        print(f"请求失败，城市: {city_name}，状态码：403，删除该城市记录。")
        cities.remove(city)

# 重新写入更新后的城市列表（删除了失败的城市）
with open('cities_all.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['City Name', 'URL'])  # 写入标题行
    writer.writerows(cities)  # 写入更新后的城市数据
