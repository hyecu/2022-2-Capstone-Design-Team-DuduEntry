import os
import modules as m

print("["+"#"*18+" "*3+"]")
vul=0; res=1; res_init=1
title="7.1 Host os - Set Config File Permissions"
m.init()

m.BAR()
m.CODE(title)
m.BAR()

print("Step1. 설정 파일 권한 설정")

files = ['/etc/kubernetes/kubelet.conf', '/var/lib/kubelet/config.yaml']
kubeadm_files = ['/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf', '/etc/systemd/system/kubelet.service.d/10-kubeadm.conf']
authority = 'root:root'
other_perm = '644'
kubeadm_perm = '755'

for i in range(0,len(files)):
    check = m.perm_chk(files[i], other_perm)
    if check == 0:
        res = 0
    check = m.perm_chk(files[i], authority)
    if check == 0:
        res = 0

check=0
for i in range(0,len(kubeadm_files)):
    check = m.perm_chk(kubeadm_files[i], kubeadm_perm)
    check = m.perm_chk(kubeadm_files[i], authority)
if check == 0:
    res=0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. 설정 파일 권한 설정\n\
파일 소유 및 권한이 적절하게 설정되지 않았습니다.\n\
파일 위치별 권한은 아래와 같이 설정해 주세요.\n\
    "+"\n    ".join(files[i]+"는 "+other_perm for i in range(0,len(files)))+"\n\
    "+"\n    ".join(files[i]+"는 "+kubeadm_perm for i in range(0,len(kubeadm_files)))+"\n\
파일 위치별 소유권은 아래와 같이 설정해 주세요.\n\
    "+"\n    ".join(files[i]+"는 "+authority for i in range(0,len(files)))+"\n\
    "+"\n    ".join(files[i]+"는 "+kubeadm_perm for i in range(0,len(kubeadm_files))))
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()