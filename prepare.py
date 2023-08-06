import subprocess
import re

def start_nginx():
    """启动 Nginx 服务"""
    try:
        subprocess.run(["service", "nginx", "start"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("启动Nginx服务失败。请确保你有足够的权限，并且Nginx已经正确安装。")
        return False

def check_nginx():
    """检查 Nginx 服务是否正常运行"""
    try:
        completed_process = subprocess.run(["service", "nginx", "status"], text=True, capture_output=True, check=True)
        # 一般来说，如果 Nginx 正在运行，状态信息里会包含 'running' 字样
        if re.search(r'running', completed_process.stdout, re.IGNORECASE):
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        print("无法获取Nginx服务状态。请确保你有足够的权限，并且Nginx已经正确安装。")
        return False


def start():
    print("正在启动Nginx服务...")
    if start_nginx():
        print("Nginx服务已经启动。")
    else:
        print("Nginx服务启动失败。")
    return

def check():
    print("正在检查Nginx服务...")
    if check_nginx():
        print("Nginx服务正常运行。")
        return True
    else:
        print("Nginx服务未正常运行。")
    return False