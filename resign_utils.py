#encoding: utf-8

import getopt
import os
import sys
import shutil
import time
import zipfile
import plistlib

script_path = os.path.dirname(__file__)  # 脚本所在目录
sign_extensions = ['.framework/', '.dylib', '.appex/', '.app/']

def execute_cmd(cmd):
    process = os.popen(cmd)
    output = process.read()
    process.close()
    return output

def copy(file, dst):
    shutil.copy(file, dst)

def rename(file_path, new_file_name):
    fileDir, fileName = os.path.split(file_path)
    os.rename(file_path, os.path.join(fileDir, new_file_name))    

# 删除目录
def remove_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

# 解压文件
def unzip_file(source_file, output_path):
    zip_obj = zipfile.ZipFile(source_file, 'r')
    zip_file_list = zip_obj.namelist()
    zip_file_list.reverse()
    zip_obj.extractall(output_path)
    zip_obj.close()
    return zip_file_list        

# 压缩文件
def zip_file(source_path, output_path):
    zip_file = zipfile.ZipFile(output_path, 'w')
    pre_len  = len(os.path.dirname(source_path))
    for parent, dir_names, file_names in os.walk(source_path):
        for file_name in file_names:
            pathFile = os.path.join(parent, file_name)
            arc_name = pathFile[pre_len:].strip(os.path.sep)
            zip_file.write(pathFile, arc_name)
    zip_file.close()

# 拼接空白路径
def handleWhiteSpace(name):
    space = name.lstrip().rstrip()
    return space.replace('\n', '')

def is_need_sign(file_name):
    for sign_extension in sign_extensions:
        if sign_extension == file_name[file_name.rfind('.'):]:
            return True
    return False

    
