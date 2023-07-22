import os
import re
import modules as m

print("[#######         ]")
vul=0; res=1; res_init=1
m.init()

title="1.7. Podman Configuration - Container Privilege Control"
m.BAR()
m.CODE(title) # 컨테이너 권한 제어
m.BAR()

cgroup_list = open('cgroup_list_1.7.txt', 'r')

print("Step1. suid/sgid 제한 1) podman daemon 설정") # '--no-new-privileges' 값이 적절하게 설정되어 있는지 확인
daemon_suid_sgid = os.popen("ps -ef | grep podmand | grep -v grep").read()
if (daemon_suid_sgid.find('no-new-privileges')) == -1:
    res=0
ret = m.res_chk(res, vul, res_init, title, "\
Step1. suid/sgid 제한 1) podman daemon 설정\n\
--no-new-privileges 값이 적절하게 설정되어 있지 않습니다.\n\
아래의 명령어를 통해 suid/sgid 제한을 해주세요.\n\
    podmand --no-new-privileges")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. suid/sgid 제한 2) podman runtime 설정") # '--security-opt' 값이 적절하게 설정되어 있는지 확인
runtime_suid_sgid = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}:SecurityOpt={{ .HostConfig.SecurityOpt }}'").read()
if (runtime_suid_sgid.find('no-new-privileges')) == -1:
    res=0 # suid/sgid 제한 - podman runtime 설정 : 취약
ret = m.res_chk(res, vul, res_init, title, "\
Step2. suid/sgid 제한 2) podman runtime 설정\n\
--security-opt 값이 적절하게 설정되어 있지 않습니다.\n\
아래의 명령어를 통해 suid/sgid 제한을 해주세요.\n\
    podman run --rm -it --security-opt=no-new-privileges ubuntu bash")
res_init = ret[0]; vul = ret[1]

# 실험(Experimental) 기능 비활성화
res=1
print("Step3. 실험(Experimental) 기능 비활성화")
experimental = os.popen("podman version --format '{{ .Server.Experimental }}'").read()
if (experimental.find('false')) == -1:
    res=0 # 실험(Experimental) 기능 비활성화 X : 취약
ret = m.res_chk(res, vul, res_init, title, "\
Step3. 실험(Experimental) 기능 비활성화\n\
Experimental 기능이 활성화되어 있습니다.\n\
아래의 옵션을 통해 Experimental 기능을 비활성화해 주세요.\n\
    --experimental")
res_init = ret[0]; vul = ret[1]

res=1
print("Step4. cgroup 변경 금지 1) podman daemon 설정") # '--cgroup-parent' 및 적절한 cgroup 설정 여부 확인
daemon_cgroup = os.popen("ps -ef | grep podmand | grep -v grep").read()
if (re.search("--cgroup-parent=\W\w+",daemon_cgroup)) is not None:
    res=0
ret = m.res_chk(res, vul, res_init, title, "\
Step4. cgroup 변경 금지 1) podman daemon 설정\n\
--cgroup-parent 및 cgroup가 적절하게 설정되어 있지 않습니다.\n\
아래의 명령어를 통해 cgroup를 변경해 주세요.\n\
    podmand --cgroup-parent=/foobar")
res_init = ret[0]; vul = ret[1]

res=1
# cgroup을 변경하지 않거나 cgroup 변경 내용을 관리하고 있는 경우 양호
print("Step5. cgroup 변경 금지 2) podman runtime 설정")
runtime_cgroups = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .HostConfig.CgroupParent }}'").read().splitlines()
for runtime_cgroup in runtime_cgroups:
    if re.search("\w+",runtime_cgroup) is not None:
        for cgroup in cgroup_list:
            if (runtime_cgroup.find(cgroup)) == -1:
                res=0
                break
ret = m.res_chk(res, vul, res_init, title, "\
Step5. cgroup 변경 금지 2) podman runtime 설정\n\
디폴트 cgroup 또는 그 외의 cgroup가 적절하게 설정되어 있지 않습니다.\n\
필요한 경우가 아닐 경우 아래의 옵션을 사용하여 컨테이너 실행을 금지시켜주세요.\n\
    --cgroup-parent")
res_init = ret[0]; vul = ret[1]

res=1
print("Step6. privilege 컨테이너 사용 제한")
privileged = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .HostConfig.Privileged }}'").read()
if (privileged.find('true')) != -1:
    res=0
ret = m.res_chk(res, vul, res_init, title, "\
Step6. privilege 컨테이너 사용 제한\n\
컨테이너 권한이 적절하게 설정되어 있지 않습니다.\n\
필요한 경우가 아닐 경우 아래의 옵션을 사용하여 컨테이너 실행을 금지시켜주세요.\n\
    --privileged")
res_init = ret[0]; vul = ret[1]

# ausearch 명령어 실행 결과 <no matches>가 출력되는 경우 해당 출력을 리다이렉션을 통해 받아올 수 없음.
# 따라서 python을 통해 명령어를 실행하고, 오류를 리다이렉션 하는 방법을 이용해야 함.
res=1
print("Step7. exec와 privileged 옵션 동시 사용 금지")
os.popen("python3 ./sub_file_fir_1.7.py 2>tmp").read()
res = os.popen("cat ./tmp").read()
if (res.find('no matches')) == -1:
    res=0
ret = m.res_chk(res, vul, res_init, title, "\
Step7. exec와 privileged 옵션 동시 사용 금지\n\
exec와 -privileged 옵션을 동시에 사용하고 있습니다.\n\
exec와 -privileged 옵션을 동시에 사용하지 않도록 설정해 주세요.")
res_init = ret[0]; vul = ret[1]
os.remove("./tmp")

res=1
print("Step8. exec와 user 옵션 동시 사용 여부 확인")
os.popen("python3 ./sub_file_sec_1.7.py 2>tmp").read()
res = os.popen("cat ./tmp").read()
if (res.find('no matches')) == -1:
    res=0
ret = m.res_chk(res, vul, res_init, title, "\
Step8. exec와 user 옵션 동시 사용 여부 확인\n\
exec와 --user 옵션을 동시에 사용하고 있습니다.\n\
exec와 --user 옵션을 동시에 사용하지 않도록 설정해 주세요.")
res_init = ret[0]; vul = ret[1]
os.remove("./tmp")

res=1
print("Step9. 컨테이너 Root Filesystem을 read only으로 설정") #(true=read only, flase=read/write)
root_filesystem = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}:ReadonlyRootfs={{ .HostConfig.ReadonlyRootfs }}' | awk -F '=' '{print $2}'").read()
if (root_filesystem.find("true")) == -1:
    res=0 # Root Filesystem을 read only으로 설정 X : 취약
ret = m.res_chk(res, vul, res_init, title, "\
Step9. 컨테이너 Root Filesystem을 read only으로 설정\n\
컨테이너 Root Filesystem의 상태가 적절하게 설정되어 있지 않습니다.\n\
아래의 명령어를 통해 read only로 설정해 주세요.\n\
    podman run <Run arguments> --read-only <Container Image Name or ID> <Command>")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()