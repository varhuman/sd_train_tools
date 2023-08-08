#!/bin/bash

echo "开始复制文件夹：/root/autodl-fs/models/ 到 /root/autodl-tmp/"

rm -rf /root/autodl-tmp/models/

cp -r /root/autodl-fs/models/ /root/autodl-tmp/

echo "复制完成！"
