#!/usr/bin/env python
# encoding: utf-8

import hashlib


def check_diff(data):
    my_md5 = hashlib.md5()
    my_md5.update(data)

    return my_md5.hexdigest()


def load_pic_data(pic_name):
    with open(pic_name) as f:
        byte = f.read()
    return byte


print load_pic_data('/home/brittyu/app/avatar/a8519c92f7e8a39e29975af84ba22c8f.jpg')

