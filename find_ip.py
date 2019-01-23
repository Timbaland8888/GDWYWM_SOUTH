# -*- ecoding:utf-8 -*-
#Function：批量转换DHCP为static
#Arthur:Timbaland
#version:1.0
#Date:2018-09-13
import gevent
import os,wmi
import time
import subprocess
import re
import winrm
import threading
ip_list = []
class IPV4(object):

    IPLIST = []
    def __init__(self,ippre):
        self.ippre = ippre
    #寻找有效IP地址
    def ping_call(self,num):

        fnull = open(os.devnull, 'w')
        ipaddr = self.ippre + str(num)
        result = subprocess.getstatusoutput('ping '+ ipaddr + ' -n 2')
        current_time = time.strftime('%Y%m%d-%H:%M:%S', time.localtime())
        ip_list = []
        #1、无法访问目标主机 2、请求超时
        if re.findall(r'无法访问目标主机',result[1]) == [r'无法访问目标主机', r'无法访问目标主机'] or re.findall(r'请求超时',result[1]) == [ r'请求超时',r'请求超时']:
            print('时间:{} ip地址:{} ping fail'.format(current_time, ipaddr))
            status = '时间:{} ip地址:{} ping fail'.format(current_time, ipaddr)

        else:
            print('时间:{} ip地址:{} ping ok'.format(current_time, ipaddr))
            status = '时间:{} ip地址:{} ping ok'.format(current_time, ipaddr)
            return ipaddr
        fnull.close()

    def asynchronous(self,ping_call): # 异步

        g_l = [gevent.spawn(ping_call, i) for i in range(1, 64)]

        gevent.joinall(g_l)

    # 远程控制win7登入设置IP
    def call_remote_ip(self,host,user,pwd,mask,gateway):
        logfile = 'logs_%s.txt' % time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        try:
            # 用wmi连接到远程win7系统设置IP
            conn = wmi.WMI(computer=host, user=user, password=pwd)
            cmd_IP = 'netsh interface ip set address name="本地连接 2" source="static" addr="%s" mask="%s" gateway="%s"'%(host,mask,gateway)
            # cmd_dns= 'netsh interface ip set dns name="本地连接 2" source="static" addr="%s"'%(dns)
            status = conn.Win32_Process.Create(CommandLine=cmd_IP)  # CHANGE IP

            # conn.Win32_Process.Create(CommandLine=cmd_dns)  # CHANGE DNS
            print("修改IP成功!")

            return True
        except Exception as e:
            print(host+'机器已经关机')
            log = open(logfile, 'a')
            log.write(('%s %s call  Failed!\r\n') % (host, e))
            log.close()
            return False
        finally:
            print('SET IP continue')

    # 远程控制win7登入设置DNS
    def call_remote_dns(self, host, user, pwd, dns):
        logfile = 'logs_%s.txt' % time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        try:
            # 用wmi连接到远程win7系统设置IP
            conn = wmi.WMI(computer=host, user=user, password=pwd)
            # cmd_IP = 'netsh interface ip set address name="本地连接 2" source="static" addr="%s" mask="%s" gateway="%s" && netsh interface ip set dns name="本地连接 2" source="static" addr="%s"' % (
            # host, mask, gateway, dns)
            cmd_dns= 'netsh interface ip set dns name="本地连接 2" source="static" addr="%s"'%(dns)
            status = conn.Win32_Process.Create(CommandLine=cmd_dns)  # CHANGE IP

            # conn.Win32_Process.Create(CommandLine=cmd_dns)  # CHANGE DNS
            print("修改DNS成功!")

            return True
        except Exception as e:
            print(host + '机器已经关机')
            log = open(logfile, 'a')
            log.write(('%s %s call  Failed!\r\n') % (host, e))
            log.close()
            return False
        finally:
            print('DNS continue')
            # 远程拷贝文件&&文件夹到远程主机上

    def rep_remote_copy(self, host, user, pwd):
        logfile = 'logs_%s.txt' % time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        try:
            # 用wmi连接到远程win7系统设置IP
            win7 = winrm.Session('http://%s:5985/wsman' % (host), auth=('Admin', 'Admin'))
            print("%s ----终端文件夹再次重新开始拷贝!" % (host))
            # 远程文件共享服务器认证
            win7.run_cmd(r'net use \\192.168.48.223\ipc$ "123456"  /user:"timbaland\administrator" ')

            # 从共享服务器上复制名字为终端文件夹到本地
            win7.run_cmd(r'xcopy \\192.168.48.223\share\课堂管理软件\终端  /y /s /e /c /z C:\终端')
            print("%s ----终端文件夹终于拷贝成功!" % (host))
            # ------------
            # ------------
            print("%s ----DLL文件夹再次重新开始拷贝!" % (host))
            #  复制DDL文件

            # 从共享服务器上复制名字为DLL文件夹到本地
            win7.run_cmd(r'xcopy \\192.168.48.223\share\课堂管理软件\DLL  /y /s /e /c /z C:\Windows\DLL')
            print("%s ----DLL文件夹终于拷贝成功" % (host))
            # -----------
            # -----------
            print("%s ----汇捷快捷方式文件再次开始拷贝" % (host))
            #  复制D汇捷快捷方式
            # 从共享服务器上复制名字为DLL文件夹到本地
            win7.run_cmd(r'xcopy \\192.168.48.223\share\课堂管理软件\云桌面快捷方式 /y /s /e /c /z C:\users\admin\desktop')
            print("%s ----汇捷快捷方式终于拷贝成功!" % (host))
            return True
        except Exception as e:
            print(e)
    #远程拷贝文件&&文件夹到远程主机上
    def call_remote_copy(self, host, user, pwd):
            logfile = 'logs_%s.txt' % time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
            try:
                # 用wmi连接到远程win7系统设置IP
                win7 = winrm.Session('http://%s:5985/wsman' %(host),auth=('Admin','Admin'))
                print("%s ----终端文件夹开始拷贝!" % (host))
                #远程文件共享服务器认证
                win7.run_cmd(r'net use \\192.168.48.223\ipc$ "123456"  /user:"timbaland\administrator" ')
                #远程强制删除C:\终端
                win7.run_cmd(r'rd/s/q C:\终端')
                #远程创建C:\终端
                win7.run_cmd(r'md C:\终端')
                #从共享服务器上复制名字为终端文件夹到本地
                win7.run_cmd(r'xcopy \\192.168.48.223\share\课堂管理软件\终端  /y /s /e /c /z C:\终端')
                print("%s ----终端文件夹拷贝成功!" % (host))
                #------------
                #------------
                print("%s ----DLL文件夹开始拷贝!" % (host))
                #  复制DDL文件
                # 远程强制删除C:\Windows\DLL
                win7.run_cmd(r'rd/s/q C:\Windows\DLL')
                # 远程创建C:\Windows\DLL
                win7.run_cmd(r'md C:\Windows\DLL')
                # 从共享服务器上复制名字为DLL文件夹到本地
                win7.run_cmd(r'xcopy \\192.168.48.223\share\课堂管理软件\DLL  /y /s /e /c /z C:\Windows\DLL')
                print("%s ----DLL文件夹拷贝成功" % (host))
                #-----------
                #-----------
                print("%s ----汇捷快捷方式文件开始拷贝" % (host))
                #  复制D汇捷快捷方式
                # 从共享服务器上复制名字为DLL文件夹到本地
                win7.run_cmd(r'xcopy \\192.168.48.223\share\课堂管理软件\云桌面快捷方式 /y /s /e /c /z C:\users\admin\desktop')
                print("%s ----汇捷快捷方式拷贝成功!"%(host))
                return True
            except Exception as e:
                print(host + '  网络故障')
                log = open(logfile, 'a')
                log.write(('%s %s call  Failed!\r\n') % (host, e))
                log.close()
                self.rep_remote_copy(host,user,pwd)
                return False
            finally:
                print('copy continue')


if __name__ == '__main__':
    start_time = time.time()
    mask = '255.255.255.0'
    gateway = '10.11.2.254'
    dns = '210.38.120.252'
    #远程主机user
    user = 'administrator'
    # 远程主机密码
    pwd = '123456'
    p = IPV4('192.168.48.')
    # p.asynchronous(p.ping_call)
    #获取IP集合
    m_ip = ['192.168.48.6','192.168.48.62']
#收集在线IP地址
    # for ip in range(62,63):
    #     if p.ping_call(ip) is not None:
    #         # print(p.ping_call(ip))
    #         m_ip.append(p.ping_call(ip))

    print('在线主机如下：\n',m_ip)
    for n in range(len(m_ip)):

        try:

            new_thread = threading.Thread(target=p.call_remote_copy, args=(m_ip[n], user, pwd))

        except Exception as e:
            print(e)

        new_thread.start()

        # p.call_remote_copy(h,user,pwd)

    print('协程执行-->耗时{:.2f}'.format(time.time() - start_time))