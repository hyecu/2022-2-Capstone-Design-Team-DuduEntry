import os
import re
import yaml
import modules as m

print("["+"#"*14+" "*7+"]")
vul=0; res=1; res_init=1
title="6.2 Kubelet Configuration - Kubelet Authority control"
m.init()

m.BAR()
m.CODE(title)
m.BAR()

print("Step1. 권한 검증 수행")

kubeletService='/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf'
N_kubeletService='/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
kubeletConf='/var/lib/kubelet/config.yaml'

kubeletService_list=os.popen('cat '+kubeletService+' 2>/dev/null | grep -v "^#"').read()
N_kubeletService_list=os.popen('cat '+N_kubeletService+' 2>/dev/null | grep -v "^#"').read()
kubeletConf_list=os.popen('cat '+kubeletConf+' 2>/dev/null | grep -v "^#"').read()


if kubeletService_list.find("KUBELET_AUTHZ_ARGS") != -1:
    cut_ser = re.compile("KUBELET_AUTHZ_ARGS.+")
    check_list = cut_ser.findall(kubeletService_list)
    for check in check_list:
        if check.find("--authorization-mode=Webhook") != -1:
            res = 1
            break
        else:
            res = 0
elif N_kubeletService_list.find("KUBELET_AUTHZ_ARGS") != -1:
    cut_ser = re.compile("KUBELET_AUTHZ_ARGS.+")
    check_list = cut_ser.findall(N_kubeletService_list)
    for check in check_list:
        if check.find("--authorization-mode=Webhook") != -1:
            res = 1
            break
        else:
            res = 0
elif kubeletConf_list.find("authorization") != -1:
    excerpt=os.popen('sed -n "/^authorization:*/, ~1 p" '+kubeletConf+' 2>/dev/null | grep -v "^#"').read()
    config = yaml.safe_load(excerpt)
    if config['authorization']['mode'] != 'Webhook':
        res = 0
else:
    res = 0


ret=m.res_chk(res, vul, res_init, title, "\
Step1. 권한 검증 수행\n\
1-1) kubelet service 파일을 사용하는 경우:\n\
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf 혹은 /etc/systemd/system/kubelet.service.d/10-kubeadm.conf \
파일 내에 아래와 같이 설정해주세요.\n\
    KUBELET_AUTHZ_ARGS 내에 --authorization-mode=Webhook\n\
1-2) kubelet config 파일을 사용하는 경우:\n\
/var/lib/kubelet/config.yaml 파일 내에 아래 파라미터 존재 및 적절한 인자 값 설정 여부를 확인하세요.\n\
    authorization:\n\
    mode: Webhook")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()