import os
import re
import modules as m

print("[#####           ]")
vul=0; res=1; res_init=1
m.init()

title="1.5. Podman Configuration - Container Network Control"
m.BAR()
m.CODE(title) # 컨테이너 네트워크 제어
m.BAR()

print("Step1. bridge 방식의 default 네트워크를 제한 1) default 네트워크 사용 여부")
default_network = os.popen("podman network ls --quiet | xargs podman network inspect --format '{{ .Name }}:{{ .Options }}'").read().splitlines()[0]
if re.search(".+icc:false.+", default_network) is None:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. bridge 방식의 default 네트워크를 제한 - 1) default 네트워크 사용 여부\n\
bridge 방식의 default 네트워크를 사용중입니다.\n\
아래의 명령어 사용하여 bridge 방식의 default 네트워크 제한시켜주세요.\n\
    podmand --icc=false")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. bridge 방식의 default 네트워크를 제한 2) podman0 인터페이스 사용 여부 확인\n ")
interface_podman0 = os.popen("podman network ls --quiet | xargs xargs podman network inspect --format '{{ .Name }}:{{ .Options }}'").read().splitlines()[0]
if re.search(".+podman0.+", interface_podman0) is not None:
    res = 0 # podman0 인터페이스 사용중 : 취약

ret = m.res_chk(res, vul, res_init, title, "\
Step2. bridge 방식의 default 네트워크를 제한 - 2) podman0 인터페이스 사용 여부 확인\n\
podman() 인터페이스를 사용중입니다.\n\
사용자 정의 네트워크를 별도로 설정해서 사용해 주세요.")
res_init = ret[0]; vul = ret[1]

res=1
print("Step3. 불필요한 포트 매핑 금지")
mapped_ports = os.popen("podman ps --quiet | xargs podman inspect --format '{{ .Id }}: Ports={{ .NetworkSettings.Ports }}'").read().splitlines()
for mapped_port in mapped_ports:
    if re.search(".+HostPort:\d+.+", mapped_port) is not None:
    # INSTANCE 조회 결과 : 검토요망
        if int(mapped_port.split()[2].split(':')[1].split(']')[0]) <= 1024:
            res=0 # INSTANCE 조회 결과 : 취약
            break
        # else 인 경우 1024 이하 포트 매핑 X, 특정 인터페이스 지정 여부 검사 적용해야 함
ret = m.res_chk(res, vul, res_init, title, "\
Step3. 불필요한 포트 매핑 금지\n\
podmanfile가 1024이하 포트 또는 서비스 운영 시 불필요한 포트가 매핑되어 있습니다.\n\
컨테이너 실행 시 -p or --publish 옵션을 사용하고, 컨테이너 인스턴스에 필요한 포트를 명시해야됩니다.")
res_init = ret[0]; vul = ret[1]

#호스트 네트워크 인터페이스 설정
res = 1
print("Step4. 호스트 네트워크 인터페이스 설정")
host_network_interface = os.popen("podman ps --quiet | xargs podman inspect --format '{{ .Id }}: Ports={{ .NetworkSettings.Ports }}'").read()
if re.search(".+<nil>.+", host_network_interface) is not None:  #<nil>인 경우 포트가 파드맨 실행시 포트를 지정하지 않음
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step4. 호스트 네트워크 인터페이스 설정\n\
컨테이너 포트가 0.0.0.0이 아닌 특정 인터페이스에 연결되어 있습니다.\n\
아래의 명령어를 통해 컨테이너 포트를 특정 호스트 인터페이스에만 연결하도록 설정해 주세요.\n\
    podman run --detach --publish [ip]:[host interface port port]:[container port]")
res_init = ret[0]; vul = ret[1]

res=1
print("Step5. 컨테이너 내 SSH 실행 금지")
# 1) 컨테이너의 실행 중인 INSTANCE 조회
container_instances = os.popen("podman ps --quiet").read().splitlines()
for container_instance in container_instances:
    # 2) SSH에 대한 프로세스 존재 여부 확인
    check_processes = os.popen("podman exec "+container_instance+" ps -el | grep sshd").read()
    if check_processes is not None:
        res = 0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step5. 컨테이너 내 SSH 실행 금지\n\
컨테이너 내 SSH가 실행되고 있습니다.\n\
컨테이너에서 SSH 서버를 제거해 주세요.")
res_init = ret[0]; vul = ret[1]

res = 1
print("Step6. Userland 프록시 사용 제한")
Userland_proxy = os.popen("ps -ef | grep podmand | grep -v grep").read()
if (Userland_proxy.find("--userland-proxy=false")) == -1:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step6. Userland 프록시 사용 제한\n\
Userland 프록시가 활성화되어 있습니다.\n\
Podman 서비스 실행 시 아래의 옵션을 통해 비활성화해 주세요.\n\
    podmand --userland-proxy=false")
res_init = ret[0]; vul = ret[1]

res = 1
print("Step7. 컨테이너에 podman.socket 마운트 금지")
podman_socket_mount = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}: Volumes={{ .Mounts }}' | grep podman.sock").read()
if (re.search("\W+",podman_socket_mount)) is not None:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step7. 컨테이너에 podman.socket 마운트 금지\n\
컨테이너에 podman.sock 마운트가 되어 있습니다.\n\
컨테이너 내에서 아래 명령어를 실행하여 mount된 podman.sock 삭제해 주세요\n\
    rm -rf /var/run/podman.sock")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()