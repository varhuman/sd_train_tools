import os
import shutil
import psutil
import math

def get_size(start_path='.'):
    total_size = 0
    if os.path.isfile(start_path):
        return os.path.getsize(start_path)
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def check_disk_space(source_path, target_path):
    # get size of source path
    source_size = get_size(source_path)
    print(f"Size of {source_path}: {convert_size(source_size)}")
    
    # get free space at target path
    target_free_space = psutil.disk_usage(target_path).free
    print(f"Free space at {target_path}: {convert_size(target_free_space)}")

    # return True if there is enough space, False otherwise
    return source_size <= target_free_space

def move_folder(src_folder, target_parent, description):
    # 检查源文件夹是否存在
    if not os.path.exists(src_folder):
        print(f"{description}地址错误")
        return

    # 检查是否有足够的磁盘空间
    if not check_disk_space(src_folder, target_parent):
        print(f"{description}移动，磁盘空间不够")
        return

    # 构造完整的目标路径
    target_folder = os.path.join(target_parent, os.path.basename(src_folder))

    # 如果目标文件夹存在，则删除它
    if os.path.exists(target_folder):
        print(f"目标文件夹{target_folder}存在，正在删除...")
        shutil.rmtree(target_folder)

    # 移动源文件夹到目标路径
    shutil.move(src_folder, target_parent)
    print(f"移动{description}成功!")

def copy_model(model, target):
    if not os.path.exists(model):
        print(f"模型地址错误 : {model} ")
        return
    # check if there is enough disk space
    if not check_disk_space(model, target):
        print(f"{model}模型复制，{target}磁盘空间不够")
        return
    # move source3 to target
    shutil.copy(model, target)
    print("复制模型成功!")


def copy_model_folder(source_folder, target_folder):
    if not os.path.exists(source_folder):
        print(f"源文件夹路径错误 : {source_folder}")
        return

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)

        # 如果是文件（而不是目录）则复制
        if os.path.isfile(source_file):
            # 创建目标文件夹（如果它还不存在）
            print("尝试创建目标文件夹：", target_folder)
            os.makedirs(target_folder, exist_ok=True)

            # 首先检查目标磁盘是否有足够的空间
            if not check_disk_space(source_file, target_folder):
                print(f"复制模型 {source_file}失败，{target_folder}磁盘空间不够")
                continue  # 跳过这个文件，继续下一个

            # 复制文件
            shutil.copy(source_file, target_folder)
            print(f"成功复制模型：{source_file}")

    print(f"完成{source_folder}模型复制")

def copy_all_model_folder(source_folder, target_folder):
    if not os.path.exists(source_folder):
        print(f"源文件夹路径错误 : {source_folder}")
        return
    
    os.makedirs(os.path.dirname(target_folder), exist_ok=True)
    if os.path.exists(target_folder):
        print(f"目标文件夹{target_folder}存在，正在删除...")
        shutil.rmtree(target_folder)
    # 使用shutil.copytree递归复制整个目录结构
    shutil.copytree(source_folder, target_folder)

    print(f"完成{source_folder}模型复制")

def delete_models():
    models_folder = "/root/autodl-tmp/models/"
    if os.path.exists(models_folder):
        print(f"目标文件夹{models_folder}存在，正在删除...")
        shutil.rmtree(models_folder)

