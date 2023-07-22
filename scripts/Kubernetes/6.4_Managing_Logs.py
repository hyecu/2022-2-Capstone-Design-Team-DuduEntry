import modules as m
import os

print("["+"#"*16+" "*5+"]")
vul=0; res=1; res_init=1
title="6.4 Kubelet Configuration - Managing Logs"
m.init()

m.BAR()
m.CODE(title)
m.BAR()

print("Step1. 이벤트 생성")

kubeletService='/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf'
N_kubeletService='/etc/systemd/system/kublet.service.d/10-kubeadm.conf'
kubeletConf='/var/lib/kubelet/config.yaml'

if os.popen('cat '+kubeletService+' 2>/dev/null').read(): #kublet service 파일이 있다면
    check=os.popen('cat '+kubeletService+' 2>/dev/null | grep -v "#" | grep KUBELET_SYSTEM_PODS_ARGS | grep "\-\-event-qps=0" |wc -l').read()
    if int(check)==0: #파일은 있는데 KUBELET_SYSTEM_PODS_ARGS 설정x
        res=0
        #kublet service 파일이 있는데 설정이 안돼있는거면 1-2검사
        if os.popen('cat '+kubeletConf+' 2>/dev/null | grep eventRecordQPS').read().find('5') == -1: #eventRecordQPS 적절하게 설정안돼있으면
            res=0
elif os.popen('cat '+N_kubeletService).read(): # (최신경로) kubelet service 파일이 있다면
    check=os.popen('cat '+N_kubeletService+' 2>/dev/null | grep -v "#" | grep KUBELET_SYSTEM_PODS_ARGS | grep "\-\-event-qps=0" |wc -l').read() #result: 0
    if int(check)==0: #파일은 있는데 KUBELET_SYSTEM_PODS_ARGS 설정x   #if check=='0'이 안먹어서 if int(check)==0으로 한것.
        res=0
        #kublet service 파일이 있는데 설정이 안돼있는거면 1-2검사
        if os.popen('cat '+kubeletConf+' 2>/dev/null | grep eventRecordQPS').read().find('5') == -1: #eventRecordQPS 적절하게 설정안돼있으면
            res=0
elif os.popen('cat '+kubeletConf+' 2>/dev/null | grep eventRecordQPS').read().find('5') == -1: #readOnlyPort 설정안돼있으면
    res=0

ret=m.res_chk(res, vul, res_init, title, "\
Step1. 이벤트 생성\n\
1-1) kubelet service 파일을 사용하는 경우:\n\
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf 혹은 /etc/systemd/system/kublet.service.d/10-kubeadm.conf 파일 내에 아래와 같이 설정해주세요.\n\
    KUBELET_SYSTEM_PODS_ARGS 내에 --event-qps=0\n\
1-2) kubelet config 파일을 사용하는 경우:\n\
/var/lib/kubelet/config.yaml 파일 내에 아래와 같이 설정해주세요.\n\
    eventRecordQPS: 0")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()


