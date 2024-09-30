import requests
from bs4 import BeautifulSoup
import os

# 目标URL
url = 'https://cf.090227.xyz/'

# 检查ip.txt文件是否存在，如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

try:
    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    response.raise_for_status()  # 如果请求不成功则抛出异常
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找包含IP信息的表格
    table = soup.find('table', class_='table')
    
    if table:
        # 创建一个文件来存储IP地址信息
        with open('ip.txt', 'w', encoding='utf-8') as file:
            rows = table.find_all('tr')[1:]  # 跳过表头
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 4:
                    ip = columns[1].text.strip()
                    line = columns[0].text.strip()
                    
                    # 检查IP是否为IPv6格式
                    if ':' in ip:
                        # 对于IPv6地址，我们需要用方括号括起来
                        formatted_ip = f"[{ip}]:8443#{line}"
                    else:
                        # 对于IPv4地址，我们不需要方括号
                        formatted_ip = f"{ip}:8443#{line}"
                    
                    file.write(formatted_ip + '\n')
        
        print('IP地址信息已保存到ip.txt文件中。')
    else:
        print('未找到包含IP信息的表格。')

except requests.RequestException as e:
    print(f"请求错误: {e}")
except Exception as e:
    print(f"发生错误: {e}")
