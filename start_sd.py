import subprocess
import os
import sys
import time
import threading
from datetime import datetime
from IPython.display import clear_output
import utils as utils

python_executable = sys.executable

python_file = "/root/charmAI/stable-diffusion-webui/launch_nolisten.py"
python_file = "/root/autodl-tmp/stable-diffusion-webui/launch_nolisten.py"

log_dir = "/root/charmAI/log/stable-diffusion-webui"

def start(is_moving=True):
    base_path = utils.get_path(is_moving)
    work_dir = os.path.join(base_path, "stable-diffusion-webui")
    python_file = os.path.join(work_dir, "launch_nolisten.py")

    log_file_name = datetime.now().strftime('%y%m%d-%H%M%S') + '.log'
    log_file_path = os.path.join(log_dir, log_file_name)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    def monitor_process(process):
        while True:
            if process.poll() is None:
                print("SD 正常运行中。。。")
            else:
                print("SD 已经终止，请重新执行")
                break

            time.sleep(5)

    # 指定conda环境路径，这里以默认安装路径为例
    conda_path = "/root/miniconda3/bin/activate"
    conda_env = "charm_env"

    try:
        with open(log_file_path, "w") as log_file:
            # 首先source activate指定的conda环境，然后执行python命令
            # command = [f"source {conda_path} {conda_env} && {python_executable} {python_file}"]
            command = ["/bin/bash", "-c", f"source {conda_path} {conda_env} && {python_executable} {python_file}"]
            # process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT, shell=True, cwd=work_dir)
            process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT, cwd=work_dir)
            print("SD 正在启动。。。")

        # monitor_thread = threading.Thread(target=monitor_process, args=(process,)) 
        # monitor_thread.start()

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        
def stop():
    res = utils.stop(7860)
    # Kill the process if exists
    if res:
        print(f"sd已经停止")
    else:
        print(f"sd未启动")

def is_running():
    res = utils.is_running(7860)
    # Check if the process exists
    if res:
        print(f"sd正在运行")
        return True
    else:
        print(f"sd未启动")
        return False
