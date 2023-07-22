import os
import re
import modules as m

print("["+"#"*17+" "*4+"]")
vul=0; res=1; chk=1; res_init=1
title="6.5. Kubelet Configuration - Setting Kernel Parameter" # Kernel 파라미터 설정
m.init()

m.BAR()
m.CODE(title)
m.BAR()

kubeletService = '/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf'
N_kubeletService='/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
kubeletConf='/var/lib/kubelet/config.yaml'

kubeletService_list = os.popen("cat "+kubeletService+" 2>/dev/null | grep -v '^#' | grep -v '^$'").read() # kubeadm
N_kubeletService_list = os.popen("cat "+N_kubeletService+" 2>/dev/null | grep -v '^#' | grep -v '^$'").read() # 추가하기
kubeletConf_lsit = os.popen("cat "+kubeletConf+" 2>/dev/null | grep -v '^#' | grep -v '^$'").read() # config

print("Step1. default Kernel 파라미터 사용 금지")
kubeadm_regex = re.compile("KUBELET_SYSTEM_PODS_ARGS=.*--protect-kernel-defaults=true.*")
if re.search("KUBELET_SYSTEM_PODS_ARGS=.*--protect-kernel-defaults=true.*", kubeletService_list) is not None:
    next
elif re.search("KUBELET_SYSTEM_PODS_ARGS=.*--protect-kernel-defaults=true.*", N_kubeletService_list) is not None:
    next
elif kubeletConf_lsit.find("protectKernelDefaults: true") != -1:
    next
else:
    res=0

ret=m.res_chk(res, vul, res_init, title, '\
Step1. default Kernel 파라미터 사용 금지\n\
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf 혹은 /etc/systemd/system/kublet.service.d/10-kubeadm.conf 파일 내 아래와 같이 설정:\n\
    "KUBELET_SYSTEM_PODS_ARGS=--protect-kernel-defaults=true"\n\
혹은 /var/lib/kubelet/config.yaml 파일 내 아래와 같이 설정:\n\
    protectKernelDefaults: true')
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.BAR()