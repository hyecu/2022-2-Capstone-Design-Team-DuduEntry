import os
import modules as m

print("[##                  ]")
vul=0; res=1; res_init=1
m.init()

title = "1.2. Docker Configuration - Authentication Privilege Control"

m.BAR()
m.CODE(title) # 인증 권한 제어
m.BAR()

print("Step1. docker group 내 사용자 확인")

docker_group_user = os.popen("getent group docker | awk -F ':' '{print $1}'").read()
Authenticated_user = open('Authenticated_user_1.2.txt', 'r')

if docker_group_user not in Authenticated_user:
    res = 0

ret = m.res_chk(res, vul, res_init, title,"\
Step1. docker group 내 사용자 확인\n\
docker group에 신뢰하지 않는 사용자가 있습니다.\n\
신뢰하지 않는 사용자를 삭제해 주세요")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. authorization plugin을 사용한 권한 제어")
authorization_plugin = os.popen("docker plugin ls").read()
if (authorization_plugin.find("authorization plugin")) == -1:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step2. authorization plugin을 사용한 권한 제어\n\
authorization plugin이 설치되어 있지 않습니다.\n\
authorization plugin을 설치해 주세요.")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()