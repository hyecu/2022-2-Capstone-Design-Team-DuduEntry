import os
import modules as m
import datetime as dt
from dateutil.parser import parse

print("[################    ]")
vul=0; res=1; res_init=1
m.init()

title = "4.2 Docker Swarm SSL/TLS apply"

m.BAR()
m.CODE(title)
m.BAR()

print("Step1. SSL/TLS 적용 여부 확인")
SSL_TLS_cks = os.popen("docker network ls --filter driver=overlay --quiet | xargs docker network inspect --format '{{.Name}} {{ .Options }}' 2>/dev/null").read()
if (SSL_TLS_cks.find('encrypted')) == -1:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. SSL/TLS 적용 여부 확인\n\
SSL/TLS가 적용되어 있지 않습니다.\n\
아래의 옵션을 사용해서 SSL/TLS를 적용해 주세요.\n\
    --opt encrypted")
res_init = ret[0]; vul = ret[1]

res = 1
print("Step2. 노드 인증서 교환주기 확인")
Node_Certificate_period = os.popen("docker info 2>/dev/null | grep 'Expiry Duration'").read()
if (Node_Certificate_period.find('days')) != -1:
    days = os.popen("docker info 2>/dev/null | grep 'Expiry Duration' | awk '{print $3}'").read()
    if int(days) >= 3:
        res = 0
else:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step2. 노드 인증서 교환주기 확인\n\
노드 인증서 교환 주기가 취약하게 설정되어 있습니다.\n\
아래 명령어를 사용해 노드 인증서 교환 주기를 재설정해 주세요.\n\
    docker swarm update --cert-expiry 48h")
res_init = ret[0]; vul = ret[1]

res = 1
print("Step3. CA인증서 교환주기 확인")
CA_Certificate_period = os.popen("ls -l /var/lib/docker/swarm/certificates/swarm-root-ca.crt | awk '{print $6, $7, $8}'").read()
pre = parse(CA_Certificate_period)
now = dt.datetime.now()

#print("now-dt.timedelta(hours=2): ", now-dt.timedelta(hours=2))
if now-dt.timedelta(hours=2) <= pre:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step3. CA인증서 교환주기 확인\n\
CA인증서의 만료 시간이 2시간도 남지 않았습니다.\n\
아래 명령어를 사용해 CA인증서를 변경해 주세요.\n\
    docker swarm ca --rotate")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()