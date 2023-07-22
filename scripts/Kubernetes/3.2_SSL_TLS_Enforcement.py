import os
import sys
import modules as m
import re

# Kubernetes
# 완료
# verbose 추가 필요
print("["+"#"*9+" "*12+"]")
vul=0; res=1; res_init=1
title="3.2. Controller Manager Configuration - SSL/TLS Enforcement"
m.init()

m.BAR()
m.CODE(title) #  SSL/TLS 적용
m.BAR()

kube_apiser = os.popen("cat /etc/kubernetes/manifests/kube-controller-manager.yaml 2>/dev/null").read()

print("Step1. SSL/TLS 적용을 통한 클라이언트 인증(포드)")
# --root-ca-file=##########.crt 인 경우 양호
if (kube_apiser.find("--root-ca-file")) != -1: # --root-ca-file 파라미터가 설정되어 있는 경우
    cut = re.compile("--root-ca-file=.+")
    check_list = cut.findall(kube_apiser)
    check = check_list[0].split('.') # --root-ca-file 파라미터를 . 기준으로 자름 (check[1] = 해당 파라미터에 설정된 파일의 확장자)
    if check[1] != "crt":
        res=0
else:
    res=0

ret=m.res_chk(res, vul, res_init, title, "\
Step1. SSL/TLS 적용을 통한 클라이언트 인증(포드)\n\
kube-controller-manager.yaml 파일 내 적절한 파라미터가 존재하지 않거나, 인자 값이 적절하게 설정되어 있지 않습니다.\n\
kube-controller-manager.yaml 파일 내 아래와 같이 설정해 주세요.\n\
    --root-ca-file=/etc/kubernetes/pki/ca.crt (default)")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. 인증서 관리(인증서 교환주기 설정)")
# --feature-gates=false 인 경우 양호
if (kube_apiser.find("--feature-gates")) != -1: # --feature-gates 파라미터가 설정되어 있는 경우
    cut = re.compile("--feature-gates=.+")
    check_list = cut.findall(kube_apiser)
    check = check_list[0].split('=') # --feature-gates 파라미터를 = 기준으로 자름 (check[1] = 해당 파라미터의 값)
    if check[1] != "true":
        res=0
else:
    res=0

ret=m.res_chk(res, vul, res_init, title, "\
Step2. 인증서 관리(인증서 교환주기 설정)\n\
kube-controller-manager.yaml 파일 내 적절한 파라미터가 존재하지 않거나, 인자 값이 적절하게 설정되어 있지 않습니다.\n\
kube-controller-manager.yaml 파일 내 아래와 같이 설정해 주세요.\n\
    --feature-gates=RotateKubeletServerCertificate=true 추가")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()
