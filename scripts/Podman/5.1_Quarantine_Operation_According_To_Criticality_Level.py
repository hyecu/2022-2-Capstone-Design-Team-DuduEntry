import modules as m
import sys

print("[##############  ]")

m.init()

title = "5.1. Etc - Quarantine Operation According To Criticality Level"

m.BAR()
m.CODE(title) # 중요도 수준에 따른 격리 운영
m.BAR()

print("Step1. 중요도 수준에 따른 격리 운영")
m.check()

m.BAR()
m.INFO("Result : Please Check The Configurations")
m.END()