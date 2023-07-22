import os
import modules as m
import re

print("["+"#"*6+" "*15+"]")
vul=0; res=1; res_init=1  #기본값: 양호
title='2.1. etcd Configuration - Apply SSL/TLS'
m.init()

m.BAR()
m.CODE(title)
m.BAR()

etcd=os.popen('cat /etc/kubernetes/manifests/etcd.yaml').read()
kube_apiser=os.popen("cat /etc/kubernetes/manifests/kube-apiserver.yaml").read()

print('Step1. SSL/TLS 적용을 통한 클라이언트 인증(etcd peer 및 클라이언트)')

etcd_check=['--client-cert-auth','--peer-client-cert-auth']
for i in etcd_check:
    if re.search(i+'=\w+',etcd) is not None: #파라미터=인자 가 있다면?
        value=re.search(i+'=\w+',etcd)[0].split('=')[1]  #각 피라미터의 인자값만 출력
        #print(value)
        if value != 'true':
            res=0
    else:
        res=0  #파라미터가 존재 및 적절한 값이 없다면

ret = m.res_chk(res, vul, res_init, title, '\
Step1. SSL/TLS 적용을 통한 클라이언트 인증(etcd peer 및 클라이언트)\n\
/etc/kubernetes/manifests/etcd.yaml 파일 내 해당 파라미터가 존재하지 않거나 적절한 인자 값 설정이 되어있지 않습니다.\n\
파라미터 추가 혹은 적절한 인자 값을 설정해 주세요.\n\
    --client-cert-auth=true, --peer-client-cert-auth=true')
res_init = ret[0]; vul = ret[1]

res=1
print('Step2. 인증서 설정(etcd peer 및 클라이언트) 1) etcd.yaml')
etcd_check=['--cert-file','--key-file','--peer-cert-file','--peer-key-file']
file_form_check=['crt','key','crt','key']

for i in range(0,4):
    if re.search(etcd_check[i]+'.+',etcd) is None: #파라미터=인자가 없다면? 취약
        res=0
    else: #파라미터=인자 존재. 적절한 값인지 확인 (/파일이름.확장자 형태인지 확인)
        file=re.search(etcd_check[i]+'.+',etcd)[0].split('=')[1] #str형으로 파일경로만 뜸
        reExpress=re.compile('/.+.'+file_form_check[i])
        excerpt=reExpress.findall(file) #리스트형태로 /파일명.확장자 부분만 하나씩 가져오기
        if not excerpt: #해당하는 부분이 없으면 취약
            res=0

ret = m.res_chk(res, vul, res_init, title, '\
Step2. 인증서 설정(etcd peer 및 클라이언트) 1)etcd.yaml\n\
/etc/kubernetes/manifests/etcd.yaml 파일 내 해당 파라미터가 존재하지 않거나 적절한 인자 값 설정이 되어있지 않습니다.\n\
파라미터 추가 혹은 적절한 인자 값을 설정해 주세요.\n\
    --cert-file=<인증서 파일>, --key-file=<키 파일>, --peer-cert-file=<peer 인증서 파일>, --peer-key-file=<peer 키 파일>')
res_init = ret[0]; vul = ret[1]

res=1
print('Step2. 인증서 설정(etcd peer 및 클라이언트) 2) kube_apiserver.yaml')

apiSer_check=['--etcd-certfile','--etcd-keyfile','--etcd-cafile']
file_form_check=['crt','key','crt']

for i in range(0,3):
    if re.search(apiSer_check[i]+'.+',kube_apiser) is None: #파라미터=인자가 없다면? 취약
        res=0
    else: #파라미터=인자 존재. 적절한 값인지 확인 (/파일이름.확장자 형태인지 확인)
        file=re.search(apiSer_check[i]+'.+',kube_apiser)[0].split('=')[1] #str형으로 파일경로만 뜸
        reExpress=re.compile('/.+.'+file_form_check[i])
        excerpt=reExpress.findall(file) #리스트형태로 /파일명.확장자 부분만 하나씩 가져오기
        if not excerpt: #해당하는 부분이 없으면 취약
            res=0

ret = m.res_chk(res, vul, res_init, title, '\
Step2. 인증서 설정(etcd peer 및 클라이언트) 2)kube-apiserver.yaml\n\
/etc/kubernetes/manifests/kube-apiserver.yaml 파일 내 해당 파라미터가 존재하지 않거나 적절한 인자 값 설정이 되어있지 않습니다.\n\
파라미터 추가 혹은 적절한 인자 값을 설정해 주세요.\n\
    --etcd-certfile=<etcd cert인증서 파일>, --etcd-keyfile=<etcd 키 파일>, --etcd-cafile=<etcd ca인증서 파일>')
res_init = ret[0]; vul = ret[1]

res=1
print('Step3. 인증서 관리(자체서명인증서 사용금지)')

#a=re.search('--auto-tls=.+',etcd) #값이 None이 뜰수도 있구나...
if etcd.find('--auto-tls=false') == -1:  #없으면
    res=0

if etcd.find('--peer-auto-tls=true') != -1: #있으면
    res=0

if re.search('--trusted-ca-file.+', etcd) is None: #파라미터=인자가 없다면? 취약
    res=0
else: #파라미터=인자가 있다면?
    file=re.search('--trusted-ca-file.+', etcd)[0].split('=')[1]
    reExpress=re.compile('/.+.crt') #/이름.crt
    excerpt=reExpress.findall(file)
    if not excerpt: #해당하는 부분이 없으면 취약
        res=0
    
ret = m.res_chk(res, vul, res_init, title, '\
Step3. 인증서 관리(자체서명인증서 사용금지)\n\
/etc/kubernetes/manifests/etcd.yaml 파일 내 해당 파라미터가 존재하지 않거나 적절한 인자 값 설정이 되어있지 않습니다.\n\
파라미터 추가 혹은 적절한 인자 값을 설정해 주세요.\n\
    --auto-tls=false, --peer-auto-tls=false or 제거, --trusted-ca-file=<인증서 파일>')
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()