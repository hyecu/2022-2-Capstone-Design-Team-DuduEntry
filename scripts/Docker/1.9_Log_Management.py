import os
import modules as m

print("[#########           ]")
vul=0; res=1; res_init=1

m.init()

title="1.9. Docker Configuration - Log Management"
m.BAR()
m.CODE(title) # 로그 관리
m.BAR()

print("Step1. 로그 레벨 설정")
log_level = os.popen("ps -ef | grep docker").read()
if (log_level.find("--log-level=info")) == -1:
    res=0

ret = m.res_chk(res, vul, res_init, title, "\
Step1. 로그 레벨 설정\n\
도커 로그 레벨이 설정되어 있지 않거나, 잘못 설정되어 있습니다.\n\
로그 레벨을 아래처럼 설정해 주세요.\n\
    --log-level='info'")
res_init = ret[0]; vul = ret[1]

res=1
print("Step2. 중앙 집중식 원격 로깅 구성")
log_driver_opt = os.popen("ps -ef | grep dockerd").read()
if (log_driver_opt.find("--log-driver=syslog --log-opt syslog-address=tcp://")) == -1:
    res = 0

ret = m.res_chk(res, vul, res_init, title, "\
Step2. 중앙 집중식 원격 로깅 구성\n\
도커 로그 드라이버가 설정되어 있지 않거나, 잘못 설정되어 있습니다.\n\
로그 드라이버를 아래처럼 설정해 주세요.\n\
    dockerd --log-driver=syslog --log-opt syslog-address=tcp://x.x.x.x")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()
