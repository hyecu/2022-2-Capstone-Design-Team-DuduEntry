import os
import modules as m

print("["+"#"*10+" "*11+"]")
vul=0; res=1; chk=1; res_init=1 #기본값: 양호
title='5.1 Host OS - Setting File Permission Setting'
m.init()

m.BAR()
m.CODE(title)
m.BAR()

files = ['/etc/kubernetes/manifests/kube-apiserver.yaml', '/etc/kubernetes/manifests/kube-controller-manager.yaml', '/etc/kubernetes/manifests/kube-scheduler.yaml', '/etc/kubernetes/manifests/etcd.yaml', '/etc/kubernetes/admin.conf', '/etc/kubernetes/scheduler.conf', '/etc/kubernetes/controller-manager.conf']
net_inter = os.popen("find /etc/cni/net.d -type f").read().splitlines()
files = files + net_inter


perm = '644'
authority = 'root:root'

print("step1. 설정 파일 권한 설정")

for i in range(0,len(files)):
    check = m.perm_chk(files[i], perm)
    if check == 0:
        res = 0
    check = m.perm_chk(files[i], authority)
    if check == 0:
        res = 0

# for l in range(0,len(files)):
#     check = m.perm_chk(files[l], authority)
#     if check == 0:
#         res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. 설정 파일 권한 설정\n\
파일 소유 및 권한이 적절하게 설정되지 않았습니다.\n\
파일 위치별 권한은 아래와 같이 설정해 주세요.\n\
    "+"\n    ".join(i+"는 "+perm for i in files)+"\n\
파일 위치별 소유권은 아래와 같이 설정해 주세요.\n\
    "+"\n    ".join(i+"는 "+authority for i in files))
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()