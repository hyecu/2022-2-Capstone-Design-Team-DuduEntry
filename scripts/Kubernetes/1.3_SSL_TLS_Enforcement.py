import os
import sys
import modules as m
import re

# Kubernetes
# verbose 추가 필요
print("["+"#"*3+" "*18+"]")
vul=0; res=1; res_init=1
title="1.3. API Server Configuration - SSL/TLS Enforcement"
sys.stdout = open('stdout.txt', 'a')

m.BAR()
m.CODE(title) #  SSL/TLS 적용
m.BAR()

kube_apiser = os.popen("cat /etc/kubernetes/manifests/kube-apiserver.yaml").read()

print("Step1. SSL/TLS 적용을 통한 네트워크 구간 데이터 보호 1) kubelet https 설정")
# --kubelet-https 파라미터 설정을 하지 않거나 값이 false 로 설정되어 있어야 양호
if (kube_apiser.find("--kubelet-https")) != -1:
    cut = re.compile("--kubelet-https=\w+")
    check_list = cut.findall(kube_apiser)
    check = check_list[0].split('=')
    if check[1] != "true":
        res=0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. SSL/TLS 적용을 통한 네트워크 구간 데이터 보호 1) kubelet https 설정\n\
--kubelet-https 파라미터가 적절하게 설정되어 있지 않습니다.\n\
    --kubelet-https를 제거해 주거나, 파라미터값을 true로 바꿔주세요.")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. SSL/TLS 적용을 통한 네트워크 구간 데이터 보호 2) secure port 설정")
# --secure-port 파라미터 설정을 하지 않거나 값이 1~65535 사이로 설정되어 있어야 양호
if (kube_apiser.find("--secure-port")) != -1:
    cut = re.compile("--secure-port=\d+")
    check_list = cut.findall(kube_apiser)
    check = check_list[0].split('=')
    if int(check[1]) < 1 or int(check[1]) > 65535:
        res=0
        
    # if int(check[1]) != 0 and (int(check[1]) > 0 or int(check[1]) < 65535):
ret = m.res_chk(res, vul, res_init, title, "\
Step2. SSL/TLS 적용을 통한 네트워크 구간 데이터 보호 2) secure port 설정\n\
--secure-port 파라미터가 적절하게 설정되어 있지 않습니다.\n\
    --secure-port를 제거해 주거나, 0이 아닌 값으로 설정해 주세요.(default 6443)")
res_init = ret[0]; vul = ret[1]

res=1
print("Step3. 인증서 관리(apiserver to kubelet)")
certificate_check = ['--kubelet-certificate-authority', '--kubelet-client-certificate', '--kubelet-client-key', '--service-account-key-file']
file_form_check = ['crt', 'crt', 'key', 'pub']

for i in range(0,4):
    cut = re.compile(certificate_check[i] + ".+")
    check_list = cut.findall(kube_apiser)
    if not check_list:  # certificate_check 에 해당하는 파라미터의 값이 설정되어 있지 않은 경우
        res = 0
        break
    else:
        file_form = check_list[0].split('.') # certificate_check 에 해당하는 파라미터의 값이 설정 됨 + '.' 기준으로 잘라서 확장자를 file_form 변수에 저장
        if file_form[1] != file_form_check[i]: # 설정된 확장자가 file_form_check 와 일치하지 않는 경우
            res = 0
            break

ret = m.res_chk(res, vul, res_init, title, "\
Step3. 인증서 관리(apiserver to kubelet)\n\
kube-apiserver.yaml 파일 내 적절한 파라미터가 존재하지 않거나, 인자 값이 적절하게 설정되어 있지 않습니다.\n\
kube-apiserver.yaml 파일 내 아래와 같이 설정해 주세요.\n\
    --kubelet-certificate-authority=<인증서 파일> 추가\n\
    --kubelet-client-certificate=<client 인증서 파일> 추가\n\
    --kubelet-client-key=<client 키 파일> 추가\n\
    --service-account-key-file=<service account 키 파일> 추가")
res_init = ret[0]; vul = ret[1]

res=1
print("Step4. 인증서 관리(apiserver)")
certificate_check = ['--tls-cert-file', '--tls-private-key-file', '--client-ca-file']
file_form_check = ['crt', 'key', 'crt']

for i in range(0,3):
    cut = re.compile(certificate_check[i] + ".+")
    check_list = cut.findall(kube_apiser)
    if not check_list: # certificate_check 에 해당하는 파라미터의 값이 설정되어 있지 않은 경우
        res = 0
        break
    else:
        file_form = check_list[0].split('.') # certificate_check 에 해당하는 파라미터의 값이 설정 됨 + '.' 기준으로 잘라서 확장자를 file_form 변수에 저장
        if file_form[1] != file_form_check[i]: # 설정된 확장자가 file_form_check 와 일치하지 않는 경우
            res = 0
            break

ret = m.res_chk(res, vul, res_init, title, "\
Step4. 인증서 관리(apiserver)\n\
kube-apiserver.yaml 파일 내 적절한 파라미터가 존재하지 않거나, 인자 값이 적절하게 설정되어 있지 않습니다.\n\
kube-apiserver.yaml 파일 내 아래와 같이 설정해 주세요.\n\
    --tls-cert-file=<tls 인증서 파일> 추가\n\
    --tls-private-key-file=<tls 키 파일> 추가\n\
    --client-ca-file=<client ca 인증서 파일> 추가")
res_init = ret[0]; vul = ret[1]

res=1
print("Step5.안전한 SSL/TLS 버전 사용")
ver_set = "--tls-ciphersuites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256"
# 이 값이 kube-apiserver.yaml 파일 내에 존재해야 양호

if kube_apiser.find(ver_set) == -1:
    res=0

ret = m.res_chk(res, vul, res_init, title, "\
Step5.안전한 SSL/TLS 버전 사용\n\
kube-apiserver.yaml 파일 내 적절한 파라미터가 존재하지 않거나, 인자 값이 적절하게 설정되어 있지 않습니다.\n\
kube-apiserver.yaml 파일 내 아래와 같이 설정해 주세요.\n\
    --tls-ciphersuites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()