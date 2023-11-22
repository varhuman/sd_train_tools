# start_train.py

# import necessary packages
import subprocess
import os
import sys
import time
import threading
from datetime import datetime
from IPython.display import clear_output
import utils as utils
python_executable = sys.executable

def gpu_tool_start(is_moving=True):
    base_path = utils.get_path(is_moving)
    work_dir = os.path.join(base_path, "aistron-gpu-tools")
    python_file = os.path.join(work_dir, "app.py")
    log_dir = "/root/charmAI/log/gpu_tool"
    log_file_name = datetime.now().strftime('%y%m%d-%H%M%S') + '.log'
    log_file_path = os.path.join(log_dir, log_file_name)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        with open(log_file_path, "w") as log_file:
            process = subprocess.Popen([python_executable, python_file], stdout=log_file, stderr=subprocess.STDOUT, cwd=work_dir)
            print("gpu工具 正在启动。。。")

    except Exception as e:
        print(f"Error occurred: {str(e)}")


def start(is_moving=True):
    gpu_tool_start(is_moving)
    python_file= "app.py"
    log_dir = "/root/charmAI/log/model_tools"
    base_path = utils.get_path(is_moving)
    work_dir = os.path.join(base_path, "model_tools")
    python_file = os.path.join(work_dir, "app.py")

    log_file_name = datetime.now().strftime('%y%m%d-%H%M%S') + '.log'
    log_file_path = os.path.join(log_dir, log_file_name)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    def monitor_process(process):
        while True:
            if process.poll() is None:
                print("工具 正常运行中。。。")
            else:
                print("工具 已经终止，请重新执行")
                break

            time.sleep(5)

    try:
        with open(log_file_path, "w") as log_file:
            process = subprocess.Popen([python_executable, python_file], stdout=log_file, stderr=subprocess.STDOUT, cwd=work_dir)
            print("工具 正在启动。。。")

        # monitor_thread = threading.Thread(target=monitor_process, args=(process,))
        # monitor_thread.start()

    except Exception as e:
        print(f"Error occurred: {str(e)}")

def stop():
    res = utils.stop(7888)
    # Kill the process if exists
    if res:
        print(f"工具已经停止")
    else:
        print(f"工具未启动")

def is_running():
    res = utils.is_running(7888)
    # Check if the process exists
    if res:
        print(f"工具正在运行")
        return True
    else:
        print(f"工具未启动")
        return False
