#! /usr/bin/env python
# coding: utf-8
# qknow@蓝鲸淘
# Licensed under the MIT License.


from watchdog.observers import Observer
from watchdog.events import *
import time
import pymongo
from AntShares.Wallets.Wallet import Wallet
from AntShares.Fixed8 import Fixed8
import os.path
import json
import binascii


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(
                event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(
                event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            # print("file created:{0}".format(event.src_path))
            # print os.path.basename(event.src_path)

            # data = JSONFileHandler.load(os.path.join(
            #     rootdir, os.path.basename(event.src_path)))
            blockIndex = get_block_index(os.path.basename(event.src_path))
            print 'blockIndex', blockIndex
            data = JSONFileHandler.load(event.src_path)
            nep5 = NEP5Handler()
            if data is not None:
                for item in data:
                    # print type(item)
                    # print item['txid']
                    item['blockIndex'] = blockIndex
                    if item['state']['value'][0]['value'] == transfer:
                        nep5.transfer(item)
            print data

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))


class JSONFileHandler(object):

    @staticmethod
    def store(path, data):
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

    @staticmethod
    def load(path):
        with open(path) as json_file:
            data = json.load(json_file)
            return data


class NEP5Handler(object):
    def __init__(self):
        self.client = pymongo.MongoClient("192.168.31.9", 27017)
        self.db = self.client['neo-otcgo']
        self.collection = self.db.nep5
        self.wallet = Wallet()

    def transfer(self, obj):
        # print obj['state']['value'][0]['value']
        result = self.collection.find_one({"txid": obj['txid']})
        # print result
        if result is not None:
            self.collection.insert_one({
                "blockIndex": obj['blockIndex'],
                "txid": obj['txid'],
                "contract": obj['contract'],
                "operation": binascii.unhexlify(obj['state']['value'][0]['value']),
                # 转出
                "from": self.wallet.toAddress(obj['state']['value'][1]['value']),
                # 输入
                "to": self.wallet.toAddress(obj['state']['value'][2]['value']),
                "value": Fixed8.getNumStr(obj['state']['value'][3]['value'])
            })
        else:
            print 'txid', obj['txid'], 'exist'


class FileHandle(object):
    @staticmethod
    def fileList(path):
        list = os.listdir(path)  # 列出文件夹下所有的目录与文件
        return list


def get_block_index(filename):
    blockIndex = re.split(r'-', filename)
    return os.path.splitext(blockIndex[1])[0]


if __name__ == "__main__":

    try:
        # 定义操作
        transfer = '7472616e73666572'

        rootdir = '/Users/wei/Desktop/otcgo/neo_wallet_analysis/nep5-script/test'
        listArr = FileHandle.fileList(rootdir)

        print 'file count', len(listArr)
        # 循环文件夹
        nep5 = NEP5Handler()
        for f in range(0, len(listArr)):
            # print os.path.join(rootdir, listArr[f])
            blockIndex = get_block_index(listArr[f])
            print 'blockIndex', blockIndex
            data = JSONFileHandler.load(os.path.join(rootdir, listArr[f]))
            if data is not None:
                for item in data:
                    # print type(item)
                    # print item['txid']
                    item['blockIndex'] = blockIndex
                    if item['state']['value'][0]['value'] == transfer:
                        nep5.transfer(item)

        # print 'success'

        # 监控文件夹
        observer = Observer()
        event_handler = FileEventHandler()
        observer.schedule(event_handler, rootdir, True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

        # data = JSONFileHandler.load('./test/block-1610072.json')
        # for item in data:
        #     print item['txid']

    except Exception as e:
        print e
