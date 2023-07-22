import os
import re
import modules as m

print("[############        ]")
vul=0; res=1; res_init=1
m.init()

title="3.1 Images - Dockerfile Config"
m.BAR()
m.CODE(title)
m.BAR()

print("Step1. 컨테이너 사용자 지정")
container_users = os.popen("docker ps --quiet --all | xargs docker inspect --format '{{ .Id }}: User={{ .Config.User }}' | awk -F '=' '{print $2}'").read().splitlines()

for container_user in container_users:
    if container_user != '':    # 왜인지 or로 처리가 안되네요
        if (container_user.find('root')) == -1:
            res=0
            break
ret = m.res_chk(res, vul, res_init, title, "\
Step1. 컨테이너 사용자 지정\n\
컨테이너 사용자가 지정되어 있지 않습니다.\n\
dockerfile 생성 시 아래 명령어를 추가해서 사용자 지정해 주세요.\n\
    RUN useradd -d /home/username -m -s /bin/bash username \nUSER username")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. Dockerfile 내 secrets 존재 여부 확인")
image_list = os.popen("docker images | awk '{print $3}'").read().splitlines()

for i in range(1, len(image_list)):
    check_secret = os.popen("docker history "+image_list[i]+" | grep secret").read()
    if (re.search("\W+", check_secret)) is not None:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step2. Dockerfile 내 secrets 존재 여부 확인\n\
dockerfile 내 secret(패스워드, 키 등)이 존재합니다.\n\
해당 내용을 삭제해 주세요.")
res_init = ret[0]; vul = ret[1]

res=1
print("Step3. setuid 및 setgid 권한 제거")
for i in range(1, len(image_list)):
    suid_sgids = os.popen("docker run "+image_list[i]+" find / -perm +6000 -type f -exec ls -ld {} \; 2> /dev/null | awk '{print $NF}'").read().splitlines()
    for suid_sgid in suid_sgids:
        check = os.popen("find "+suid_sgid+" -perm -4000 -o -perm -2000").read()
        if re.search("\W+", check) is None:
            res=0
            break
ret = m.res_chk(res, vul, res_init, title, "\
Step3. setuid 및 setgid 권한 제거\n\
dockerfile에 setuid 또는 setgid의 권한이 존재합니다.\n\
dockerfile 생성 시 아래 명령어를 추가하여 권한을 제거해 주세요.\n\
    docker run <Image_ID> find / -perm +6000 -type f -exec ls -ld {} \; 2> /dev/null")
res_init = ret[0]; vul = ret[1]

res=1
print("Step4. ADD 대신 COPY 사용")
for i in range(1, len(image_list)):
    check_secret = os.popen("docker history "+image_list[i]+" | grep ADD").read()
    if (re.search("\W+", check_secret)) is not None:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step4. ADD 대신 COPY 사용\n\
dockerfile 내 ADD명령어를 사용중입니다.\n\
    ADD대신 COPY 명령어를 사용해 주세요.")
res_init = ret[0]; vul = ret[1]

res=1
print("Step5. Dockerfile을 통한 업데이트 금지")
updating_commands = ['apt-get update', 'apt update', 'yum update']

for i in range(1, len(image_list)):
    for updating_command in updating_commands:
        check_secret = os.popen("docker history "+image_list[i]+" | grep '"+updating_command+"'").read()
        if (re.search("\W+", check_secret)) is not None:
            res=0
            break
ret = m.res_chk(res, vul, res_init, title, "\
Step5. Dockerfile을 통한 업데이트 금지\n\
dockerfile 내 업데이트 명령어를 사용중입니다.\n\
    해당 명령어를 삭제해 주세요.")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()