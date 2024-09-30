import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 
    'https://ip.164746.xyz',
    'https://cf.090227.xyz/'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'(?:(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(?:[0-9a-fA-F:]+))'

# 检查ip.txt文件是否存在，如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储IP地址
with open('ip.txt', 'w', encoding='utf-8') as file:
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if url == 'https://cf.090227.xyz/':
                table = soup.find('table', class_='table')
                rows = table.find_all('tr')[1:] if table else []
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) >= 4:
                        ip = columns[1].text.strip()
                        line = columns[0].text.strip()
                        formatted_ip = f"[{ip}]:8443#{line}" if ':' in ip else f"{ip}:8443#{line}"
                        file.write(formatted_ip + '\n')
            else:
                elements = soup.find_all('tr') if url in urls[:2] else soup.find_all('li')
                for element in elements:
                    ip_matches = re.findall(ip_pattern, element.get_text())
                    for ip in ip_matches:
                        file.write(ip + '\n')

        except requests.RequestException:
            continue

# 检查文件是否为空
if os.path.exists('ip.txt'):
    if os.path.getsize('ip.txt') > 0:
        with open('ip.txt', 'r', encoding='utf-8') as file:
            print(file.read(500))  # 读取前500个字符
    else:
        print("警告：ip.txt 文件是空的。没有成功写入任何数据。")
else:
    print("错误：ip.txt 文件不存在。")
