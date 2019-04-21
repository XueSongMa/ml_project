from spider import request_fun
import bs4

'''
    输出格式：
    内地排行榜
        分数：99   排名：1    名字：阿斯蒂芬asd  发布时间：2019   歌手：XXX
        分数：99   排名：1    名字：阿斯蒂芬asd  发布时间：2019   歌手：XXX
    香港排行榜
        分数：99   排名：1    名字：阿斯蒂芬asd  发布时间：2019   歌手：XXX
    韩国
    美国
    
'''
def get_content(url):
    '''
    取得每一类型小说排行榜，按顺序写入文件
    :param url:
    :return:
    '''
    url_list = []
    html = request_fun.get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    #rank_all = soup.find_all('div', attrs={'class': 'search-rank_L'})

    # con = rank_all

    mv_list = soup.find_all('li', class_='vitem J_li_toggle_date ')
    mvs_info = []
    for mv in mv_list:
        mv_info = {}
        score_nm = mv.find('div', class_='score_box')
        mv_info['score_number'] = score_nm.find('h3').text
        #score_increase  = score_nm.find('span', class_="asc-num")
        #mv_info['score_increase'] = score_increase.find()

        mv_info['top_num'] = mv.find('div', class_='top_num').text
        mv_sum_info = mv.find('div', class_='info')
        mv_info['mv_title'] = mv_sum_info.find('h3').text.replace('\n','')
        mv_info['mv_href'] = mv_sum_info.find('h3').a['href']
        mv_info['singer'] = mv_sum_info.find('p', class_='cc').text.replace('--','').replace('\t','').replace('\n','').strip()
        mv_info['published_time'] = mv_sum_info.find('p', class_='c9').text
        mvs_info.append(mv_info)

    return mvs_info


def get_one_channel(channel_url):
    '''

    :param channel_url: 含有channel name 和URL的字典
    :return: 状态
    : 通过调用get_content 得到每一个Channel 里的内容
    '''

    for channel_nm, url in channel_url.items():
        print('现在在读取 {} TOP20的MTV'.format(channel_nm))

        mv_list_info = get_content(url)

        #把读取的内容存文件
        with open('MTV_top20.txt', 'a+', encoding='utf-8') as f:
            f.write('{}的TOP20MTV list\n'.format(channel_nm))
            for mv in mv_list_info:
                f.write('    分数：{}\t排名：{}\tMV歌曲名：{}\t歌手：{}\t地址：{}\t{}\n'.format(
                    mv['score_number'], mv['top_num'], mv['mv_title'], mv['singer'], mv['mv_href'], mv['published_time']
                ))



def main():
    channel_list = ['ML', 'HT', 'US', 'JP', 'KR']
    channel_url = {}
    # 排行榜地址：
    base_url = 'http://vchart.yinyuetai.com/vchart/trends?area={}'
    for channel in channel_list:
        channel_url[channel] = base_url.format(channel)

    get_one_channel(channel_url)


if __name__ == '__main__':
    main()