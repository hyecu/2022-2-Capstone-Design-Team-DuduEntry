import os
import modules as m
import re

print("["+"#"*4+" "*17+"]")
vul=0; chk=1; res=1; res_init=1  #기본값: 양호
title='1.4. API Server Configuration - Admission Control Plugin Settings'
m.init()

m.BAR()
m.CODE(title)
m.BAR()

kube_apiser = os.popen("cat /etc/kubernetes/manifests/kube-apiserver.yaml").read()

print('Step1. Admission Control 설정 검토')

if (kube_apiser.find('--enable-admission-plugins')) != -1:
    reExpress=re.compile('--enable-admission-plugins=.+')  #\w+로 하면 ,로 인자 여러개 있을때 ,때문에 다 안나와서 .+
    excerpt=reExpress.findall(kube_apiser)  #['--enable-admission-plugins=NodeRestriction,AlwaysPullImages']
    str_excerpt=''.join(excerpt)  #--enable-admission-plugins=NodeRestriction,AlwaysPullImages (리스트->str)
    k_value=str_excerpt.split('=')[1]  #NodeRestriction,AlwaysPullImages
    value_list=''.join(k_value).split(',')  #['NodeRestriction', 'AlwaysPullImages']
    
    check_list=['AlwaysPullImages','DenyEscalatingExec','NodeRestriction','SecurityContextDeny','PodSecurityPolicy','EventRateLimit']

    #--enable-admission-plugins에 있어야 할 값들 다 있는지 확인
    for i in check_list:
        if (i not in value_list):
            res=0 #취약
            break
        else:
            next

    #--enable-admission-plugins에 AlwaysAdmit 있으면 취약
    if ('AlwaysAdmit' in value_list): 
        res=0
else:  #--enable-admission-plugins 파라미터 없다면
    res=0

#--disable-admission-plugins
if (kube_apiser.find('--disable-admission-plugins')) != -1: 
    reExpress=re.compile('--disable-admission-plugins=.+') 
    excerpt=reExpress.findall(kube_apiser)  
    str_excerpt=''.join(excerpt)  #(리스트->str)
    k_value=str_excerpt.split('=')[1]  
    value_list=''.join(k_value).split(',')  #--disable-admission-plugins 인자값만 리스트로

    if ('NamespaceLifecycle' in value_list):
        res=0
    
    if ('ServiceAccount' not in value_list):
        res=0
else: #--disable-admission-plugins 파라미터 존재 x
    res=0

#--admission-control-config-file
if (kube_apiser.find('--admission-control-config-file')) != -1:
    reExpress=re.compile('--admission-control-config-file=/.+')
    excerpt=reExpress.findall(kube_apiser)
    if (excerpt) == -1:
        res=0 
else: #--admission-control-config-file 파라미터 존재x
    res=0


ret=m.res_chk(res, vul, res_init, title, '\
Step1. Admission Control 설정 검토\n\
/etc/kubernetes/manifests/kube-apiserver.yaml 파일 내 아래 파라미터가 존재하지 않거나 적절한 인자 값 설정이 되어있지 않습니다.\n\
파라미터 및 적절한 인자값을 설정해주세요.\n\
    --enable-admission-plugins\n\
        (추가)AlwaysPullImages, DenyEscalatingExec, NodeRestriction, SecurityContextDeny, PodSecurityPolicy, EventRateLimit\n\
        (제거)AlwaysAdmit\n\
    --disable-admission-plugins\n\
        (추가)ServiceAccount\n\
        (제거)NamespaceLifecycle\n\
    --admission-control-config-file=<path/to/configuration/file>')
res_init = ret[0]; vul = ret[1]

m.BAR()
m.vul_chk(vul)
m.END()
