#!/usr/bin/evn python
# -*- encoding:utf-8 -*-
# function: connect exsi server api  for restart vm
# date:2019-08-09
# Arthor:Timbaland
import sys


_Arthur_ = 'Timbaland'
import pysphere, pymysql
from pysphere import VIServer
import logging
import ssl
import datetime, os, time
import configparser, codecs

# 全局取消证书验证,忽略连接VSPHERE时提示证书验证
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VcentTools(object):
    def __init__(self, host_ip, user, password,flag):
        self.host_ip = host_ip
        self.user = user
        self.password = password
        self.flag = flag
    # 可以连接esxi主机，也可以连接vcenter

    def _connect(self):

        server_obj = VIServer()

    def esxi_version(self):
        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
            servertype, version = server_obj.get_server_type(), server_obj.get_api_version()
            server_obj.disconnect()
            return servertype, version
        except Exception as  e:
            print (e)

    def vm_status(self, vm_name):

        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
            # servertype, version = server_obj.get_server_type(),server_obj.get_api_version()


        except Exception as  e:
            print (e)

        # 通过名称获取vm的实例
        try:
            vm = server_obj.get_vm_by_name(vm_name)
            if vm.is_powered_off() == False:
                server_obj.disconnect()
                return 1

            if vm.is_powered_off() == True:
                server_obj.disconnect()
                return 2

        except Exception as e:
            server_obj.disconnect()
            return 3

    def vmaction(self, vm_name, vm_hz):

        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
        except Exception as  e:
            print (e)

        # 通过名称获取vm的实例
        try:
            vm = server_obj.get_vm_by_name(vm_name)
        except Exception as e:
            return 0
        if vm.is_powered_off() == False:
            try:
                vm.reset()
                # print (type(int(vm_hz)))
                for i in range(1, int(vm_hz)):
                    print (f'虚拟机{vm_name} 正在重置中。。。。，请等待注册\n' )
                    time.sleep(1)
                print ('重置完成')
                server_obj.disconnect()

                return 1
            except Exception as e:
                print (e)

        if vm.is_powered_off() == True:
            try:
                vm.power_on()
                print (f'虚拟机{vm_name} 正在开机中。。。。')
                server_obj.disconnect()

            except Exception as e:
                return 2

class Class_VM(object):
    def __init__(self, host, user, pwd, port, db, charset):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.db = db
        self.charset = charset

    # 获取教室里面的虚拟机信息
    def get_vmname(self, query_sql):
        try:
            # 连接mysql数据库参数字段
            con = None
            db = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, db=self.db, port=self.port,
                                 charset=self.charset)
            cursor = db.cursor()
            vmlist = []
            cursor.execute(query_sql)
            result = cursor.fetchall()
            # 获取教室云桌面数量
            vm_count = len(result)
            print (f'教室云桌面虚拟机数量共{vm_count}台')

            # print len(cursor.fetchall())
            # cursor.execute(query_vm)
            for vm_id in range(0, vm_count, 1):
                # print result[vm_id][0]
                # print result[vm_id][1]
                vmlist.append(result[vm_id][0])
                # print result[vm_id][0]

            # print type(cursor.fetchall()[0])

            db.commit()

        except ValueError:
            db.roolback
            print ('error')
        # 关闭游标和mysql数据库连接
        cursor.close()
        db.close()
        return vmlist


