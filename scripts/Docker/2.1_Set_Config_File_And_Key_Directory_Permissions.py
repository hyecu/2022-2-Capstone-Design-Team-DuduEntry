import os
import modules as m

print("[##########          ]")
vul=0; res=1; res_init=1

m.init()

title="2.1 Host OS - Permission Settings for Config Files and Major Directories"
m.BAR()
m.CODE(title) # 설정 파일 및 주요 디렉터리 권한 설정
m.BAR()

print("Step1. 설정 파일 및 디렉터리 권한 설정")

docker_files = ['service', 'socket']
files = ['', '', '/var/run/docker.sock', '/etc/docker/daemon.json', '/etc/docker', '/etc/default/docker']
check_files = ['/usr/lib/systemd/system/docker.service', '/usr/lib/systemd/system/docker.socket']
perm = ['644', '644', '660', '644', '755', '644']


for i in range(0,2):
    files[i] = os.popen("systemctl show -p FragmentPath docker."+docker_files[i]+" | sed 's/^.*=//'").read().strip()
    if (files[i][:4]) != "/usr":
        files[i] = "/usr" + files[i]

for r in range(0,2):
    if (files[r] != check_files[r]):
        res = 0

for l in range(0,6):
    check = m.perm_chk(files[l], perm[l])
    if check == 0:
        res=0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. 설정 파일 및 디렉터리 권한 설정\n\
파일의 경로가 맞지않거나 파일 소유 및 권한이 적절하게 설정되지 않았습니다.\n\
    docker.service의 경로는 "+check_files[0]+"\n\
    docker.socket의 경로는 "+check_files[1]+"로 설정해 주세요.\n\
파일 위치별 권한은 아래와 같이 설정해 주세요.\n\
    "+files[0]+"는 "+perm[0]+"\n\
    "+files[1]+"는 "+perm[1]+"\n\
    "+files[2]+"는 "+perm[2]+"\n\
    "+files[3]+"는 "+perm[3]+"\n\
    "+files[4]+"는 "+perm[4]+"\n\
    "+files[5]+"는 "+perm[5]+"\n")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()