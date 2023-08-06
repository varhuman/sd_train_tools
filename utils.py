import subprocess
def get_path(is_moving: bool):
    if is_moving:
        return "/root/autodl-tmp/"
    else:
        return "/root/charmAI/"
    


def is_running(port: int):
    proc = subprocess.Popen(['lsof', '-t', '-i:%d' % port], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    # Check if the process exists
    if out:
        return True
    else:
        return False

def stop(port: int):
    proc = subprocess.Popen(['lsof', '-t', '-i:%d' % port], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    # Kill the process if exists
    if out:
        pid = out.strip()
        subprocess.run(['kill', '-9', pid])
        return True
    else:
        return False