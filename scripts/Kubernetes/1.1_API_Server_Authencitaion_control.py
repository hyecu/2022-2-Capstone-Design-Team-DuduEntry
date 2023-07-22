import os
import re
import sys
import yaml
import modules as m

print("["+"#"*1+" "*20+"]")
# Kubernetes
# 완료

vul=0; res=1; chk=1; res_init=1
title="1.1. API Server Configuration - API Server Authentication Control" # API Server 인증 제어
m.init()

m.BAR()
m.CODE(title)
m.BAR()

api_server = os.popen("cat /etc/kubernetes/manifests/kube-apiserver.yaml 2>/dev/null").read()
scheduler = os.popen("cat /etc/kubernetes/manifests/kube-scheduler.yaml 2>/dev/null").read()
control_m = os.popen("cat /etc/kubernetes/manifests/kube-controller-manager.yaml 2>/dev/null").read()

config = "$HOME/.kube/config"
ip_regex = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

# OAuth 나 Webhook 같은 연동 서비스를 지원, 이를 활용하여 외부 인증 관리 서비스 연동을 통해 사용자 계정 관리를 권고
# 사용자 인증을 위한 외부 서비스 사용: Webhook or OAuth 사용 검사, 둘 다 사용하지 않는 경우 check 출력하기

# webhook 검사 방법은 webhook 설정 방법을 참조하여 확인했습니다
# k8s 인증 완벽이해 #4 - Webhook 인증:    https://coffeewhale.com/kubernetes/authentication/webhook/2020/05/05/auth04/

# OAuth 검사 방법은 OAuth 설정 방법을 참조하여 확인했습니다
# kubectl-login:   https://github.com/clastix/kubectl-login

print("Step1. 사용자 계정 관리를 위한 시스템 연동")

reEx = re.compile("--authentication-token-webhook-config-file=(?:\/\w+)+(?:\/)?webhook.yaml") # <임의의경로>/webhook.yaml 파일로 설정되어 있는지 확인
webhook_apiserver = reEx.findall(api_server)
OAuth_config = os.popen("cat "+config+" 2>/dev/null | grep '^current-context: oidc'").read()

# Webhook 서비스 사용 여부 확인
if webhook_apiserver: # regex 검색 결과가 존재하는 경우: webhook.yaml 파일 검사
    webhook_yaml_in_apiserver = webhook_apiserver[0].split('=')[1].strip() # 파일 경로만 자르기
    webhook_yaml = os.popen("if [ -s "+webhook_yaml_in_apiserver+" ]; then echo 1; fi").read() # 시스템 내 해당 파일에 내용이 존재하는지 (쉘 스크립트 if문의 -s 옵션은 용량으로 확인합니다)
    if int(webhook_yaml) != 1: # 해당 파일의 내용이 존재하지 않는 경우: 취약
        res=0
# OAuth 서비스 사용 여부 확인 (Webhook 서비스를 사용하지 않는 경우)
elif not OAuth_config:
    res=0
# Webhook , OAuth 서비스 모두 사용하지 않는 경우
else:
    chk=0

ret = m.res_chk_with_chk(res, vul, chk, res_init, title, "\
Step1. 사용자 계정 관리를 위한 시스템 연동\n\
외부 인증 관리 서비스 연동을 통해 사용자 계정을 관리하는 것을 권고합니다.","\
\
Step1. 사용자 계정 관리를 위한 시스템 연동\n\
사용자 계정 인증을 위해 외부 독립 서비스를 사용해야 합니다.\n\
아래의 서비스를 이용해 사용자 계정 인증을 수행해주세요.\n\
    OAuth , Webhook , OpenID Connect 등")
res_init = ret[0]; vul = ret[1]


res=1
print("Step2. 비인증 접근 차단")
if api_server.find("--anonymous-auth=false") == -1: # 추가 (예외 가능)
    chk=0
if api_server.find("--insecure-allow-any-token=true") != -1: # 제거
    res=0
if re.search("--insecure-bind-address="+ip_regex, api_server) is not None: # 제거
    res=0
if api_server.find("--insecure-port=0") == -1: # 추가
    res=0
if api_server.find("--repair-malformed-updates=false") == -1: # 추가
    res=0
if api_server.find("--service-account-lookup=true") == -1: # 추가
    res=0

ret = m.res_chk_with_chk(res, vul, chk, res_init, title, "\
Step2. 비인증 접근 차단\n\
아래 설정에 대한 확인이 필요합니다.\n\
    --anonymous-auth=false\n\
    일반적인 정보 조회가 필요한 경우 검토 후 제외\n\
    ex) health check, CustomResourceDefinitions", "\
\
Step2. 비인증 접근 차단\n\
/etc/kubernetes/manifests/kube-apiserver.yaml 파일 내 아래 파라미터 존재 및 적절한 인자 값 설정 여부 확인:\n\
    --insecure-allow-any-token=true\n\
    --insecure-bind-address=X.X.X.X\n\
    --insecure-port=0\n\
    --repair-malformed-updates=false\n\
    --service-account-lookup-true")
res_init = ret[0]; vul = ret[1]

res=1
print("Step3. 취약한 방식의 인증 방식 사용")
if re.search("--basic-auth-file=/\w+(?:/\w+)*.*", api_server) is not None: # 제거
    res=0
if re.search("--token-auth-file=/\w+(?:/\w+)*.*", api_server) is not None: # 제거
    res=0

ret = m.res_chk(res, vul, res_init, title, "\
Step3. 취약한 방식의 인증 방식 사용\n\
/etc/kubernetes/manifests/kube-apiserver.yaml 파일 내 아래와 같이 설정:\n\
    --basic-auth-file=<filename> 존재할 경우 제거\n\
    --token-auth-file=<filename> 존재할 경우 제거")
res_init = ret[0]; vul = ret[1]


res=1
print("Step4. 서비스 API 외부 오픈 금지 1) Scheduler API 서비스")
if scheduler.find("--address=127.0.0.1") == -1: # 추가
    res=0

ret = m.res_chk(res, vul, res_init, title, "\
Step4. 서비스 API 외부 오픈 금지 1) Scheduler API 서비스\n\
/etc/kubernetes/manifests/kube-scheduler.yaml 파일 내 아래와 같이 설정:\n\
    --address=127.0.0.1")
res_init = ret[0]; vul = ret[1]


res=1
print("Step5. 서비스 API 외부 오픈 금지 2) Controller Manager API 서비스")
if control_m.find("--address=127.0.0.1") == -1: # 추가
    res=0

ret = m.res_chk(res, vul, res_init, title, "\
Step5. 서비스 API 외부 오픈 금지 2) Controller Manager API 서비스\n\
/etc/kubernetes/manifests/kube-controller-manager.yaml 파일 내 아래 파라미터 존재 및 적절한 인자 값 설정 여부 확인:\n\
    --address=127.0.0.1")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk_with_chk(vul, chk)
m.END()