from openpyxl import Workbook
import datetime as dt
import os
import re

Absolute_path = "/home/ansible/ansible-playbook/diagnose/result"
systems = os.popen("ls "+Absolute_path).read().split()
services=['docker', 'kubernetes', 'podman']
upservices=['Docker', 'Kubernetes', 'Podman']

for i in range(0,len(systems)):
    find_ver = os.popen("find "+Absolute_path+"/"+systems[i]+" -name verbose").read().splitlines()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Verbose'

    sheet['A1'] = "진단 대상"
    sheet['B1'] = "분류"
    sheet['C1'] = "항목"
    sheet['D1'] = "스텝"
    sheet['E1'] = "취약한 설정 내용"
    sheet['F1'] = "설정 방법"
    sheet['G1'] = "점검 날짜"

    explain=[]; settings=[]; step=[]
    for j in range(0,len(find_ver)):
        for n in range(0,len(services)):
            if find_ver[j].find(services[n]) != -1:
                df = open(find_ver[j], 'r', encoding="UTF-8")
                lines = df.read().splitlines()

                for k in range(0,len(lines)):
                    if re.search("\d\.\d.+-.+", lines[k]) is not None:      # 타이틀 라인
                        split_line = lines[k].split('-')
                        number = (split_line[0].split()[0])
                        category = " ".join(split_line[0].split()[1:])
                        if category.find(upservices[n]) != -1:
                            category = category.split()[1]
                        title = number+' '+split_line[1]
                        date = dt.datetime.now()
                        next
                    
                    if re.search("Step\d\.+", lines[k]) is not None:       # 스텝 라인
                        step.append(lines[k])
                        next
                    if re.search("^\w+.+\.$", lines[k]) is not None or re.search("^\w+.+:$", lines[k]) is not None:            # 설명
                        explain.append(lines[k])
                    if re.search("^\s.+", lines[k]) is not None:             # 설정 방법
                        settings.append(lines[k])
                        next
                    
                    if k < len(lines)-1:
                        if lines[k].find('──') != -1 and lines[k+1].find('===') != -1:     # 끝 라인
                            explain = "\n".join(explain)
                            settings = "\n".join(settings)
                            step = "\n".join(step)
                            sheet.append([services[n], category, title, step, explain, settings, date])
                            explain=[]; settings=[]; step=[]

                sheet.append([' ', ' ', ' ', ' ', ' ', ' ', ' '])

    workbook.save(Absolute_path+"/"+systems[i]+"/"+systems[i]+"_verbose.xlsx")
