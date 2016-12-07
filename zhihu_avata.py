#!/usr/bin/env python
# encoding: utf-8

import json
import time
import urllib2
import MySQLdb
import requests


def generate_cookie(cookies):
    '''
    generate python's request cookies with website's cookie @return type object
    '''
    my_cookie = cookies
    request_cookie = {}
    for line in my_cookie.split(';'):
        name, value = line.strip().split('=', 1)
        request_cookie[name] = value

    return request_cookie


def do_requests(base_url, cookies, proxy, headers):
    """
    do request to site
    """
    s = requests.Session()
    response = s.get(
            base_url,
            proxies=proxy,
            headers=headers,
            cookies=cookies)

    return response.text


def download_avatar(avatar_url, avatar_name):
    if avatar_url == u'https://pic1.zhimg.com/da8e974dc_is.jpg':
        return
    try:
        proxy_support = urllib2.ProxyHandler({'http': 'http://101.53.101.172:9999'})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        socket = urllib2.urlopen(avatar_url)
        data = socket.read()
        with open('./avatar/%s.jpg' % avatar_name, 'wb') as jpg:
            jpg.write(data)
    except:
        return


def update_database(user_list):
    db = MySQLdb.connect(
            'localhost',
            'root',
            'yxs',
            'user_pool')
    cursor = db.cursor()
    for user in user_list:
        meta_value = '%s' % user
        meta_value = meta_value.replace('\"', '\'')
        insert_sql = 'insert into user (`content`) value ("%s")' % meta_value
        cursor.execute(insert_sql)
        print user['avatar_url']
        download_avatar(user['avatar_url'], user['id'])
    db.commit()


def run():
    base_url = 'https://www.zhihu.com/api/v4/members/su-fei-17/followers?per_page=30&include=data%5B%2A%5D.answer_count%2Carticles_count%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=30&offset=0'
    my_proxy = {
        'http': 'http://101.53.101.172:9999'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'www.zhihu.com',
        'authorization': 'Bearer Mi4wQUdDQ080X3c5QW9BVUlJRDRoX3RDaGNBQUFCaEFsVk53aEZ1V0FEakVvWmViZFE1QTJib2c1cGpRZFhLTGowQ2FB|1481017142|0f2e2c4800de1f3349b2900ad6c419c9a3a2c63b'
    }
    cookies = 'd_c0="AFCCA-If7QqPThkZc6EkJxMToLY5RB6tyV0=|1480491850"; _zap=2375a458-9155-4323-ade0-52917cc047f6; r_cap_id="ZjQ3YmFhMmM5Y2Q4NGE5Nzg2YzEwZTNjNWVhZjNjMDA=|1481015847|9e77633e5994bef947a42345f9f7782ba9c27917"; login="YmJlM2NkZWJkYTE5NDZiYmFhODY4ZTVlMzhiZDVjNzg=|1481015859|33d2c53149c52188e5e13d44c74bf2ef286aa4a9"; q_c1=803162cbd324492095a97787922b88d9|1481016366000|1481016366000; l_cap_id="ZjIwNmU1ODQxZDRiNGYzYjkyYzkyNDI5YjAxNWE1YzE=|1481016366|f43208ca9ecb4a102c5f31fdfa829985aff68e57"; cap_id="NzExNTJhMWJiZTk2NDBjYzg0MzBiZjZhNGYwNWEyOTM=|1481016366|c604f470cd0c9331da3bf3a9247a8adbbea8fa12"; n_c=1; __utma=51854390.426880515.1481016999.1481016999.1481016999.1; __utmb=51854390.9.9.1481017046486; __utmc=51854390; __utmz=51854390.1481016999.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20161206=1^3=entry_date=20161206=1; z_c0=Mi4wQUdDQ080X3c5QW9BVUlJRDRoX3RDaGNBQUFCaEFsVk53aEZ1V0FEakVvWmViZFE1QTJib2c1cGpRZFhLTGowQ2FB|1481017142|0f2e2c4800de1f3349b2900ad6c419c9a3a2c63b'
    cookies = generate_cookie(cookies)

    while True:
        time.sleep(3)
        response = do_requests(base_url, cookies, my_proxy, headers)
        print response
        my_json = json.loads(response)
        update_database(my_json['data'])

        base_url = my_json['paging']['next']


if __name__ == '__main__':
    run()
