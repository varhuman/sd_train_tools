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


work_dir = "lora-scripts-for-api"
python_file= "main.py"

log_dir = "/root/charmAI/log/lora-scripts-for-api"

def start(is_moving=True):
    base_path = utils.get_path(is_moving)
    print(base_path)
    
    work_dir = os.path.join(base_path, "lora-scripts-for-api")
    python_file = "main.py"

    log_file_name = datetime.now().strftime('%y%m%d-%H%M%S') + '.log'
    log_file_path = os.path.join(log_dir, log_file_name)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    def monitor_process(process):
        while True:
            if process.poll() is None:
                print("lora训练 正常运行中。。。")
            else:
                print("lora训练 已经终止，请重新执行")
                break

            time.sleep(5)

    
    # 指定conda环境路径，这里以默认安装路径为例
    conda_path = "/root/miniconda3/bin/activate"
    conda_env = "train_env"

    try:
        with open(log_file_path, "w") as log_file:
            command = f"source $(conda info --base)/etc/profile.d/conda.sh && conda activate train_env && {python_executable} {python_file}"
            process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT, shell=True, cwd=work_dir)

            print("lora训练 正在启动。。。")

        # monitor_thread = threading.Thread(target=monitor_process, args=(process,))
        # monitor_thread.start()

    except Exception as e:
        print(f"Error occurred: {str(e)}")

def stop():
    res = utils.stop(28000)
    # Kill the process if exists
    if res:
        print(f"训练已经停止")
    else:
        print(f"训练未启动")

def is_running():
    res = utils.is_running(28000)
    # Check if the process exists
    if res:
        print(f"训练正在运行")
        return True
    else:
        print(f"训练未启动")
        return False

start()