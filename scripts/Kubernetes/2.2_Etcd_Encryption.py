import os
import modules as m
import yaml
import re

print("["+"#"*7+" "*14+"]")
vul=0; res=1; res_init=1#기본값: 양호
title='2.2. Etcd Configuration - Etcd Encryption'
m.init()
m.BAR()
m.CODE(title)
m.BAR()

kube_apiser='/etc/kubernetes/manifests/kube-apiserver.yaml'
excerpt=os.popen('cat '+kube_apiser+'|grep -v "#"|egrep "\-\-experimental-encryption-provider-config=/.+"').read() #str형

print('Step1. etcd 암호화 적용')
if not excerpt: #결과 없으면
    res=0 #취약
    ret=m.res_chk(res, vul, res_init, title,'\
Step1. etcd 암호화 적용\n\
/etc/kubernetes/manifests/kube-apiserver.yaml 파일 내 해당 파라미터가 존재하지 않거나 적절한 인자 값 설정이 되어있지 않습니다.\n\
파라미터 추가 혹은 적절한 인자 값을 설정해 주세요.\n\
    --experimental-encryption-provider-config=</path/to/EncryptionConfig/File>')
    res_init=ret[0]; vul=ret[1]

if vul==0:
    m.ok()

res=1
print('Step2. 안전한 암호화 방식 사용')
if excerpt:
    file=excerpt.split('=')[1] #파일명 가져오기(str형)
    text=os.popen('cat '+file).read() #file내용
    current_config=yaml.safe_load(text) #/home/dudu/jye/a.yaml

    kind_chk=current_config['kind']
    if kind_chk!='EncryptionConfig':
        res=0

    provider_chk=current_config['resources'][0]['providers']
    if str(provider_chk).find('aescbc')==-1:
        res=0
else:
    res=0

if excerpt:
    encode_chk=current_config['resources'][0]['providers'][0]['aescbc']['secret']
    reExpress=re.compile('^[A-Za-z0-9+/]{43}=')
    excerpt=reExpress.findall(encode_chk)
    if not excerpt: #정규표현식이랑 일치하지 않으면
        res=0
else:
    res=0
ret=m.res_chk(res, vul, res_init, title,'\
Step2. 안전한 암호화 방식 사용\n\
/etc/kubernetes/manifests/kube-apiserver.yaml내 --experimental-encryption-provider-config에 설정된 경로의 암호화 설정 파일을 확인해주세요.\n\
(aescbc권고, secret 필드에 Encryption Key로 32byte base64인코딩 값 권고)\n\
    예시)\n\
    kind: EncryptionConfig\n\
    apiVersion: v1 resources:\n\
        - resources:\n\
            - secrets\n\
            providers:\n\
            - aescbc:\n\
                keys:\n\
                - name: key1\n\
                    secret: <32-byte base64-encoded secret>\n\
            - identity: {}')
res_init=ret[0]; vul=ret[1]

m.BAR()
m.vul_chk(vul)
m.END()



