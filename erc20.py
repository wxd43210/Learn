# --学习
"""
作者：Administrator
日期：2022年{05}月{05}日
"""
import pprint
import time
import traceback

import requests
from lxml import etree


def get_table_from_html(html):
    tree = etree.HTML(html)
    # 寻找所有的table标签
    table_lst = tree.xpath("//table")
    table_data_lst = []
    for table in table_lst:
        table_data_lst.append(get_table(table))

    return table_data_lst


def get_table(table_ele):
    """
    获取table数据
    :param table_ele:
    :return:
    """
    tr_lst = table_ele.xpath(".//tr")
    # 第一行通常来说都是标题
    title_data = get_title(tr_lst[0])
    # 第一行后面都是数据
    data = get_data(tr_lst[1:])

    return {
        'title': title_data,
        'data': data
    }


def get_title(tr_ele):
    """
    获取标题
    标题可能用th 标签，也可能用td标签
    :param tr_ele:
    :return:
    """
    # 先寻找th标签
    title_lst = get_tr_data_by_tag(tr_ele, 'th')
    if not title_lst:
        title_lst = get_tr_data_by_tag(tr_ele, 'td')

    return title_lst


def get_data(tr_lst):
    """
    获取数据
    :param tr_lst:
    :return:
    """
    datas = []
    for tr in tr_lst:
        tr_data = get_tr_data_by_tag(tr, 'td')
        datas.append(tr_data)

    return datas


def get_tr_data_by_tag(tr, tag):
    """
    获取一行数据
    :param tr:
    :param tag:
    :return:
    """
    datas = []
    nodes = tr.xpath(".//{tag}".format(tag=tag))
    for node in nodes:
        text = node.xpath('string(.)').strip()
        datas.append(text)

    return datas


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    return res.text


def run():
    url = 'https://etherscan.io/tokentxns?a=0xe0e8cc0ae10f3f24343a630d6ead1a512ab73d8b&p=1'
    html = get_html(url)
    table_lst = get_table_from_html(html)
    # pprint.pprint(table_lst)
    return table_lst


if __name__ == '__main__':
    first_str = ""
    trade_token = []
    while True:
        try:
            send_msg1 = "="*18+"\n"
            send_msg3 = send_msg1+"HASH:{}\n"
            send_msg4 = send_msg1+"时间:{}\n"
            send_msg5 = send_msg1+"from:{}\n"
            send_msg6 = send_msg1+"to:{}\n"
            send_msg8 = send_msg1+"Token:{}\n"
            send_msg9 = send_msg1+"数量:{}\n"
            return_table_data = run()[0]["data"][0]
            return_table_data.pop(3)
            send_str = return_table_data[1]
            if first_str != send_str:
                first_str = send_str
                send_msg31 = send_msg3.format(return_table_data[1])
                time_utc = int(time.mktime(time.strptime(return_table_data[2], "%Y-%m-%d %H:%M:%S")))
                time_utc += 8*60*60
                send_msg41 = send_msg4.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_utc)))
                send_msg51 = send_msg5.format(return_table_data[3])
                send_msg61 = send_msg6.format(return_table_data[5])
                send_msg81 = send_msg8.format(return_table_data[7])
                send_msg91 = send_msg9.format(return_table_data[6])
                send_msg = send_msg31+send_msg41+send_msg51+send_msg61+send_msg81+send_msg91
                trade_token = [return_table_data[7]]
                param = {"text": send_msg}
                res = requests.post("http://114.132.237.91:5000/sendJK6", data=param)
            else:
                if return_table_data[7] not in trade_token:
                    send_msg31 = send_msg3.format(return_table_data[1])
                    time_utc = int(time.mktime(time.strptime(return_table_data[2], "%Y-%m-%d %H:%M:%S")))
                    time_utc += 8 * 60 * 60
                    send_msg41 = send_msg4.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_utc)))
                    send_msg51 = send_msg5.format(return_table_data[3])
                    send_msg61 = send_msg6.format(return_table_data[5])
                    send_msg81 = send_msg8.format(return_table_data[7])
                    send_msg91 = send_msg9.format(return_table_data[6])
                    send_msg = send_msg31 + send_msg41 + send_msg51 + send_msg61 + send_msg81 + send_msg91
                    trade_token.append(return_table_data[7])
                    param = {"text": send_msg}
                    res = requests.post("http://114.132.237.91:5000/sendJK6", data=param)
        except:
            error_msg = traceback.format_exc()
            print(error_msg)
        time.sleep(10)














