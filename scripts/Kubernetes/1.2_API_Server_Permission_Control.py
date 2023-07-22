import os
import sys
import modules as m
import re

print("["+"#"*2+" "*19+"]")
vul=0; res=1; res_init=1
title="1.2. API Server Configuration - API Server Permission Control"
m.init()

m.BAR()
m.CODE(title) # API server 권한 제어
m.BAR()

print("Step1. Node 권한, 역할 기반 액세스 제어(RBAC) 사용")
kube_apiser = os.popen("cat /etc/kubernetes/manifests/kube-apiserver.yaml").read()
if kube_apiser.find("--authorization-mode=") == -1:
    res = 0
else:
    cut = re.compile("--authorization-mode.+")
    check_list = cut.findall(kube_apiser)
    check = re.split(r',|=', check_list[0])
    
    if len(check) != 3:
        res = 0
    else:
        safe_list = ['Node', 'RBAC']
        for safe in safe_list:
            if safe not in check[1:]:
                res=0
        
ret=m.res_chk(res, vul, res_init, title, "\
Step1. Node 권한, 역할 기반 액세스 제어(RBAC) 사용\n\
Node권한 및 역할 기반 액세스 제어(RBAC)를 사용하고 있지 않습니다.\n\
아래의 설정을 추가해 주세요.\n\
    --authorization-mode=Node\n\
    --authorization-mode=RBAC")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()