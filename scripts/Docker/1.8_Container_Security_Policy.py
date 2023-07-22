import os
import re
import sys
import modules as m

print("[########            ]")
vul=0; res=1; res_init=1
m.init()

title="1.8 Docker Configuration - Container Security Policy"
m.BAR()
m.CODE(title) # 컨테이너 보안 정책
m.BAR()

print("Step1. seccomp 프로필 사용 여부")
use_seccomp_profiles = os.popen("docker ps --quiet --all | xargs docker inspect --format '{{ .HostConfig.SecurityOpt }}'").read().splitlines()
for use_seccomp_profile in use_seccomp_profiles:
    if (use_seccomp_profile.find("seccomp")) == -1:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step1. seccomp 프로필 사용 여부\n\
default seccomp 프로필을 사용하지 않고 있습니다.")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. seccomp 프로필 적용 여부")
apply_seccomp_profile = os.popen("docker info --format '{{ .SecurityOptions }}'").read()
if (apply_seccomp_profile.find("seccomp")) == -1:
    res=0
ret = m.res_chk(res, vul, res_init, title, "\
Step2. seccomp 프로필 적용 여부\n\
default seccomp 프로필을 적용하지않고 있습니다.\n\
아래의 명령어를 통해 seccomp 프로필을 적용해 주세요.\n\
    dockerd --seccomp-profile <seccomp 프로파일 파일 경로>")
res_init = ret[0]; vul = ret[1]

res=1
print("Step3. AppArmor 프로필 활성화")
AppArmor_profiles = os.popen("docker ps --quiet --all | xargs docker inspect --format '{{ .AppArmorProfile }}'").read().splitlines()
for AppArmor_profile in AppArmor_profiles:
    if re.search("\W+", AppArmor_profile) is None:
        res = 0
        break
ret = m.res_chk(res, vul, res_init, title, '\
Step3. AppArmor 프로필 활성화\n\
AppArmor 프로필이 활성화되어 있지 않습니다.\n\
아래의 옵션을 통해 컨테이너를 실행해 주세요.\n\
    --security-opt="apparmor=<생성한 apparmor 프로필>"')
res_init = ret[0]; vul = ret[1]

res=1
print("Step4. SELinux 사용")
SELinux = os.popen("docker ps --quiet --all | xargs docker inspect --format '{{ .HostConfig.SecurityOpt }}'").read()
if (SELinux.find("no value")) != -1: # 'no value' 가 아니면 양호
    res=0
ret = m.res_chk(res, vul, res_init, title, "\
Step4. SELinux 사용\n\
SELinux를 사용하고 있지 않습니다.\n\
SELinux가 활성화 된 상태에서 아래와 같이 실행시킨 후, docker daemon --selinux-enabled\n\
컨테이너 실행 시 아래와 같은 옵션을 사용해 주세요.\n\
    docker run --interactive --tty --security-opt label=level:TopSecret centos /bin/bash")
res_init = ret[0]; vul = ret[1]

res = 1
print("Step5. 컨테이너 내 리눅스 커널 Capabilities 제한")
CapAdd = os.popen("docker ps --quiet --all | xargs docker inspect --format '{{ .HostConfig.CapAdd }}'").read()
CapDrop = os.popen("docker ps --quiet --all | xargs docker inspect --format '{{ .HostConfig.CapDrop }}'").read()
if (CapAdd.find("no value")) == -1 or (CapDrop.find("no value")) == -1:
    res = 0

if res == 1:
    m.ok()
else:
    m.check()
    sys.stdout = open('verbose', 'a')
    if res_init == 1:
        m.BAR()
        print(title)
        m.BAR()
        res_init=0
    print("\
Step5. 컨테이너 내 리눅스 커널 Capabilities 제한\n\
컨테이너 실행 시 사용 환경에 맞게 아래와 같이 기능 추가 및 제거:\n\
    # 필요한 Capabilities 추가\n\
    docker run --cap-add={'Capability 1','Capability 2'}\n\
    # 필요하지 않은 Capabilities 삭제\n\
    docker run --cap-drop={'Capability 1','Capability 2'}\n\
    # 모든 Capabilities 삭제 후 필요한 Capabilities 추가\n\
    docker run --cap-drop=all --cap-add={'Capability 1','Capability 2'}")
    m.END()
    sys.stdout = open('stdout.txt', 'a')

m.BAR()
if vul == 1:
    m.BAD("Result : Vulnerable")
elif res == 0:
    m.INFO("Result : Please Check The Configurations")
else:
    m.OK("Result : Good")
m.END()