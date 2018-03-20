import re
import requests
import json
import time
from requests import RequestException

#获取单页内容，然后对其解析
def get_one_page(url):
    """
    加入异常判断。
    猫眼增加了User-Agent识别，所以在headers中增加User-Agent参数
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text

        return None
    except RequestException:
        return None


#正则匹配电影结果，提取所有内容
def parse_information(html):
    pattern = re.compile(
        '<dd>.*?<i.*?board-index.*?>(.*?)</i>.*?<a.*?title="(.*?)".*?img\sdata-src="(.*?)".*?</a>.*?<p.*?star.*?>(.*?)</p>.*?<p.*?releasetime.*?>(.*?)</p>',
        re.S)
    datas = re.findall(pattern, html)
    for data in datas:
        yield {
            'index': data[0],
            'title': data[1],
            'imgSrc': data[2].strip(),
            'star': data[3].strip()[3:] if len(data[3].strip()) > 3 else '',
            'releaseTime': data[4].strip()[5:] if len(data[4].strip()) > 5 else ''
        }

'''
将提取的结果写入文件，通过json库的dumps方法实现字典的序列化，
指定ensure_ascii=False，保证输出的结果是中文
'''
def write_to_json(content):
    with open('res.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    #offset实现分页
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_information(html):
        print(item)
        write_to_json(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset = i*10)
        #延迟等待
        time.sleep(1)