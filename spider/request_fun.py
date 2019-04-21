import requests

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        # r.raise_for_status
        # 我手动测试了编码。并设置好，这样有助于效率的提升
        r.encoding = ('utr-8')
        return r.text
    except:
        return "读取网页内容出错————Something Wrong！"
