import os
import re
import modules as m

print("[################]")
vul=0; res=1; res_init=1
# check_list = ['upgraded', 'newly installed']

m.init()

title = "5.3. Etc - Apply security patches"
m.BAR()
m.CODE(title) # 보안 패치 적용
m.BAR()

print("Step1. 최신 엔진 업데이트 설치 여부 확인")

system = os.popen("cat /etc/*release*").read()
# print("system: ", system)
if system.find('Ubuntu') != -1:
    newest_ver = os.popen("apt list 2>/dev/null | grep -i 'podman-rootless/unknown.*amd64'").read().split()[1].split(':')[1].split('-')[0]
elif system.find('centos') != -1:
    newest_ver = os.popen("yum list | grep podman.x86_64'").read().split()[1].split('-')[0]
current_podman_version = os.popen("podman --version").read().split()[2]

print("newest_ver: ", newest_ver)
print("current_podman_version: ", current_podman_version)

if current_podman_version != newest_ver:
    res=0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. 최신 엔진 업데이트 설치 여부 확인\n\
Podman 최신 버전이 아닙니다.\n\
최신 버전으로 업그레이드해 주세요.\n\
    현재버전: "+current_podman_version+" 최신버전: "+newest_ver)
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()