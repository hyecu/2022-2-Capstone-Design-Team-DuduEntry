import os
import modules as m
import re

print("["+"#"*8+" "*13+"]")
vul=0;res=1;res_init=1  #기본값: 양호
title='3.1. Controller Manager Configuration - Controller Authentication Control'
m.init()

m.BAR()
m.CODE(title)
m.BAR()


print('Step1. 각 컨트롤러에 대해 개별 서비스 계정 자격 증명')
file=os.popen('cat /etc/kubernetes/manifests/kube-controller-manager.yaml').read()

if (file.find('--use-service-account-credentials')) != -1:
    reExpress=re.compile('--use-service-account-credentials=\w+')
    excerpt=reExpress.findall(file) #['--use-service-account-credentials=true']
    value=excerpt[0].split('=')[1] 
    if value != 'true':
        res=0
else:
    res=0

ret = m.res_chk(res, vul, res_init, title, '\
Step1. 각 컨트롤러에 대해 개별 서비스 계정 자격 증명\n\
/etc/kubernetes/manifests/kube-controller-manager.yaml 파일 내 아래 파라미터가 존재하지 않거나 적절한 인자 값 설정이 되어있지 않습니다.\n\
파라미터 및 적절한 인자값을 설정해주세요.\n\
    --use-service-account-credentials=true')
res_init = ret[0]; vul = ret[1]

res=1
print('Step2. 컨트롤러 계정 자격증명에 사용되는 인증서 관리')
if (file.find('--service-account-private-key-file')) != -1:
    reExpress=re.compile('--service-account-private-key-file=/.+')
    excerpt=reExpress.findall(file) #['--service-account-private-key-file=/etc/kubernetes/pki/sa.key']
    value=excerpt[0].split('=')[1]
    if value != '/etc/kubernetes/pki/sa.key':
        res=0
else:
    res=0

ret = m.res_chk(res, vul, res_init, title, '\
Step2. 컨트롤러 계정 자격증명에 사용되는 인증서 관리\n\
/etc/kubernetes/manifests/kube-controller-manager.yaml 파일 내 \
아래 파라미터가 존재하지 않거나 적절한 값이 설정되어 있지 않습니다.\n\
파라미터 및 적절한 값을 설정해주세요.\n\
    --service-account-private-key-file=/etc/kubernetes/pki/sa.key')
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()