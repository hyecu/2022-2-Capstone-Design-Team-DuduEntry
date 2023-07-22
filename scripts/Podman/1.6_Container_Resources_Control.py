import os
import modules as m

print("[######          ]")
vul=0; res=1; res_init=1
m.init()

title="1.6. Podman Configuration - Container Resources Control"
m.BAR()
m.CODE(title) # 컨테이너 리소스 제어
m.BAR()

print("Step1. 컨테이너 크기 설정 1) 컨테이너별 할당 공간 확인")
# 1) '--storage-opt dm.basesize' 값 확인 후 컨테이너별 할당 된 공간 확인
check_storage = os.popen("ps -ef | grep podmand | grep -v grep").read()
if (check_storage.find("storage")) != -1:
    m.check()
else:
    m.fail()
    vul=1

res=1
print("Step2. 컨테이너 크기 설정 2) 마운트 된 볼륨을 공유하는지 확인")
shared_volumes = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{range $mnt := .Mounts}} {{json $mnt.Propagation}} {{end}}'").read().splitlines()
for shared_volume in shared_volumes:
    if (shared_volume.find("shared")) != -1:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step2. 컨테이너 크기 설정 2) 마운트 된 볼륨을 공유하는지 확인\n\
마운트 된 볼륨을 공유하고 있습니다.\n\
??? pdf가 이상해요")
res_init = ret[0]; vul = ret[1]

res=1
print("Step3. 메모리 할당 적절성 여부 확인") # (memory=0이면 제한 없음)
memories = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}:Memory={{ .HostConfig.Memory }}' | awk -F '=' '{print $2}'").read().splitlines()
for memory in memories:
    if int(memory) == 0:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step3. 메모리 할당 적절성 여부 확인\n\
메모리가 적절하게 할당되어 있지 않습니다.\n\
컨테이너 실행 시 아래의 명령어를 통해 사용자 환경에 맞게 설정해 주세요.\n\
    podman run --interactive --tty --memory 256m centos /bin/bash")
res_init = ret[0]; vul = ret[1]

res=1
print("Step4. CPU 우선순위 적절성 여부 확인")
cpu_shares = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}:CpuShares={{ .HostConfig.CpuShares }}' | awk -F '=' '{print $2}'").read().splitlines()
for cpu_share in cpu_shares:
    if int(cpu_share) == 0:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step4. CPU 우선순위 적절성 여부 확인\n\
CPU 우선순위가 절절하게 할당되어 있지 않습니다.\n\
컨테이너 실행 시 아래의 명령어를 통해 사용자 환경에 맞게 설정해 주세요.\n\
    podman run --interactive --tty --cpu-shares 512 centos /bin/bash")
res_init = ret[0]; vul = ret[1]

res=1
print("Step5. 프로세스 제한 설정 1) podman daemon 설정") # '--default-ulimit' 파라미터값이 적절하게 설정되어 있는지 확인
daemon_process_limit = os.popen("ps -ef | grep podmand | grep -v grep").read()
if (daemon_process_limit.find('default-ulimit')) == -1:
    res=0
ret = m.res_chk(res, vul, res_init, title, "\
Step5. 프로세스 제한 설정 1) podman daemon 설정\n\
--default-ulimit 파라미터값이 적절하게 설정되어 있지 않습니다.\n\
Podman 서비스 실행 시 아래의 명령어를 통해 프로세스 제한을 설정해 주세요.\n\
    podmand --default-ulimit nproc=1024:2048 --default-ulimit nofile=100:200")
res_init = ret[0]; vul = ret[1]

res=1
print("Step6. 프로세스 제한 설정 2) podman runtime 설정")
runtime_process_limits = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}:Ulimits={{ .HostConfig.Ulimits }}' | awk -F '=' '{print $2}'").read().splitlines()
for runtime_process_limit in runtime_process_limits:
    if (runtime_process_limit.find("no value")) != -1:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step6. 프로세스 제한 설정 2) podman runtime 설정\n\
Ulimits가 적절하게 설정되어 있지 않습니다.\n\
아래의 명령어를 통해 Podman daemon에서 설정한 ulimit을 무시하도록 설정해 주세요.\n\
    podman run --ulimit nofile=1024:1024 --interactive --tty centos /bin/bash")
res_init = ret[0]; vul = ret[1]

res=1
print("Step7. 프로세스 제한 설정 3) 프로세스 생성 제한")
process_limits = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}:PidsLimit={{ .HostConfig.PidsLimit }}' | awk -F '=' '{print $2}'").read().splitlines()
for process_limit in process_limits:
    if (process_limit.find("no value")) != -1:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step7. 프로세스 제한 설정 3) 프로세스 생성 제한\n\
프로세스 생성 제한 여부가 설정되어 있지 않습니다.\n\
아래의 명령어를 통해 설정해 주세요.\n\
    --pids-limit flag")
res_init = ret[0]; vul = ret[1]

res=1
print("Step8. 컨테이너 재시작 횟수 설정 여부 확인")
RestartPolicyName = ['always', 'n', 'no', 'null']
restart_policies = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}:RestartPolicyName={{ .HostConfig.RestartPolicy.Name }}' | awk -F '=' '{print $2}'").read().splitlines()
retry_counts = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}:MaximumRetryCount={{ .HostConfig.RestartPolicy.MaximumRetryCount }}' | awk -F '=' '{print $2}'").read().splitlines()
for i in range(0,len(restart_policies)):
    for l in range(0,len(RestartPolicyName)):
        if(restart_policies[i].find(RestartPolicyName[l])) != -1 or int(retry_counts[i]) == 0:
            res=0
            break
ret = m.res_chk(res, vul, res_init, title, "\
Step8. 컨테이너 재시작 횟수 설정 여부 확인\n\
컨테이너 재시작 횟수가 설정되어 있지 않습니다.\n\
아래의 명령어를 통해 재시작 횟수를 설정해 주세요.\n\
    -restart=on-failure")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()