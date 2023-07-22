import os
import sys
import modules as m
import re

print("["+"#"*5+" "*16+"]")
vul=0; res=1; chk=0; res_init=1  #기본값: 양호
title='1.5. API Server Configuration - Log Management'

m.init()
m.BAR()
m.CODE(title)
m.BAR()

kube_apiser = os.popen('cat /etc/kubernetes/manifests/kube-apiserver.yaml').read()

print("Step1. 로그 디렉터리 및 파일 설정")

# --audit-log-path=<filename>이 있는지 없는지 확인하는 명령어
if re.search("--audit-log-path=(\/|\w)\w+", kube_apiser) is None: # \/ : 절대경로 방식    \w : 문자가 오는지 안 오는지 확인   + : 하나 이상의 문자가 오는지 안 오는지 확인 바로앞에 있는 \가 1개 이상은 있어야 함. is None : 없으면 양호하지 않음
    res=0  # 파일의 설정이 적합하지 않으면 양호하지 않음.

# backupsize 확인하는 명령어
if (kube_apiser.find('--audit-log-maxbackup')) != -1:
    maxbackup=re.compile('--audit-log-maxbackup=\d+').findall(kube_apiser)[0].split('=')[1] # backupsize의 값을 정수로 받기 때문에 d 사용함. 0을 기준으로 자름]-
   
    if int(maxbackup) != 10: # backsize가 10 이외의 값을 지니게 되면 항목 구성을 재점검 해야함
        chk=1 # chk가 1이면 구성을 다시 확인해야함

# maxsize가 적절한지 아닌지 확인하는 명령어
if (kube_apiser.find('--audit-log-maxsize=\d+')) != -1:
    maxsize=re.compile('--audit-log-maxsize=\d+').findall(kube_apiser)[0].split('=')[1]
    if int(maxsize) != 100: # maxsize가 100 이외의 값을 지니게 되면 항목 구성을 재점검 해야함
        chk=1

if res == 0:
    m.fail() # res=0일경우 fail이 뜸
    sys.stdout = open('verbose', 'a') # 파일 열어줌
    print("\
Step1. 로그 디렉터리 및 파일 설정\n\
--audit-log-path의 파라미터 값이 적절하지 않습니다.\n\
적절한 인자값을 아래와 같이 설정해 주세요.\n\
    --audit-log-path=<filename>") # 오류메시지 출력
    sys.stdout = open('stdout.txt', 'a') # 파일 열어줌

elif chk == 1:
    m.check() # chk=1일경우 
    sys.stdout = open('verbose', 'a') # 파일 열어줌
    print("\
Step1. 로그 디렉터리 및 파일 설정\n\
maxbackup과 maxsize의 값을 확인해야 합니다.\n\
아래의 설정값 혹은 적절한 인자값을 확인해주세요.\n\
    --audit-log-maxbackup=10 or 적절한 사이즈 추가\n\
    --audit-log-maxsize=100 or 적절한 사이즈 추가") # 오류메시지 출력
    sys.stdout = open('stdout.txt', 'a') # 파일 열어줌
else:
    m.ok() # 위의 경우가 아니고, 만족할 경우에는 ok를 출력함


res=1 # 여기에 res=1을 넣는 이유는 앞에가 res=0의 값을 지니게 된다면 뒤에도 res의 값은 0이 되므로 1로 변경을 해준다.
print("Step2. 로그 저장 주기")
if (re.search("--audit-log-maxage=\d+", kube_apiser)) is not None: # 값이 존재하면
    maxage=re.compile('--audit-log-maxage=\d+').findall(kube_apiser)[0].split('=')[1] # --audit-log-maxage 파라미터의 = 이후 값을 추출해서 maxage 변수에 저장
    if (int(maxage) < 30):# maxage의 값이 30보다 작을 경우에는 취약하고 30보다 클 경우에는 양호함
        res=0 # maxage가 30보다 작으면 취약함
else:
    res=1 # maxage가 30보다 클 경우이므로 양호하다고 판단함


# 오류메시지 출력
ret=m.res_chk(res, vul, res_init, title, '\
Step2. 로그 저장 주기\n\
/etc/kubernetes/manifests/kube-apiserver.yaml 파일 내 아래 파라미터가 존재하지 않거나 적절한 인자 값이 설정이 되어있지 않습니다.\n\
--audit-log-maxage의 파라미터 및 적절한 인자값을 아래와 같이 설정해 주세요.\n\
    --audit-log-maxage=30 or 적절한 기간 추가')
res_init = ret[0]; vul = ret[1]

res=1
print("Step3. AdvancedAuditing 설정")
if re.search("--audit-policy-file=(\/|\w)\w+", kube_apiser) is None:
    res=0

# 오류메시지 출력
ret=m.res_chk(res, vul, res_init, title, '\
Step3. AdvancedAuditing 설정\n\
/etc/kubernetes/manifests/kube-apiserver.yaml 파일 내 아래 파라미터가 존재하지 않거나 적절한 인자 값이 설정이 되어있지 않습니다.\n\
파라미터 및 적절한 인자값을 설정해 주세요.\n\
    -audit-policy-file')
res_init = ret[0]; vul = ret[1]

# 값의 설정에서 문제가 있을 경우에 아래의 메시지를 띄워줌
m.BAR()
if vul == 1:
    m.BAD("Result : Vulnerable")
elif chk == 1:
    m.INFO("Result : Please Check The Configurations")
else:
    m.OK("Result : Good")
m.END()