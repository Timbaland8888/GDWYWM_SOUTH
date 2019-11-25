# -*- encoding:utf-8 -*-
#!/bin/user/python

from tkinter import *
from tkinter import ttk

import  configparser,codecs
import os
from  con_mysql import Con_mysql
from vm_reset import  *
def go(*args):  # 处理事件，*args表示可变参数

    # os.system(r'wscript .\rename.vbs %s\%s' % (sharedir, sname))
    print(comboxlist.get())  # 打印选中的值
    classroom = comboxlist.get()
    # classroom = 'c406-1 -->WIN7406'
    classroom = classroom.split('-->')[0].strip()
    cf = configparser.ConfigParser()
    cf.read_file(codecs.open('config.ini', "r", "utf-8-sig"))
    obj1 = VcentTools(cf.get('vc1', 'vc_ip'), cf.get('vc1', 'vc_acount'), cf.get('vc1', 'vc_pwd'), flag='obj1')
    # obj2 = VcentTools(cf.get('vc2', 'vc_ip'), cf.get('vc2', 'vc_acount'), cf.get('vc2', 'vc_pwd'), flag='obj2')
    # obj3 = VcentTools(cf.get('vc3', 'vc_ip'), cf.get('vc3', 'vc_acount'), cf.get('vc3', 'vc_pwd'), flag='obj3')
    # obj4 = VcentTools(cf.get('vc4', 'vc_ip'), cf.get('vc4', 'vc_acount'), cf.get('vc4', 'vc_pwd'), flag='obj4')

    # 查询教室虚拟机
    query_vm = f'''  SELECT  b.vm_name 
                    from hj_dg a 
                    INNER JOIN hj_vm b on a.id = b.dg_id 
                    WHERE b.vm_type = 1 and a.dg_name = "{classroom}"
 '''

    # print(query_vm)
    # 查询虚拟机信息
    p = Class_VM(cf.get('hj_db', 'db_host'), cf.get('hj_db', 'db_user'), cf.get('hj_db', 'db_pwd'),
                 cf.getint('hj_db', 'db_port'), cf.get('hj_db', 'db'), 'utf8')
    # time.sleep(1)
    root.destroy()
    root.quit()
    for vmname in p.get_vmname(query_vm):
        if obj1.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
            print(f"is not exsit {cf.get('vc1', 'vc_ip')} ")
        # if obj2.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
        #     print(f"is not exsit {cf.get('vc2', 'vc_ip')} ")
        # if obj3.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
        #     print(f"is not exsit {cf.get('vc3', 'vc_ip')} ")
        # if obj4.vmaction(vmname, cf.get('vm_hz', 'vm_hz')) == 0:
        #     print(f"is not exsit {cf.get('vc4', 'vc_ip')} ")

        logger.info(f'正在重置{vmname}')
        # time.sleep(10)


if __name__ == '__main__':
    cf = configparser.ConfigParser()

    cf.read_file(codecs.open('config.ini', "r", "utf-8-sig"))
    # delnetuse = "net use u: /del /y"
    # os.system(delnetuse)
    root = Tk()
    root.title('重启桌面工具')
    root.iconbitmap('1.ico')
    # root.iconphoto('1.ico')

    width = 320
    height = 240
    # Label(root, bg='#C0FF3E', text="汇 捷",font=("华文行楷", 14), ).pack(side="bottom")
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)  # 居中对齐
    root.resizable(0, 0)
    root['background'] = '#C0FF3E'

    comvalue = StringVar()  # 窗体自带的文本，新建一个值

    Label( bg='#C0FF3E', text='教 室:',font = 'Helvetica -16 bold ',fg='red').pack(side=LEFT)
    comboxlist = ttk.Combobox(root, textvariable=comvalue)  # 初始化
    l = Con_mysql(cf.get('hj_db', 'db_host'),cf.get('hj_db', 'db_user'),cf.get('hj_db', 'db_pwd'),cf.get('hj_db', 'db'))
    listroom = l.query("""select DISTINCT CONCAT(a.dg_name,' -->',template_name)
                            from  hj_dg a
                            INNER JOIN hj_vm b on a.id = b.dg_id
                            INNER JOIN hj_template c on c.id = b.template_id""")
    newlistroom = []
    for i in listroom:
        newlistroom.append(i[0])
    comboxlist["values"] = newlistroom
    comboxlist.current(2)  # 选择第一个
    comboxlist.bind("<<ComboboxSelected>>",)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
    comboxlist.pack(side=LEFT,ipady=3)
    button_yes = Button(  root,text='重启', command=go)
    button_yes.pack(side=LEFT,padx=10)

    print(f'注意：1、确保本地电脑可以ping通 172.16.200.104 \n')
    print(f'注意：2、确保本地电脑可以ping通 172.16.200.112 \n')
    print(os.popen('ping 172.16.200.104').read())
    print(os.popen('ping 172.16.200.112').read())
    print(f'注意：3、请选择对应的教室重启云桌面 \n')
    print(f'注意：4、请重启云桌面的教室不要在使用，等待重启完成 \n')
    print(f'注意：5、技术问题请联系轩辕网络工程师：何建平\n')
    root.mainloop()
