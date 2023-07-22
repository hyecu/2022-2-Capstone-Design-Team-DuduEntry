import modules as m
import sys

print("["+"#"*11+" "*10+"]")

# 2022.11.20 경로 수정 완료, 주석 제거 완료

vul=0; res=1; chk=0; res_init=1  #기본값: 양호
title='5.2 Host OS - Etcd Data Directory Permissions Settings'
m.init()
m.BAR()
m.CODE(title)
m.BAR()

print("Step1. etcd 데이터 디렉터리 권한 설정")

permCheck = m.perm_chk('/var/lib/etcd', 700)
if permCheck == 0: #권한이 700이 아니면
    res=0  #취약
    ret = m.res_chk(res, vul, res_init, title, '\
Step1. etcd 데이터 디렉터리 권한 설정\n\
/var/lib/etcd 파일 권한이 700으로 설정되어 있지 않습니다.\n\
    /var/lib/etcd 권한을 700으로 변경한 후 소유자 및 그룹 권한을 확인해주세요.')
    res_init = ret[0]; vul = ret[1]
    
    
else: #권한이 700이면 소유자, 그룹권한 확인 (root가 아닌 소유자라 수동체크)
    chk=1
    m.check() # chk=1일경우
    sys.stdout = open('verbose', 'a') # 파일 열어줌
    if res_init == 1:
        m.BAR()
        print(title)
        m.BAR()
        res_init = 0
    print('Step1. etcd 데이터 디렉터리 권한 설정\n\
/var/lib/etcd 디렉터리의 소유자 및 그룹 권한을 확인해주세요.') # 메시지 출력
    sys.stdout = open('stdout.txt', 'a')

m.BAR()
if vul == 1:
    m.BAD("Result : Vulnerable")
elif chk == 1:
    m.INFO("Result : Please Check The Configurations")
m.END()