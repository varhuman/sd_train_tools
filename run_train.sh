#!/bin/bash

# 定义工作目录和Python文件
work_dir="/root/autodl-tmp/lora-scripts-for-api"
python_file="main.py"

# 创建日志目录
log_dir="/root/charmAI/log/lora-scripts-for-api"
mkdir -p $log_dir

# 创建带时间戳的日志文件名
log_file_name=$(date +"%y%m%d-%H%M%S").log
log_file_path="$log_dir/$log_file_name"

# 检查28000端口是否在使用，并可能中断该进程
PORT_IN_USE=$(lsof -i :28000 -t)
if [ ! -z "$PORT_IN_USE" ]; then
  echo "已有lora训练在运行。。。尝试终止"
  kill -9 $PORT_IN_USE
  echo "进程已终止。"
fi

# 进入工作目录
cd $work_dir

# 初始化conda命令并激活环境
source $(conda info --base)/etc/profile.d/conda.sh
conda activate train_env
echo "开始启动lora训练。。"
python $python_file >> $log_file_path 2>&1
