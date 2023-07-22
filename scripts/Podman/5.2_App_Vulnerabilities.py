import modules as m
import sys

print("[############### ]")

m.init()

title = "5.2. Etc - App Vulnerabilities"

m.BAR()
m.CODE(title) # 앱 취약점
m.BAR()

print("Step1. 앱 취약점")
m.check()

m.BAR()
m.INFO("Result : Please Check The Configurations")
m.END()