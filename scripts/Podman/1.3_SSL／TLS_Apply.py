import os
import modules as m


print("[###             ]")
vul=0; res=1; res_init=1
m.init()
checks = ['tlsverify', 'tlscacert', 'tlscert', 'tlskey']

title = "1.3. Podman Configuration - SSL/TLS Apply"

m.BAR()
m.CODE(title) # SSL/TLS 적용
m.BAR()

print("Step1. SSL/TLS 암호화 적용 여부")
ssl_tls = os.popen("ps -ef | grep podmand | grep -v grep").read()
for check in checks:
    if (ssl_tls.find(check)) == -1:
        res=0
        break
ret = m.res_chk(res, vul, res_init, title, "\
Step1. SSL/TLS 암호화 적용 여부 \nSSL/TLS 암호화가 적용되지 않았습니다.\n\
openssl을 사용하여 키 생성을 하고, 아래의 옵션을 넣으세요. \n\
    podman --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem -H=$HOST:2376 version")
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()