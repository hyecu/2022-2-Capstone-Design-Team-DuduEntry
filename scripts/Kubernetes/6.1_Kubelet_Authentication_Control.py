import os
import modules as m

print("["+"#"*13+" "*8+"]")
vul=0; res=1; res_init=1
title="6.1 Kubelet Configuration - Kubelet Authentication Control"
m.init()

m.BAR()
m.CODE(title)
m.BAR()

print("Step1. 비인증 접근 차단")
kubeletService='/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf'
N_kubeletService='/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
kubeletConf='/var/lib/kubelet/config.yaml'

if os.popen('cat '+kubeletService).read(): #kublet service 파일이 있다면
    check=os.popen('cat '+kubeletService+' 2>/dev/null | grep -v "#" | grep KUBELET_SYSTEM_PODS_ARGS | grep "\-\-anonymous-auth=false"\
    | grep "\-\-read-only-port=0" |wc -l').read()
    if int(check)==0: #파일은 있는데 KUBELET_SYSTEM_PODS_ARGS 설정x
        res=0
    else: #파일은 있고 KUBELET_SYSTEM_PODS_ARGS 설정o
        check=os.popen('cat '+kubeletService+' 2>/dev/null | grep -v "#" | grep KUBELET_CADVISOR_ARGS | grep "\-\-cadvisor-port=0" | wc -l').read()
        if int(check)==0: #KUBELET_SYSTEM_PODS_ARGS 설정 o, KUBELET_CADVISOR_ARGS 설정x
            res=0

    if res==0:  #kublet service 파일이 있는데 설정이 안돼있는거면 1-2검사
        if os.popen('cat '+kubeletConf).read():
            excerpt=os.popen('sed -n "/^authentication:*/, ~4 p" '+kubeletConf).read() #그냥 authentication 포함 3줄만 뽑아버림

            if excerpt.find('authentication:')==-1: #find가 -만 아니면 값이 있는건가봄. authentication: 없으면 취약
                res=0
            elif excerpt.find('anonymous:')==-1: #anonymous: 없으면 취약
                res=0
            elif os.popen('sed -n "/^authentication:*/, ~4 p" '+kubeletConf+' | grep enabled:').read().find('false')==-1: #enalbed:에 false 없으면 취약
                res=0
            elif os.popen('cat '+kubeletConf+' | grep readOnlyPort').read().find('0') == -1: #readOnlyPort 설정안돼있으면
                res=0

elif os.popen('cat '+N_kubeletService).read(): # (최신경로) kubelet service 파일이 있다면
    check=os.popen('cat '+N_kubeletService+' 2>/dev/null | grep -v "#" | grep KUBELET_SYSTEM_PODS_ARGS | grep "\-\-anonymous-auth=false"\
    | grep "\-\-read-only-port=0" |wc -l').read()
    if int(check)==0: #파일은 있는데 KUBELET_SYSTEM_PODS_ARGS 설정x
        res=0
    else: #파일은 있고 KUBELET_SYSTEM_PODS_ARGS 설정o
        check=os.popen('cat '+N_kubeletService+' 2>/dev/null | grep -v "#" | grep KUBELET_CADVISOR_ARGS | grep "\-\-cadvisor-port=0" | wc -l').read()
        if (check)==0: #KUBELET_SYSTEM_PODS_ARGS 설정 o, KUBELET_CADVISOR_ARGS 설정x
            res=0

    if res==0: #kublet service 파일이 있는데 설정이 안돼있는거면 1-2검사
        if os.popen('cat '+kubeletConf).read():
            excerpt=os.popen('sed -n "/^authentication:*/, ~4 p" '+kubeletConf+' 2>/dev/null').read() #그냥 authentication 포함 3줄만 뽑아버림

            if excerpt.find('authentication:')==-1: #find가 -만 아니면 값이 있는건가봄. authentication: 없으면 취약
                res=0
            elif excerpt.find('anonymous:')==-1: #anonymous: 없으면 취약
                res=0
            elif os.popen('sed -n "/^authentication:*/, ~4 p" '+kubeletConf+' 2>/dev/null| grep enabled:').read().find('false')==-1: #enalbed:에 false 없으면 취약
                res=0
            elif os.popen('cat '+kubeletConf+' | grep readOnlyPort').read().find('0') == -1: #readOnlyPort 설정안돼있으면
                res=0

elif os.popen('cat '+kubeletConf).read(): #1.2검사
    excerpt=os.popen('sed -n "/^authentication:*/, ~4 p" '+kubeletConf+' 2>/dev/null').read() #그냥 authentication 포함 3줄만 뽑아버림

    if excerpt.find('authentication:')==-1: #find가 -만 아니면 값이 있는건가봄. authentication: 없으면 취약
        res=0
    elif excerpt.find('anonymous:')==-1: #anonymous: 없으면 취약
        res=0
    elif os.popen('sed -n "/^authentication:*/, ~4 p" '+kubeletConf+' 2>/dev/null | grep enabled:').read().find('false')==-1: #enalbed:에 false 없으면 취약
        res=0
    elif os.popen('cat '+kubeletConf+' 2>/dev/null | grep readOnlyPort').read().find('0') == -1: #readOnlyPort 설정안돼있으면
        res=0

ret=m.res_chk(res, vul, res_init, title, "\
Step1. 비인증 접근 차단\n\
1-1) kubelet service 파일을 사용하는 경우:\n\
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf 혹은 /etc/systemd/system/kubelet.service.d/10-kubeadm.conf \
파일 내에 아래와 같이 설정해주세요.\n\
    KUBELET_SYSTEM_PODS_ARGS 내에 --anonymous-auth=false --read-only-port=0\n\
    KUBELET_CADVISOR_ARGS 내에 --cadvisor-port=0\n\
1-2) kubelet config 파일을 사용하는 경우:\n\
/var/lib/kubelet/config.yaml 파일 내에 아래 파라미터 존재 및 적절한 인자 값 설정 여부를 확인해주세요.\n\
    authentication:\n\
    anonymous:\n\
    enabled: false\n\
    readOnlyPort: 0")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()
       

    
