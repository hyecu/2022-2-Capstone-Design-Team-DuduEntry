import os
import modules as m

print("[###############     ]")
vul=0; res=1; res_init=1
m.init()

title="4.1 Docker Swarm Access Control"

m.BAR()
m.CODE(title)
m.BAR()

print("Step1. swarm mode 동작 여부 확인")
swarm_mode = os.popen("docker info 2>/devnull | grep Swarm | awk '{print $2}'").read()
if (swarm_mode.find('inactive')) == -1:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. swarm mode 동작 여부 확인\n\
불필요한 swarm mode가 활성화되어 있습니다.\n\
아래의 명령어를 사용해서 비활성화해 주세요.\n\
    docker swarm leave")
res_init = ret[0]; vul = ret[1]

res = 1
print("Step2. 관리자 노드 최소화")
manager_node = os.popen("docker info --format '{{.Swarm.Managers}}'").read()
if int(manager_node) > 1:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step2. 관리자 노드 최소화\n\
불필요한 관리자 노드가 활성화되어 있습니다.\n\
아래의 명령어를 통해 삭제해 주세요.\n\
    docker node demote <ID>")
res_init = ret[0]; vul = ret[1]

res=1
print("Step3. 자동 잠금 모드 사용")

auto_lock = os.popen("docker swarm unlock-key 2>tmp").read()
error_check = os.popen("cat ./tmp").read()
if (error_check.find('Error')) != -1:
    res = 0
elif (error_check.find('no')) != -1:
    res = 0
os.remove("./tmp")

ret = m.res_chk(res, vul, res_init, title, "\
Step3. 자동 잠금 모드 사용\n\
자동 잠금 모드를 사용하지 않고 있습니다.\n\
아래의 명령어를 사용해서 자동 잠금 모드를 실행해 주세요.\n\
    (swarm 모드 시작 시 적용)docker swarm init –autolock\n\
    (swarm 모드 동작 중 적용)docker swarm update --autolock")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()