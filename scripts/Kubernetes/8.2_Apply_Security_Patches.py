import os
import yaml
import modules as m

print("["+"#"*21+" "*0+"]")
vul=0; res=1; res_init=1
title="8.2 Etc - Apply Security Patches"
m.init()

m.BAR()
m.CODE(title) # 보안 패치 적용
m.BAR()

print("Step1. 최신 엔진 업데이트 설치 유무 확인")

system = os.popen("cat /etc/*release*").read()
if system.find('Ubuntu') != -1:
    newest_ver = os.popen("apt list | grep 'kubectl/kubernetes-xenial'").read().split()[1].split('-')[0]
elif system.find('centos') != -1:
    newest_ver = os.popen("yum list | grep 'kubectl/kubernetes-xenial'").read().split()[1].split('-')[0]
    
current_kuber_version = (yaml.safe_load(os.popen("sudo --user=$(echo $(pwd|awk -F '/' '{print $3}')) kubectl version --output=yaml").read()))

current_kuber_Client_version = current_kuber_version['clientVersion']['gitVersion'].split('v')[1]
current_kuber_Server_version = current_kuber_version['serverVersion']['gitVersion'].split('v')[1]

if current_kuber_Client_version != newest_ver or current_kuber_Server_version != newest_ver:
    res = 0

ret=m.res_chk(res, vul, res_init, title, "\
Step1. 최신 엔진 업데이트 설치 유무 확인\n\
kubernetes 최신 버전이 아닙니다.\n\
최신 버전으로 업그레이드해 주세요.\n\
    현재 클라이언트 버전: "+current_kuber_Client_version+" 최신 버전: "+newest_ver+"\n\
    현재 서버 버전: "+current_kuber_Server_version+" 최신 버전: "+newest_ver)
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()
