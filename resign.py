#encoding: utf-8
import sys
import os
import shutil
import time

import resign_utils
#重签名流程
#1.解压ipa
#2.删除旧签名
#3.复制新描述文件
#4.用新的证书
#5.压缩ipa
#security find-identity -v -p codesigning 可以查看当前电脑安装的证书

class Resign:

    def __init__(self):
        #ipa解压后文件列表
        self.zip_file_list = None
        # 解压后的app路径
        self.app_temp_path = '' 
        self.current_path    = os.path.dirname(__file__)                                # 脚本所在目录
        self.temp_file_dir   = os.path.join(self.current_path, 'temp')                  # 临时文件夹目录
        self.entitle_plist   = os.path.join(self.temp_file_dir, 'entitlements.plist')   # 生成的plist信息
        self.output_ipa_path = os.path.join(self.current_path,  'output','%s.ipa' % str(int(time.time())) ) # 默认输出ipa文件的路径
        print('output_ipa_path ==>%s' % self.output_ipa_path)  

# 处理原ipa文件
    def unzip_ipa(self,ipa_path):
        if os.path.exists(ipa_path):
            if '.ipa' in ipa_path:
                resign_utils.remove_dir(self.temp_file_dir)
                self.zip_file_list = resign_utils.unzip_file(ipa_path, self.temp_file_dir)
                payload_path       = os.path.join(self.temp_file_dir, 'Payload')
                app_PackageName    = resign_utils.execute_cmd('ls %s' % (payload_path))
                app_path           = os.path.join(payload_path, app_PackageName)
                self.app_temp_path = resign_utils.handleWhiteSpace(app_path)
                print('app_temp_path   ==>%s' % self.app_temp_path)
            else:
                print('文件格式非法')
        else:
            print('文件不存在')

    def zip_ipa(self):
        resign_utils.zip_file(os.path.join(self.temp_file_dir, 'Payload'), self.output_ipa_path)
        resign_utils.remove_dir(self.temp_file_dir)

    # 根据pp文件导出Entitlements信息
    def export_sign_info(self,pp_path):
        temp_plist = os.path.join(self.temp_file_dir, 'entitlements_temp.plist')

        cmd = 'security cms -D -i "%s" > %s' % (pp_path, temp_plist)
        result = resign_utils.execute_cmd(cmd)

        cmd = '/usr/libexec/PlistBuddy -x -c "Print:Entitlements" %s > %s' % (temp_plist, self.entitle_plist)
        result = resign_utils.execute_cmd(cmd)

        resign_utils.copy(pp_path, self.app_temp_path)
        file_dir, file_name = os.path.split(pp_path)
        resign_utils.rename(os.path.join(self.app_temp_path, file_name), 'embedded.mobileprovision')
        os.remove(temp_plist)

    def code_sign(self,cert_name, file_path):
        cmd = 'codesign -f -s "%s" --entitlements %s "%s"' % (cert_name, self.entitle_plist, file_path)
        resign_utils.execute_cmd(cmd)

    def sign_start(self,cer_name):
        for file_name in self.zip_file_list:
            if resign_utils.is_need_sign(file_name):
                self.code_sign(cer_name, os.path.join(self.temp_file_dir, file_name))
        os.remove(self.entitle_plist)

if __name__ == '__main__':
    resign = Resign()
    ipa_path = '/Users/xx/Desktop/git/JoyUnity/joy_tools/scripts/resign/JoyDemo.ipa'
    resign.unzip_ipa(ipa_path)

    #itc后台下载 
    pp_path  = '/Users/baofengzhang/Downloads/match_AppStore_testjoygamescom.mobileprovision'
    #需要本机安装 相应证书
    cer_name = 'iPhone Distribution: li wei (5X27T35YBN)'

    resign.export_sign_info(pp_path)
    resign.sign_start(cer_name)
    resign.zip_ipa()


