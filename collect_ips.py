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

# 正则表达式用于匹配IP地址 (同时支持 IPv4 和 IPv6)
ip_pattern = r'(?:(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(?:[0-9a-fA-F:]+))'

# 检查ip.txt文件是否存在，如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')
    print("已删除现有的 ip.txt 文件")

# 创建一个文件来存储IP地址
with open('ip.txt', 'w', encoding='utf-8') as file:
    for url in urls:
        try:
            print(f"正在处理 URL: {url}")
            
            # 发送HTTP请求获取网页内容
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            print(f"成功获取网页内容，状态码: {response.status_code}")

            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            if url == 'https://cf.090227.xyz/':
                # 处理 cf.090227.xyz 的特殊情况
                table = soup.find('table', class_='table')
                if table:
                    print("找到表格，开始解析行")
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
                            print(f"写入: {formatted_ip}")
                else:
                    print(f"在 {url} 中未找到包含IP信息的表格。")
            else:
                # 处理其他网站
                if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
                    elements = soup.find_all('tr')
                elif url == 'https://ip.164746.xyz':
                    elements = soup.find_all('tr')
                else:
                    elements = soup.find_all('li')
                
                # 遍历所有元素，查找IP地址
                for element in elements:
                    element_text = element.get_text()
                    ip_matches = re.findall(ip_pattern, element_text)
                    
                    # 如果找到IP地址，则写入文件
                    for ip in ip_matches:
                        file.write(ip + '\n')
                        print(f"写入: {ip}")

        except requests.RequestException as e:
            print(f"请求 {url} 时发生错误: {e}")
        except Exception as e:
            print(f"处理 {url} 时发生错误: {e}")

print('处理完成。正在检查 ip.txt 文件...')

# 检查文件是否为空
if os.path.exists('ip.txt'):
    if os.path.getsize('ip.txt') == 0:
        print("警告：ip.txt 文件是空的。没有成功写入任何数据。")
    else:
        print(f"成功写入数据到 ip.txt。文件大小：{os.path.getsize('ip.txt')} 字节")
    
    # 打印文件内容（前几行）用于验证
    with open('ip.txt', 'r', encoding='utf-8') as file:
        print("ip.txt 内容预览:")
        print(file.read(500))  # 读取前500个字符
else:
    print("错误：ip.txt 文件不存在。可能是由于写入过程中发生错误。")

print('IP地址已保存到ip.txt文件中。脚本执行完毕。')
