import os
import re
import yaml
import modules as m


print("["+"#"*15+" "*6+"]")
vul=0; res=1; chk=1; res_init=1
title="6.3. Kubelet Configuration - SSL/TLS Apply" # SSL/TLS 적용
m.init()

m.BAR()
m.CODE(title)
m.BAR()

kubeletService = '/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf'
N_kubeletService = '/etc/systemd/system/kubelet.service.d/10-kubeadm.conf'
kubeletConf = '/var/lib/kubelet/config.yaml'

kubeletService_list = os.popen("cat "+kubeletService+" 2>/dev/null | grep -v '^#' | grep -v '^$'").read()
N_kubeletService_list = os.popen("cat "+N_kubeletService+" 2>/dev/null | grep -v '^#' | grep -v '^$'").read()
# config = "/home/dudu/kubernetes/worker1/config.yaml"

print("Step1. SSL/TLS 적용을 통한 클라이언트 인증 (kubelet to apiserver)")
kubeletService_regex = re.compile("KUBELET_AUTHZ_ARGS=.*--client-ca-file=.+")
kubeletConf_excerpt = os.popen("sed -n '/^authentication:*/,/^\w/ p' "+kubeletConf).read()
kubeletConf_yaml = yaml.safe_load(kubeletConf_excerpt)['authentication']['x509']['clientCAFile']

# 10-kubeadm.conf 파일 내 "KUBELET_AUTHZ_ARGS=--client-ca-file=<파일명>" 으로 설정 여부 검사
if kubeletService_regex.match(kubeletService_list): # 추가
    next # 존재하는 경우: 양호
# config.yaml 파일 내 아래 내용이 존재하는지 검사 (yaml 형식)
# {'authentication': {'x509': {'clientCAFile': '<client CA 파일 경로>'}}}
elif kubeletService_regex.match(N_kubeletService_list): # 추가
    next
elif re.search("(?:\/w+)+.crt", kubeletConf_yaml) is not None: # 추가
    next # 존재하는 경우: 양호
else:
    res=0 # 둘 다 존재하지 않는 경우: 취약
ret=m.res_chk(res, vul, res_init, title, '\
Step1. 권한 검증 수행\n\
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf 혹은 /etc/systemd/system/kublet.service.d/10-kubeadm.conf 파일 내 아래와 같이 설정해 주세요.\n\
    "KUBELET_AUTHZ_ARGS=--client-ca-file=<파일명>"\n\
혹은 /var/lib/kubelet/config.yaml 파일 내 아래와 같이 설정해 주세요.\n\
    authentication:\n\
        x509:\n\
            clientCAFile: <client CA 파일 경로>')
res_init = ret[0]; vul = ret[1]


res=1
print("Step2. 인증서 관리 (Kubelets) (인증서설정)")
kubeletService_regex = re.compile("KUBELET_CERTIFICATE_ARGS=.*--tls-cert-file=.+")
kubeletService_regex = [kubeletService_regex, (re.compile("KUBELET_CERTIFICATE_ARGS=.*--tls-private-key-file=.+"))]

if kubeletService_regex[0].match(kubeletService_list) and kubeletService_regex[1].match(kubeletService_list): # 추가 
    next
elif kubeletService_regex[0].match(N_kubeletService_list) and kubeletService_regex[1].match(N_kubeletService_list): # 추가
    next
elif re.search("tlsCertFile: .+", kubeletConf) is not None and re.search("tlsPrivateKeyFile: .+") is not None: # 추가
    next
else:
    res=0
ret=m.res_chk(res, vul, res_init, title, '\
Step2. 인증서 관리 (Kubelets) (인증서설정)\n\
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf 혹은 /etc/systemd/system/kublet.service.d/10-kubeadm.conf 파일 내 아래와 같이 설정해 주세요.\n\
    "KUBELET_CERTIFICATE_ARGS=--tls-cert-file==<파일명>"\n\
혹은 /var/lib/kubelet/config.yaml 파일 내 아래와 같이 설정해 주세요.\n\
    tlsCertFile: <tls인증서 위치>\n\
    tlsPrivateKeyFile: <tls키 파일 위치>')
res_init = ret[0]; vul = ret[1]

res=1
print("Step3. 인증서 관리 (인증서 교환주기 설정)")
kubeadm_regex = re.compile("KUBELET_CERTIFICATE_ARGS=.*--rotate-certificates=true\s*")
kubeadm_regex = [kubeadm_regex, (re.compile("KUBELET_CERTIFICATE_ARGS=.*--feature-gates=RotateKubeletServerCertificate=true\s*"))]
if kubeadm_regex[0].match(kubeletService_list) and kubeadm_regex[1].match(kubeletService_list): # 추가
    next
elif kubeadm_regex[0].match(N_kubeletService_list) and kubeadm_regex[1].match(N_kubeletService_list): # 추가
    next
elif kubeletConf.find("rotateCertificates: true") != -1: # 추가
    next
else:
    res=0
    
ret=m.res_chk(res, vul, res_init, title, '\
Step3. 인증서 관리 (인증서 교환주기 설정)\n\
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf 혹은 /etc/systemd/system/kublet.service.d/10-kubeadm.conf 파일 내 아래와 같이 설정해 주세요.\n\
    "KUBELET_CERTIFICATE_ARGS 내\n\
        --rotate-certificates=true\n\
        --feature-gates=RotateKubeletServerCertificate=true"\n\
혹은 /var/lib/kubelet/config.yaml 파일 내 아래와 같이 설정해 주세요.\n\
    rotateCertificates: true')
res_init = ret[0]; vul = ret[1]

res=1
print("Step4. 안전한 SSL/TLS 버전 사용")
SSL_TLS_kubeadm = "--tls-ciphersuites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256"
SSL_TLS_config = "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256"
TLSCipherSuites = os.popen('sed -n "/^TLSCipherSuites:*/, ~1 p" '+kubeletConf).read()

if kubeletService_list.find(SSL_TLS_kubeadm) != -1: # 추가
    next
elif N_kubeletService_list.find(SSL_TLS_kubeadm) != -1: # 추가
    next
elif TLSCipherSuites.find(SSL_TLS_config) != -1: # 추가
    next
else:
    res=0

ret=m.res_chk(res, vul, res_init, title, '\
Step4. 안전한 SSL/TLS 버전 사용\n\
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf 혹은 /etc/systemd/system/kublet.service.d/10-kubeadm.conf 파일 내 아래와 같이 설정해 주세요.\n\
    '+SSL_TLS_kubeadm+'\n\
혹은 /var/lib/kubelet/config.yaml 파일 내 아래와 같이 설정해 주세요.\n\
    TLSCipherSuites:\n\
        '+SSL_TLS_config)
res_init = ret[0]; vul = ret[1]

res=1
print("Step5. node hostname 임의 변경 금지")
if re.search("KUBELET_SYSTEM_PODS_ARGS=.*--hostname-override.*", kubeletService_list) is None: # 제거
    res=0
elif re.search("KUBELET_SYSTEM_PODS_ARGS=.*--hostname-override.*", N_kubeletService_list) is None: # 제거
    res=0

ret=m.res_chk(res, vul, res_init, title, '\
Step5. node hostname 임의 변경 금지\n\
/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf 혹은 /etc/systemd/system/kublet.service.d/10-kubeadm.conf 파일 내에 아래와 같이 설정해 주세요.\n\
    "KUBELET_CERTIFICATE_ARGS 내\n\
        --hostname-override 존재할 경우 제거')
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.BAR()