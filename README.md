
## 目录结构

--output 
	输出目录

--resign.py

	修改ipa_path，pp_path（描述文件路径），cer_name（证书名称）

	执行python resign.py 


重签名流程，跟安卓的类似

1.解压ipa

2.导出entitlements_temp.plist

3.重签名

4.压缩ipa


security api

https://ss64.com/osx/security.html