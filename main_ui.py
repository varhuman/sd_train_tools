import ipywidgets as widgets
from ipywidgets import Layout,Label, HBox, VBox
import sys
import start_sd
# import start_train
import move
import start_tool
import prepare
python_executable = sys.executable
import utils as utils

isMoving = False

sd_port = 7860
train_port = 28000
tool_port = 7888

output_port = 6006

def getUi():
    out = widgets.Output(layout={'border': '1px solid black'})
    
    line = widgets.HTML(
        value="<hr>",
    )
    white_line = widgets.HTML(
        value="<br>",
    )
    
    # ======================
    
    auth_set_tip = widgets.HTML(
        value="<font size='2' color='red'>TIP:首次运行请移动，之后直接点击环境准备并检查是否正常，最后点击一键运行并检查是否正常即可/font>",
    )

    move_buttom = widgets.Button(
        description='移动',
        button_style='success'
    )
    run_pre_buttom = widgets.Button(
        description='环境准备',
        button_style='success'
    )
    pre_is_ok_buttom = widgets.Button(
        description='检查环境是否正常',
        button_style='success'
    )
    run_all_buttom = widgets.Button(
        description='一键运行',
        button_style='success'
    )

    run_all_is_ok_buttom = widgets.Button(
        description='检查是否成功运行',
        button_style='success'
    )

    run_sd_buttom = widgets.Button(
        description='运行SD',
        button_style='success'
    )
    run_train_buttom = widgets.Button(
        description='运行训练',
        button_style='success'
    )
    run_tool_buttom = widgets.Button(
        description='运行工具',
        button_style='success'
    )

    stop_train_buttom = widgets.Button(
        description='停止训练',
        button_style='danger'
    )

    stop_sd_buttom = widgets.Button(
        description='停止SD',
        button_style='danger'
    )
    
    stop_tool_buttom = widgets.Button(
        description='停止工具',
        button_style='danger'
    )
        
    # ======================


    #运行函数

    def move_click(self):
        with out:
            out.clear_output()
            print("正在移动...")
            print("请稍等...")
            move.start()

    def run_pre_click(self):
        with out:
            out.clear_output()
            print("正在准备环境...")
            print("请稍等...")
            prepare.start()

    def run_sd_click(self):
        with out:
            out.clear_output()
            print("正在启动SD...")
            print("请稍等...")
            start_sd.start()

    # def run_train_click(self):
    #     with out:
    #         out.clear_output()
    #         print("正在启动训练...")
    #         print("请稍等...")
    #         start_train.start()
        
    def run_tool_click(self):
        with out:
            out.clear_output()
            print("正在启动工具...")
            print("请稍等...")
            start_tool.start()
    
    def stop_train_click(self):
        with out:
            out.clear_output()
            print("正在停止训练...")
            print("请稍等...")            
            res = utils.stop(train_port)
            if res:
                print("训练停止成功")
            else:
                print("训练停止失败，或者是训练未在运行")


    def stop_sd_click(self):
        with out:
            out.clear_output()
            print("正在停止SD...")
            print("请稍等...")
            res = utils.stop(sd_port)
            if res:
                print("SD停止成功")
            else:
                print("SD停止失败，或者是SD未在运行")
            
    def stop_tool_click(self):
        with out:
            out.clear_output()
            print("正在停止工具...")
            print("请稍等...")
            res = utils.stop(tool_port)
            if res:
                print("工具停止成功")
            else:
                print("工具停止失败，或者是SD未在运行")

    def check_pre(self):
        with out:
            out.clear_output()

            res = prepare.check()
            if res:
                print("环境正常, 请点击一键运行")
            else:
                print("环境异常,请点击”环境准备“按钮尝试重启")

    def check_all_is_running_click(self):
        with out:
            out.clear_output()
            print("正在检查是否成功运行...")
            res = utils.is_running(train_port)
            if res:
                print("Lora训练运行成功")
            else:
                print("Lora训练运行失败,请点击”启动lora训练“按钮尝试重启")
            
            res = utils.is_running(sd_port)
            if res:
                print("SD运行成功")
            else:
                print("SD运行失败,请点击”启动SD“按钮尝试重启")

            res = utils.is_running(tool_port)
            if res:
                print("工具运行成功")
            else:
                print("工具运行失败,请点击”启动工具“按钮尝试重启")

    def run_all_click(self):
        with out:
            out.clear_output()
            print("一键启动中")
            start_sd.start()
            # start_train.start()
            start_tool.start()
    
    #绑定加速函数
    run_sd_buttom.on_click(run_sd_click)
    # run_train_buttom.on_click(run_train_click)
    run_tool_buttom.on_click(run_tool_click)
    stop_train_buttom.on_click(stop_train_click)
    stop_sd_buttom.on_click(stop_sd_click)
    stop_tool_buttom.on_click(stop_tool_click)
    run_all_is_ok_buttom.on_click(check_all_is_running_click)
    run_all_buttom.on_click(run_all_click)
    run_pre_buttom.on_click(run_pre_click)
    pre_is_ok_buttom.on_click(check_pre)
    move_buttom.on_click(move_click)

    return VBox([
        auth_set_tip,
        line,
        white_line,
        move_buttom,
        line,
        run_pre_buttom,
        pre_is_ok_buttom,
        line,
        run_all_buttom,
        run_all_is_ok_buttom,
        line,
        run_sd_buttom,
        # run_train_buttom,
        run_tool_buttom,
        line,
        # stop_train_buttom,
        stop_sd_buttom,
        stop_tool_buttom,
        out
    ])

def show():
    tab_titles = ['主页']
    children = [getUi()]

    tab = widgets.Tab()
    tab.children = children
    for i in range(len(tab_titles)):
        tab.set_title(i, tab_titles[i])

    is_moving = move.is_moving()
    display(tab)