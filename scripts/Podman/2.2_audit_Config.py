import os
import re
import modules as m

print("[##########      ]")
vul=0; res=1; res_init=1

m.init()

title="2.2 Host OS - audit Config"
m.BAR()
m.CODE(title) # audit 설정
m.BAR()

print("Step1. podman 관련 주요 디렉터리 감사(audit)")
podman_major_directories = ["/usr/bin/podman", "/var/lib/podman", "/etc/podman", "/etc/default/podman", "/etc/podman/daemon.json", "/usr/bin/podman-containerd", "/usr/bin/podman-runc"]

os.popen("auditctl 2>tmp")                                                                      # auditctl 명령 실행을 위해 auditd 라이브러리가 설치되어 있는지 확인
auditchk = os.popen("cat tmp").read()
if 'not' in auditchk:                                                                           # auditd 라이브러리가 설치가 안 된 경우
    system = os.popen("cat /etc/*release*").read()
    if system.find('Ubuntu') != -1:                                                             # OS가 'Ubuntu' 라면
        os.popen("apt-get install auditd")                                                      # apt-get 명령어로 설치
    elif system.find('centos') != -1:                                                           # OS가 'centos' 라면
        os.popen("yum install auditd")                                                          # yum 명령어로 설치
for podman_major_directory in podman_major_directories:                                         # 파드맨 주요 디렉터리 반복문 수행
    check_directory_audit = os.popen("auditctl -l | grep '"+podman_major_directory+"'").read()  # 파드맨 주요 디렉터리 감사(audit) 확인
    if re.search("\W+", check_directory_audit) is None:                                         # 문자가 없는 경우 (감사 설정이 안 된 경우) 취약
        res=0
        break

ret = m.res_chk(res, vul, res_init, title, "\
Step1. podman 관련 주요 디렉터리 감사(audit) \n\
podman 관련 주요 디렉터리 감사가 적절하게 설정되어 있지 않습니다.\n\
/etc/audit/rules.d/audit.rules 파일 내 아래와 같이 설정해 주세요.\n\
    -w /usr/bin/podman -k podman 추가\n\
    -w /var/lib/podman -k podman 추가\n\
    -w /etc/podman -k podman 추가\n\
    -w /etc/default/podman -k podman 추가\n\
    -w /etc/podman/daemon.json -k podman 추가\n\
    -w /usr/bin/podman-containerd -k podman 추가\n\
    -w /usr/bin/podman-runc -k podman 추가")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. podman 관련 주요 파일 감사(audit)")
podman_major_files = ["podman.service", "podman.socket"]
for podman_major_file in podman_major_files:
    find_file_location = os.popen("systemctl show -p FragmentPath '"+podman_major_file+"'").read().split('=')[1].split('\n')[0]
    # check_file_audit = os.popen("auditctl -l | grep '"+podman_major_file+"'").read().split()[1].split('\n')[0]
    check_file_audit = os.popen("auditctl -l | grep '"+podman_major_file+"'").read()
    if check_file_audit is list:
        check_file_audit = check_file_audit.split()[1].split('\n')[0]
    if find_file_location != check_file_audit:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step2. podman 관련 주요 파일 감사(audit)\n\
podman 관련 주요 파일 감사가 적절하게 설정되어 있지 않습니다.\n\
/etc/audit/rules.d/audit.rules 파일 내 아래와 같이 설정해 주세요.\n\
podman.service 파일이 존재할 경우:\n\
    -w /usr/lib/systemd/system/podman.service -k podman 추가\n\
podman.socket 파일이 존재할 경우:\n\
    -w /usr/lib/systemd/system/podman.socket -k podman 추가")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()