def move_files_and_log(sd, lora_train, model_tools, target):
    try:
        print("开始移动工程。。。")
        move_folder(sd, target, "sd")
        move_folder(lora_train, target, "lora训练")
        move_folder(model_tools, target, "工具")

        print("开始复制模型。。。")
        model1_folder = "/root/autodl-tmp/models/sd/"
        dst1 = "/root/autodl-tmp/stable-diffusion-webui/models/Stable-diffusion"
        dst2 = "/root/autodl-tmp/lora-scripts-for-api/sd-models"
        # move model
        copy_model_folder(model1_folder, dst1)
        copy_model_folder(model1_folder, dst2)

        model1_folder2 = "/root/autodl-tmp/models/lora/"
        dst3 = "/root/autodl-tmp/stable-diffusion-webui/models/Lora"
        # move model
        copy_model_folder(model1_folder2, dst3)

        model2 = "/root/autodl-tmp/stable-diffusion-webui/models/deepdanbooru/model-resnet_custom_v3.h5"
        target2 = "/root/autodl-tmp/stable-diffusion-webui/models/torch_deepdanbooru"
        copy_model(model2, target2)
                
        controlnet_zoedepth_model_folder = "/root/autodl-tmp/models/roop/"
        target2 = "/root/autodl-tmp/stable-diffusion-webui/models/roop/"
        copy_model_folder(controlnet_zoedepth_model_folder, target2)

        codeformer_model_folder = "/root/autodl-tmp/models/codeformer/"
        codeformer_target = "/root/autodl-tmp/stable-diffusion-webui/models/Codeformer/"
        copy_model_folder(codeformer_model_folder, codeformer_target)

        model3_folder = "/root/autodl-tmp/models/clip/"
        target3 = "/root/.cache/clip/"
        copy_model_folder(model3_folder, target3)

        controlnet_model_folder = "/root/autodl-tmp/models/controlnet/"
        target4 = "/root/autodl-tmp/stable-diffusion-webui/extensions/sd-webui-controlnet/models/"
        copy_model_folder(controlnet_model_folder, target4)

        controlnet_midas_model_folder = "/root/autodl-tmp/models/midas/"
        target5 = "/root/autodl-tmp/stable-diffusion-webui/extensions/sd-webui-controlnet/annotator/downloads/midas/"
        copy_model_folder(controlnet_midas_model_folder, target5)

        controlnet_zoedepth_model_folder = "/root/autodl-tmp/models/zoedepth/"
        target7 = "/root/autodl-tmp/stable-diffusion-webui/extensions/sd-webui-controlnet/annotator/downloads/zoedepth/"
        copy_model_folder(controlnet_zoedepth_model_folder, target7)

        pytorch_model_folder = "/root/autodl-tmp/models/models--openai--clip-vit-large-patch14/"
        target6 = "/root/.cache/huggingface/hub/models--openai--clip-vit-large-patch14/"
        copy_model_folder(pytorch_model_folder, target6)

        pytorch_model_folder = "/root/autodl-tmp/models/models--bert-base-uncased/"
        bert_base = "/root/.cache/huggingface/hub/models--bert-base-uncased/"
        
        copy_all_model_folder(pytorch_model_folder, bert_base)

        ifnude_folder = "/root/autodl-tmp/models/ifnude/"
        target8 = "/root/.ifnude/"
        
        copy_model_folder(ifnude_folder, target8)
        
        buffalo_l_folder = "/root/autodl-tmp/models/buffalo_l/"
        target9 = "/root/.insightface/models/buffalo_l/"
        
        copy_model_folder(buffalo_l_folder, target9)

        delete_models()
        print("已经全部完成!!!!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")


def start():
    # define source and target paths
    # source1 = "/root/autodl-tmp/stable-diffusion-webui"
    # source2 = "/root/autodl-tmp/lora-scripts-for-api"

    source1 = "/root/charmAI/stable-diffusion-webui"
    source2 = "/root/charmAI/lora-scripts-for-api"
    source3 = "/root/charmAI/model_tools"
    target = "/root/autodl-tmp"

    # call the function
    move_files_and_log(source1, source2, source3, target)


def is_moving():
    # define source and target paths
    source1 = "/root/autodl-tmp/stable-diffusion-webui"
    source2 = "/root/autodl-tmp/lora-scripts-for-api"
    source3 = "/root/autodl-tmp/model_tools"

    if os.path.exists(source1) or os.path.exists(source2) or os.path.exists(source3):
        return True

    return False