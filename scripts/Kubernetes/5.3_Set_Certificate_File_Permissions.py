import modules as m
import os

# 2022.11.20 경로 수정 완료, 주석 제거 완료
print("["+"#"*12+" "*9+"]")

vul=0; res=1; res_init=1
title="5.3 Host OS - Set Certificate File Permissions"
m.init()

m.BAR()
m.CODE(title)
m.BAR()

print('Step1. PKI 인증 디렉터리')
file='/etc/kubernetes/pki/'
authority='root:root'

check=m.perm_chk(file, authority)
if check==0: #권한 안맞으면 취약
    res=0
    ret=m.res_chk(res, vul, res_init, title, "\
Step1. PKI 인증 디렉터리\n\
/etc/kubernetes/pki 소유자 혹은 소유그룹이 root로 설정되어 있지 않습니다.\n\
아래 명령어를 실행하여 소유 그룹을 root로 변경해주세요.\n\
    chown root.root /etc/kubernetes/pki")
    res_init=ret[0]; vul=ret[1]

res=1
print('Step2. PKI 인증서 파일')
file='/etc/kubernetes/pki/*.crt'
permCheck=m.perm_chk(file,644)

if permCheck==0:
    res=0
    ret=m.res_chk(res, vul, res_init, title, "\
Step2. PKI 인증서 파일\n\
/etc/kubernetes/pki/*.crt 파일 권한이 644로 설정되어 있지 않습니다.\n\
아래 명령어를 실행하여 파일 권한을 644로 변경해주세요.\n\
    chmod 644 /etc/kubernetes/pki/*.crt")
    res_init=ret[0]; vul=ret[1]

res=1
print('Step3. PKI 키 파일')
file='/etc/kubernetes/pki/*.key'
permCheck=m.perm_chk(file,600)

if permCheck==0:
    res=0
    ret=m.res_chk(res, vul, res_init, title, "\
Step3. PKI 키 파일\n\
/etc/kubernetes/pki/*.key 파일 권한이 600으로 설정되어 있지 않습니다.\n\
아래 명령어를 사용하여 파일 권한을 600으로 설정해주세요.\n\
    chmod 600 /etc/kubernetes/pki/*.key")
    res_init=ret[0]; vul=ret[1]

m.BAR()
m.vul_chk(vul)
m.END()


