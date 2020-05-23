"""
此页面是主程序的GUI界面
Created by CSDN梦栖，2020-05-22
"""

import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import os
import CrawlXueQiu

window = tk.Tk()
window.title('雪球网股票爬取系统')
window.geometry('400x550')

var_source_choose = tk.StringVar()
var_target_choose = tk.StringVar()
var_process_hint = tk.StringVar()


# presenter
def choose_source():
    answer = filedialog.askopenfilename(parent=window,
                                        initialdir=os.getcwd(),
                                        title="请选择源csv文件(请勿含有中文)：")
    if answer is not None:
        var_source_choose.set(answer)
        return answer


def choose_target():
    answer = filedialog.askdirectory(parent=window,
                                     initialdir=os.getcwd(),
                                     title="请选择目标文件夹(请勿含有中文)：")
    if answer is not None:
        var_target_choose.set(answer)
        return answer


def start_crawl():
    if var_source_choose is not None and var_target_choose is not None:
        tk.messagebox.showinfo('请注意', '正在处理...请不要关闭主窗口，任务结束后会有提示！')
        message = "进程：" + CrawlXueQiu.give_message()
        var_process_hint.set(message)
        source = var_source_choose.get()
        target = var_target_choose.get() + "/targetData.csv"
        stock_id_list = CrawlXueQiu.get_source_data(source)
        stock_name_list = CrawlXueQiu.get_source_data_name(source)
        CrawlXueQiu.handle_url(stock_id_list, stock_name_list, target)
        var_process_hint.set('处理完成，请到你设置的输出文件夹下查看...')
        tk.messagebox.showinfo('处理结果', '爬取完成，请到对应位置进行查看！')


# welcome image
canvas = tk.Canvas(window, height=235, width=400)
image_file = tk.PhotoImage(file='assets/spider.gif')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# label
tk.Label(window, text='选择源csv文件(请勿含有中文):').place(x=30, y=260)
tk.Label(window, text='选择爬取结果保存位置(同上):').place(x=30, y=300)
tk.Label(window, text='源路径:').place(x=10, y=400)
tk.Label(window, textvariable=var_source_choose).place(x=10, y=430)
tk.Label(window, text='目标文件夹(输出文件为targetData.csv):').place(x=10, y=460)
tk.Label(window, textvariable=var_target_choose).place(x=10, y=490)
tk.Label(window, textvariable=var_process_hint).place(x=10, y=520)

# Button
b1 = tk.Button(window, text='点击选择源csv文件', width=25, height=1, bg='#efffff', activebackground='#aaaaaa',
               command=choose_source, relief='raised', bd=1).place(x=200, y=255)
b2 = tk.Button(window, text='点击选择目的路径', width=25, height=1, bg='#efffff', activebackground='#aaaaaa',
               command=choose_target, relief='raised', bd=1).place(x=200, y=295)

# start button
b3 = tk.Button(window, text='开始爬取', width=25, height=1, bg='#efffff', activebackground='#aaaaaa', command=start_crawl,
               relief='raised', bd=1).place(x=120, y=350)

window.mainloop()
