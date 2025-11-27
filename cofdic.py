#!/usr/bin/env python3
# coding=utf-8
# update: 2025-11-27
# author: Cof-Lee <cof8007@gmail.com>
# this module uses the GPL-3.0 open source protocol

import tkinter
from tkinter import messagebox
from tkinter import font


class MainWindow:
    def __init__(self, width=800, height=480, title=''):
        self.about_info_list = ["CofDic，开源的离线本地词典",
                                "版本:  v251127",
                                "本软件使用GPL-v3.0协议开源",
                                "作者:  李茂福（Cof-Lee）",
                                "更新时间: 2025-11-27",
                                "开源地址: https://github.com/limaofu/CofDic"]
        self.title = title  # 主程序标题
        self.width = width  # 主程序界面宽度（单位：像素）
        self.height = height  # 主程序界面高度（单位：像素）
        self.resizable = False  # False 表示宽度和高度不可由用户手动调整
        self.minsize = (480, 320)  # 主程序界面最小尺寸
        self.maxsize = (1920, 1080)  # 主程序界面最大尺寸
        self.background = "#3A3A3A"  # 主窗口背景色，RGB
        self.window_obj = None  # 主窗口对象，在 MainWindow.show()里创建
        self.menu_bar = None  # 菜单栏，在 MainWindow.create_menu_bar_init()里创建
        self.frame_nav = None  # 导航栏frame，在 MainWindow.create_frame_nav()里创建
        self.frame_nav_height = 30  # 导航栏frame高度（单位：像素）
        self.frame_nav_button_width = 12  # 导航栏frame里的button宽度（单位：字符）
        self.frame_main_func = None  # 功能界面主frame，在 MainWindow.create_frame_main_func()里创建
        self.frame_main_func_height = self.height - self.frame_nav_height  # 功能界面主frame高度（单位：像素）
        # 在 功能界面主frame 里创建若干个功能子窗口
        self.frame_main_func_search_page = None  # 功能界面主frame里的 search 窗口
        self.frame_main_func_edit_page = None  # 功能界面主frame里的 edit 窗口
        self.frame_main_func_memorize_vocabulary_page = None  # 功能界面主frame里的 memorize_vocabulary 窗口
        self.screen_width = 0  # 在 MainWindow.show()里赋值
        self.screen_height = 0  # 在 MainWindow.show()里赋值
        self.padx = 2
        self.pady = 2
        self.view_width = 20
        self.text_font = None  # 全局字体
        self.font_family = ""  # 全局字体
        self.font_size = 18  # 全局字体大小
        self.page_index_search = 0
        self.page_index_edit = 1
        self.page_index_memorize_vocabulary = 2
        self.widget_dict_search = {}  # search 界面的控制对象字典
        self.widget_dict_edit = {}  # edit 界面的控制对象字典
        self.widget_dict_memorize_vocabulary = {}  # memorize_vocabulary 界面的控制对象字典

    def show(self):
        self.window_obj = tkinter.Tk()  # ★★★创建主窗口对象★★★
        self.screen_width = self.window_obj.winfo_screenwidth()
        self.screen_height = self.window_obj.winfo_screenheight()
        self.window_obj.title(self.title)  # 设置窗口标题
        # self.window_obj.iconbitmap(bitmap="D:\\test.ico")  # 设置窗口图标，默认为羽毛图标
        win_pos_x = self.screen_width // 2 - self.width // 2
        win_pos_y = self.screen_height // 2 - self.height // 2
        win_pos = f"{self.width}x{self.height}+{win_pos_x}+{win_pos_y}"
        self.window_obj.geometry(win_pos)  # 设置窗口大小及位置，居中
        self.window_obj.resizable(width=self.resizable, height=self.resizable)  # 若值为 True 则表示宽度和高度可由用户手动调整
        self.window_obj.minsize(*self.minsize)  # 可调整的最小宽度及高度
        self.window_obj.maxsize(*self.maxsize)  # 可调整的最大宽度及高度
        self.window_obj.pack_propagate(True)  # True表示窗口内的控件大小自适应
        self.window_obj.configure(bg=self.background)  # 设置主窗口背景色，RGB
        # 加载初始化界面控件
        self.load_main_window_init_widget()  # ★★★ 接下来，所有的事情都在此界面操作 ★★★
        # 主窗口点击右上角的关闭按钮后，触发此函数
        self.window_obj.protocol("WM_DELETE_WINDOW", self.on_closing_main_window)
        # 运行窗口主循环
        self.window_obj.mainloop()

    def load_main_window_init_widget(self):
        """
        加载程序初始化界面控件
        """
        # 首先清空主window
        self.clear_tkinter_widget(self.window_obj)
        # 设置全局字体
        self.text_font = font.Font(size=self.font_size, family=self.font_family)
        # 加载菜单栏
        self.create_menu_bar_init()
        # 加载导航栏
        self.create_frame_nav()
        # 添加功能窗口（默认为 search 查询单词 界面）
        self.create_frame_main_func()

    def create_menu_bar_init(self):
        """
        创建菜单栏-主界面的
        创建完菜单栏后，一般不会再修改此组件了
        """
        self.menu_bar = tkinter.Menu(self.window_obj)  # 创建一个菜单，做菜单栏
        # 创建一个菜单，做1级子菜单，不分窗（表示此菜单不可拉出来变成一个可移动的独立弹窗）
        menu_help = tkinter.Menu(self.menu_bar, tearoff=0, activebackground="green", activeforeground="white",
                                 background="white", foreground="black")
        # 菜单栏添加1级子菜单
        self.menu_bar.add_cascade(label="Help", menu=menu_help)
        # 1级子菜单添加2级子菜单（功能按钮）
        menu_help.add_command(label="About", command=self.click_menu_about_of_menu_bar_init)
        # 主窗口添加菜单栏
        self.window_obj.config(menu=self.menu_bar)

    def click_menu_about_of_menu_bar_init(self):
        messagebox.showinfo("About", "\n".join(self.about_info_list))

    def create_frame_nav(self):
        # 创建导航栏frame
        self.frame_nav = tkinter.Frame(self.window_obj, bg="green", borderwidth=1, width=self.width, height=self.frame_nav_height,
                                       relief='groove')
        self.frame_nav.grid_propagate(False)
        self.frame_nav.pack_propagate(False)
        self.frame_nav.grid(row=0, column=0)
        # search-界面按钮
        menu_button_search = tkinter.Button(self.frame_nav, text="查询单词", width=self.frame_nav_button_width, height=1, bg="white",
                                            command=self.frame_main_func_search_page_display)
        menu_button_search.pack(side=tkinter.LEFT, padx=self.padx)
        # edit-界面按钮
        menu_button_edit = tkinter.Button(self.frame_nav, text="编辑模式", width=self.frame_nav_button_width, height=1,
                                          bg="white",
                                          command=self.frame_main_func_edit_page_display)
        menu_button_edit.pack(side=tkinter.LEFT, padx=self.padx)
        # memorize_vocabulary-界面按钮
        menu_button_memorize_vocabulary = tkinter.Button(self.frame_nav, text="记单词", width=self.frame_nav_button_width, height=1,
                                                         bg="white", command=self.frame_main_func_memorize_vocabulary_page_display)
        menu_button_memorize_vocabulary.pack(side=tkinter.LEFT, padx=self.padx)

    def create_frame_main_func(self):
        # 创建功能界面主frame
        self.frame_main_func = tkinter.Frame(self.window_obj, bg="pink", borderwidth=0, width=self.width,
                                             height=self.frame_main_func_height)
        self.frame_main_func.grid_propagate(False)
        self.frame_main_func.pack_propagate(False)
        self.frame_main_func.grid(row=1, column=0)
        # 创建3个功能界面子frame
        self.frame_main_func_search_page = tkinter.Frame(self.frame_main_func, bg="#222222", borderwidth=0, width=self.width,
                                                         height=self.frame_main_func_height)
        self.frame_main_func_edit_page = tkinter.Frame(self.frame_main_func, bg="#333333", borderwidth=0, width=self.width,
                                                       height=self.frame_main_func_height)
        self.frame_main_func_memorize_vocabulary_page = tkinter.Frame(self.frame_main_func, bg="#444444", borderwidth=0, width=self.width,
                                                                      height=self.frame_main_func_height)
        # 初始化3个功能界面
        self.init_search_page()
        self.init_edit_page()
        self.init_memorize_vocabulary_page()
        # 首次打开程序，显示的是 search 查询单词 界面
        widget_index = 0
        for widget in self.frame_nav.winfo_children():
            if widget_index == self.page_index_search:
                widget.config(bg="pink")
            else:
                widget.config(bg="white")
            widget_index += 1
        self.frame_main_func_search_page.place(x=0, y=0, width=self.width, height=self.frame_main_func_height)
        self.widget_dict_search["entry_input_word"].focus_force()  # 使输入框聚焦

    def init_search_page(self):
        # 添加控件
        # 输入要查询的单词
        label_input_word = tkinter.Label(self.frame_main_func_search_page, text="输入要查询的单词:")  # ip信息为【必填】
        label_input_word.grid(row=0, column=0, padx=self.padx, pady=self.pady)
        self.widget_dict_search["sv_input_word"] = tkinter.StringVar()
        self.widget_dict_search["entry_input_word"] = tkinter.Entry(self.frame_main_func_search_page,
                                                                    textvariable=self.widget_dict_search["sv_input_word"], width=48,
                                                                    bg="#e2deff")
        self.widget_dict_search["entry_input_word"].grid(row=0, column=1, columnspan=2, padx=self.padx, pady=self.pady)
        self.widget_dict_search["entry_input_word"].bind("<KeyPress>", self.front_end_input_func_printable_char_search)  # 监听键盘输入的字符
        button_search = tkinter.Button(self.frame_main_func_search_page, text="查询", width=12, command=self.search_word)
        button_search.grid(row=0, column=3, padx=self.padx, pady=self.pady)

    def init_edit_page(self):
        pass

    def init_memorize_vocabulary_page(self):
        pass

    def frame_main_func_search_page_display(self):
        # 更新导航框架 self.frame_nav 的当前选项卡背景色
        widget_index = 0
        for widget in self.frame_nav.winfo_children():
            if widget_index == self.page_index_search:
                widget.config(bg="pink")
            else:
                widget.config(bg="white")
            widget_index += 1
        # 显示 search 页面
        self.frame_main_func_edit_page.place_forget()
        self.frame_main_func_memorize_vocabulary_page.place_forget()
        self.frame_main_func_search_page.place(x=0, y=0, width=self.width, height=self.frame_main_func_height)
        # self.widget_dict_search["entry_input_ip"].focus_force()  # 使输入框聚焦

    def frame_main_func_edit_page_display(self):
        # 更新导航框架 self.frame_nav 的当前选项卡背景色
        widget_index = 0
        for widget in self.frame_nav.winfo_children():
            if widget_index == self.page_index_edit:
                widget.config(bg="pink")
            else:
                widget.config(bg="white")
            widget_index += 1
        # 显示 edit 页面
        self.frame_main_func_search_page.place_forget()
        self.frame_main_func_memorize_vocabulary_page.place_forget()
        self.frame_main_func_edit_page.place(x=0, y=0, width=self.width, height=self.frame_main_func_height)
        # self.widget_dict_edit["entry_input_ip"].focus_force()  # 使输入框聚焦

    def frame_main_func_memorize_vocabulary_page_display(self):
        # 更新导航框架 self.frame_nav 的当前选项卡背景色
        widget_index = 0
        for widget in self.frame_nav.winfo_children():
            if widget_index == self.page_index_memorize_vocabulary:
                widget.config(bg="pink")
            else:
                widget.config(bg="white")
            widget_index += 1
        # 显示 memorize_vocabulary 页面
        self.frame_main_func_search_page.place_forget()
        self.frame_main_func_edit_page.place_forget()
        self.frame_main_func_memorize_vocabulary_page.place(x=0, y=0, width=self.width, height=self.frame_main_func_height)
        # self.widget_dict_memorize_vocabulary["entry_input_ip"].focus_force()  # 使输入框聚焦

    def front_end_input_func_printable_char_search(self, event):
        """
        处理普通可打印字符，控制键及组合按键
        ★★★ 按键，ascii字符，vt100控制符是3个不同的概念
        按键可以对应一个字符，也可没有相应字符，
        按下shift/ctrl等控制键后再按其他键，可能会产生换档字符（如按下shift加数字键2，产生字符@）
        vt100控制符是由ESC（十六进制为\0x1b，八进制为\033）加其他可打印字符组成，比如:
        按键↑（方向键Up）对应的vt100控制符为 ESC加字母OA，即b'\033OA'
        ★★★
        """
        # print("普通字符输入如下：")
        # print(event.keysym)
        # print(event.keycode)
        # 非可打印字符没有event.char，event.char为空，只有event.keycode
        if event.keysym == "Return":
            self.search_word()

    def search_word(self):
        pass

    @staticmethod
    def clear_tkinter_widget(root):
        for widget in root.winfo_children():
            widget.destroy()

    def on_closing_main_window(self):
        # self.clear_tkinter_widget()
        self.window_obj.quit()
        print("MainWindow.on_closing_main_window: 退出了主程序")


if __name__ == "__main__":
    # 创建程序主界面对象，全局只有一个
    main_window_obj = MainWindow(width=900, height=600, title='CofDic')
    main_window_obj.show()  # 显示主界面，一切从这里开始
