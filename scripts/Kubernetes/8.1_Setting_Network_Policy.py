import modules as m
import sys

print("["+"#"*20+" "*1+"]")
m.init()
title = "8.1. Etc - Setting Network Policy" # 네트워크 정책 설정

m.BAR()
m.CODE(title) # 앱 취약점
m.BAR()

print("Step1. 네트워크 격리 운영")
m.check()
print("Step2. 일반 트래픽과 관리 트래픽을 분리")
m.check()

m.BAR()
m.INFO("Result : Please Check The Configurations")
m.END()