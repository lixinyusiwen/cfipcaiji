import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = ['https://cf.090227.xyz/']

# 正则表达式用于匹配IP地址 (同时支持 IPv4 和 IPv6)
ip_pattern = r'(?:(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(?:[0-9a-fA-F:]+))'

# 检查ip.txt文件是否存在，如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储IP地址
with open('ip.txt', 'w', encoding='utf-8') as file:
    for url in urls:
        try:
            # 发送HTTP请求获取网页内容
            response = requests.get(url)
            response.raise_for_status()

            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找包含IP信息的表格
            table = soup.find('table', class_='table')

            if table:
                rows = table.find_all('tr')[1:]  # 跳过表头
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) >= 4:
                        ip = columns[1].text.strip()
                        line = columns[0].text.strip()

                        # 检查IP是否为IPv6格式
                        if ':' in ip:
                            formatted_ip = f"[{ip}]:8443#{line}"
                        else:
                            formatted_ip = f"{ip}:8443#{line}"

                        file.write(formatted_ip + '\n')
            else:
                print(f"在 {url} 中未找到包含IP信息的表格。")

        except requests.RequestException as e:
            print(f"请求 {url} 时发生错误: {e}")
        except Exception as e:
            print(f"处理 {url} 时发生错误: {e}")

print('IP地址已保存到ip.txt文件中。')
