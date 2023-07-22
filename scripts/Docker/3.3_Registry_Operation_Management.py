import os
import modules as m

print("[##############      ]")
vul=0; res=1; res_init=1

m.init()

title="3.3. Images - Registry Operation Management"
m.BAR()
m.CODE(title) # 레지스트리 운영 관리
m.BAR()

print("Step1. 원격 레지스트리와 주고받는 데이터에 Content trust 적용")
content_trust = os.popen("echo $DOCKER_CONTENT_TRUST").read()
if content_trust.find('1') == -1:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. 원격 레지스트리와 주고받는 데이터에 Content trust 적용\n\
Content trust가 활성화 되어있지않습니다.\n\
아래의 명령어를 사용해서 활성화해주세요.\n\
    export DOCKER_CONTENT_TRUST=1")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. 레지스트리와 암호화되지 않은 연결 금지")
registry_encryption = os.popen("ps -ef | grep dockerd").read()
if (registry_encryption.find("--insecure-registry")) != -1:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step2. 레지스트리와 암호화되지 않은 연결 금지 \n\
인증 정보가 없어도 접근이 가능하도록 설정되어 있습니다. \n\
아래의 옵션을 삭제해 주세요. \n\
    --insecure-registry")
res_init = ret[0]; vul = ret[1]

res = 1
print("Step3. 구 버전(v1) legacy registry 사용 금지")
version_check = os.popen("docker version --format '{{.Server.Version}}'").read()
ver_num = (version_check).split('.')
v17_12 = ("17.12").split('.')

for i in range(len(ver_num)):
    if int(ver_num[i]) > int(v17_12[i]):
        break
    else:
        check_old_ver = os.popen("ps -ef | grep docker").read()
        if (check_old_ver.find("--disable-legacy-registry")) == -1:
            res = 0
            break
        else:
            break

ret = m.res_chk(res, vul, res_init, title, "\
Step3. 구 버전(v1) legacy registry 사용 금지\n\
구 버전 레지스트리가 활성화되어 있습니다.\n\
아래의 명령어를 사용하여 비 활성화해 주세요.\n\
    dockerd --disable-legacy-registry")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()
