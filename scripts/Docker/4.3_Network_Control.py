import os
import modules as m

print("[#################   ]")
vul=0; res=1; res_init=1

m.init()

title = "4.3. Docker Swarm - Network Control"

m.BAR()
m.CODE(title) # 네트워크 제어
m.BAR()

print("Step1. Docker Swarm 네트워크 인터페이스 설정")
inter_set = os.popen("netstat -lt | grep -i 2377").read()
if (inter_set.find('[::]')) != -1:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. Docker Swarm 네트워크 인터페이스 설정\n\
모든 인터페이스에서 Docker Swarm에 접근이 가능하도록 설정되어 있습니다.\n\
아래의 명령어를 사용해서 특정 인터페이스에서만 접근이 가능하도록 설정해 주세요.\n\
    docker swarm init --listen-addr example IP")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()
