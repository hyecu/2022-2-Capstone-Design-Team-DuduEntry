import os
import modules as m
import re

print("["+"#"*19+" "*2+"]")
vul=0; res=1; res_init=1  #기본값: 양호
title="7.2 Host OS - Set Certificate File Permissions"
m.init()

m.BAR()
m.CODE(title)
m.BAR()

print("Step1. 인증서 파일 권한 설정")

text=os.popen('ps -ef | grep kubelet | grep "\--client-ca-file"').read()
reExpress=re.compile("--client-ca-file=/\w+(?:/\w+)+.crt") 
excerpt=reExpress.findall(text)[0]  #--client-ca-file=경로 (str형식)
file=excerpt.split('=')[1] #검사할 파일 경로만


permCheck=m.perm_chk(file,644)
if permCheck==0:  #권한 644 아닌 경우
    res=0
    ret=m.res_chk(res, vul, res_init, title, "\
Step1. 인증서 파일 권한 설정\n\
client ca 인증서:\n\
파일의 권한이 644로 되어있지 않습니다.\n\
    client ca 인증서 파일의 권한을 644로 바꾸고 소유자 및 그룹 권한이 root로 되어있는지 확인해 주세요.")
    res_init = ret[0]; vul = ret[1]


else: #권한 644이면 소유자+그룹권한 확인
    check=os.popen('stat -c %U:%G '+file).read().split(':')
    if check[0].find('root') == -1: #소유자 체크, root가 아니면 취약
        res=0
        ret=m.res_chk(res, vul, res_init, title, "\
Step1. 인증서 파일 권한 설정\n\
client ca 인증서 파일의 권한이 644로 되어있으나 소유자가 root가 아닙니다.\n\
    소유자를 root로 바꾼 후 그룹 권한이 root로 되어있는지 확인해 주세요.")
        res_init = ret[0]; vul = ret[1]

    elif check[1].find('root') == -1: #소유그룹 체크, root가 아니면 취약
        res=0
        ret=m.res_chk(res, vul, res_init, title, "\
Step1. 인증서 파일 권한 설정\n\
client ca 인증서 파일의 권한이 644로 되어있고 소유자가 root이나 그룹 권한이 root로 되어있지 않습니다.\n\
    그룹 권한을 root로 바꿔주세요.")
        res_init = ret[0]; vul = ret[1]

if vul==0: #ok, fail안떠서 수동으로 준 것
    m.ok()
else:
    m.fail()

# text=os.popen('ps -ef | grep kubelet | grep "\-client-ca-file"').read()
# reExpress=re.compile("(?:--\w+)?\-?-client-ca-file=/\w+(?:/\w+)+(?:-?\w+)+.crt") 
# excerpt=reExpress.findall(text)  #-client-ca-file 파라미터 들어간부분 파라미터랑 파일경로 찾기

# for i in range(len(excerpt)): #검색되는 파라미터 수만큼 
#     file=excerpt[i].split('=')[1] #['파라미터','파일경로']로 분할 후 파일경로만 str형으로 가져오기
#     permCheck=m.perm_chk(file,644)
#     if permCheck==0:  #권한 644 아닌 경우
#         res=0
#         vul=m.res_chk(res, vul, 'Step1. 인증서 파일 권한 설정\nclient ca 인증서 파일의 권한이 644로 되어있지 않습니다.\n\
# client ca 인증서 파일의 권한을 644로 바꾸고 소유자 및 그룹 권한이 root로 되어있는지 확인해 주세요.')

#     else: #권한 644이면 -> 소유자, 소유그룹 확인
#         check=os.popen('stat -c %U:%G '+file).read().split(':') 
#         if check[0].find('root') == -1: #소유자 체크, root가 아니면 취약
#             res=0
#             vul=m.res_chk(res, vul, 'Step1. 인증서 파일 권한 설정\nclient ca 인증서 파일의 권한이 644로 되어있으나 소유자가 root가 아닙니다.\n\
# 소유자를 root로 바꾼 후 그룹 권한이 root로 되어있는지 확인해 주세요.')
#         elif check[1].find('root') == -1: #소유그룹 체크, root가 아니면 취약
#             res=0
#             vul=m.res_chk(res, vul, 'Step1. 인증서 파일 권한 설정\nclient ca 인증서 파일의 권한이 644로 되어있고 소유자가 root이나 그룹 권한이 root로 되어있지 않습니다.\n\
# 그룹 권한을 root로 바꿔주세요.')



m.BAR()
m.vul_chk(vul)
m.END()
