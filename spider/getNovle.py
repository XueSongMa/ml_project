import requests
import bs4
from bs4 import BeautifulSoup


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        # r.raise_for_status
        # 我手动测试了编码。并设置好，这样有助于效率的提升
        r.encoding = ('utr-8')
        return r.text
    except:
        return "读取网页内容出错————Something Wrong！"

def get_content(url):
    '''
    取得每一类型小说排行榜，按顺序写入文件
    :param url:
    :return:
    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    category_list = soup.find_all('div', attrs={'class': 'index_toplist mright mbottom'})
    history_finished_list = soup.find_all('div', attrs={'class': 'index_toplist mbottom'})

    for cate in category_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a+', encoding='utf-8') as f:
            f.write("\n小说种类：{}\n".format(name))
        general_list = cate.find(class_='topbooks')
        book_list = general_list.find_all('li')

        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']

            url_list.append(link)

            with open('novel_list.csv', 'a', encoding='utf-8') as f:
                f.write("小说名：{}\t 小说地址：{}\n".format(title, link))

    for cate in history_finished_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a', encoding='utf-8') as f:
            f.write("\n小说种类：{} \n".format(name))

        general_list = cate.find(style='display: block;')
        book_list = general_list.find_all('li')

        for book in book_list:
            link = 'http://ww.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)
            with open('novel_list.csv','a',encoding='utf-8') as f:
                f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))

    return url_list

def get_txt_url(url):
    '''
    获取该小说每个章节的url地址：
    并创建小说文件

    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    lista = soup.find_all('dd')
    txt_name = soup.find('h1').text
    with open('C:\\Projects\\myprojects\\spider\\小说\\{}.txt'.format(txt_name), "a+", encoding='utf-8') as f:
        f.write('小说标题：{} \n'.format(txt_name))
    for url in lista:
        url_list.append('http://www.qu.la/' + url.a['href'])

    return url_list, txt_name

def get_one_txt(url, txt_name):
    '''
    获取小说每个章节的文本
    并写入到本地
    '''
    html = get_html(url) #.replace('<br>', '\n')

    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        txt = soup.find('div', id='content').text.replace('chaptererror();', '')
        title = soup.find('title').text

        with open('C:\\Projects\\myprojects\\spider\\小说\\{}.txt'.format(txt_name), "a", encoding='utf-8') as f:
            f.write(title + '\n\n')
            f.write(txt + '\n')
            print('当前小说：{} 当前章节{} 已经下载完毕'.format(txt_name, title))
    except:
        print('someting wrong')


def get_all_txt(url_list):
    '''
    下载排行榜里所有的小说
    并保存为txt格式
    '''

    for url in url_list:
        # 便利获取当前小说的所有章节的目录，
        # 并且生成小说头文件

        page_list, txt_name = get_txt_url(url)

        for page_url in page_list:
            # 遍历每一篇小说，并下载到目录
            get_one_txt(page_url, txt_name)
            print('当前进度 {}% '.format(url_list.index(url) / len(url_list) * 100))



def main():
    # 排行榜地址：
    base_url = 'http://www.qu.la/paihangbang/'
    # 获取排行榜中所有小说的url连接
    url_list = get_content(base_url)

    # 除去重复的小说，增加效率
    url_list = list(set(url_list))
    get_all_txt(url_list)


if __name__ == '__main__':
    main()