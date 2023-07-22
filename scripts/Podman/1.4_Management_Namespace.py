import os
import modules as m

print("[####            ]")
vul=0; res=1; res_init=1
m.init()

title = "1.4. Podman Configuration - Management Namespace"
m.BAR()
m.CODE(title) # Namespace 관리
m.BAR()

namespaces = ['network', 'process', 'ipc', 'uts', 'userns']
modes = ['NetworkMode', 'PidMode', 'IpcMode', 'UTSMode', 'UsernsMode']

# Step1 ~ Step5 반복문으로 진행
for i in range(0,5):
    print("Step"+str(i+1)+". 호스트 "+namespaces[i]+" namespace 공유 금지")
    checks = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}:"+modes[i]+"={{ .HostConfig."+modes[i]+" }}'").read().splitlines()
    res=1
    for check in checks:
        if 'host' in check:
            res=0
            break
    ret = m.res_chk(res, vul, res_init, title, "\
Step"+str(i+1)+". 호스트 "+namespaces[i]+"\namespace 공유 금지\n\
"+checks[i].split(':')[0]+"컨테이너에 "+modes[i]+namespaces[i]+"가 'host'로 설정되어 있습니다.\n\
컨테이너 실행 시 아래의 옵션을 사용하지 마십시오.\n\
    --"+namespaces[i]+"=host")
    res_init = ret[0]; vul = ret[1]

res=1
print("Step6. user namespace support 사용")
container_ID = os.popen("podman ps | awk '{print $1}'").read()
lines = len(container_ID.splitlines())
for i in range(1,lines):
    container_user = os.popen("ps -p $(podman inspect --format='{{ .State.Pid }}' "+container_ID.splitlines()[i]+") -o pid,user").read()
    if (container_user.splitlines()[1].split()[1].find('root')) != -1: #컨테이너 사용자 이름 확인
        res=0
        break

ret = m.res_chk(res, vul, res_init, title, "\
Step6. user namespace support 사용\n\
컨테이너 사용자의 이름이 root로 설정되어 있습니다.\n\
아래 명령어를 통해 컨테이너 사용자 이름을 변경해 주세요.\n\
    --userns-remap=default")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()