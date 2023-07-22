import os
import sys

def init():
    sys.stdout = open('stdout.txt', 'a')

def BAR():
    print("=================================================================")

def END():
    print("─────────────────────────────────────────────────────────────────")

def OK(argv):
    print('\033[32m[GOOD] ' + argv + '\033[0m')

def BAD(argv):
    print('\033[31m[BAD] ' + argv + '\033[0m')

def INFO(argv):
    print('\033[35m[INFO] ' + argv + '\033[0m')

def CODE(argv):
    print('\033[36m' + argv + '\033[0m')

def ok():
    print("...................ok")

def fail():
    print("...................fail")

def check():
    print("...................check")

def vul_chk(num):
    if num == 1:
        BAD("Result : Vulnerable")
    else:
        OK("Result : Good")

def vul_chk_with_chk(vul, chk): # 이걸로 통합하기
    if vul == 1:
        BAD("Result : Vulnerable")
    elif chk == 0:
        INFO("Result : Please Check The Configurations")
    else:
        OK("Result : Good")

def res_chk(num, vul, res_init, title, txt):
    if num == 1:
        ok()
    else:
        fail()
        sys.stdout = open('verbose', 'a')
        if res_init == 1:
            BAR()
            print(title)
            BAR()
            res_init=0
        CODE("Vulnerable")
        print(txt)
        END()
        sys.stdout = open('stdout.txt', 'a')
        vul = 1
    ret = [res_init, vul]
    return ret

def res_chk_with_chk(num, vul, chk, res_init, title, chk_txt, txt): # 이걸로 통합하기
    if num == 0:
        fail()
        sys.stdout = open('verbose', 'a')
        if res_init == 1:
            BAR()
            print(title)
            BAR()
            res_init=0
        CODE("Vulnerable")
        print(txt)
        END()
        sys.stdout = open('stdout.txt', 'a')
        vul = 1
    elif chk == 0:
        check()
        sys.stdout = open('verbose', 'a')
        if res_init == 1:
            BAR()
            print(title)
            BAR()
            res_init=0
        CODE("Check")
        print(chk_txt)
        END()
        sys.stdout = open('stdout.txt', 'a')
    else:
        ok()
    ret = [res_init, vul]
    return ret

def perm_chk(file,perm): # 남겨두기
    if ((os.popen("stat -c %a:%U:%G "+file).read()).find(str(perm))) != -1:
        return 1
    else:
        return 0