import os
import re
import modules as m

print("[#               ]")
vul=0; res=1; res_init=1
m.init()

title="1.1. Podman Configuration - HostOS Resouces Access Control"
m.BAR()
m.CODE(title) # 호스트 OS 주요 자원 접근 제어
m.BAR()

print("Step1. 주요 시스템 디렉터리 마운트 금지")

major_directory_mount = os.popen("podman ps --quiet --all | xargs podman inspect --format '{{ .Id }}: Volumes={{ .Mounts }}' 2>/dev/null").read()

split = re.compile("Destination:\W\w+")
need_cks = split.findall(major_directory_mount)

res = 1
for need_ck in need_cks:
    check_list = ['/boot', '/dev', '/etc', '/lib', '/proc', '/sys', '/usr']
    for check in check_list:
        if (need_ck.find(check)) != -1:
            res = 0
            break

ret = m.res_chk(res, vul, res_init, title, "\
Step1. 주요 시스템 디렉터리 마운트 금지\n\
파드맨 컨테이너에 주요한 로컬 디렉토리가 마운트되어 있습니다.\n\
파드맨 컨테이너를 아래 디렉토리로 마운트하지 마십시오. \n\
    '/boot', '/dev', '/etc', '/lib', '/proc', '/sys', '/usr'")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()
