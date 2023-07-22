from openpyxl import Workbook
import datetime as dt
import os
import re

Absolute_path = "/home/ansible/ansible-playbook/diagnose/result"

systems = os.popen("ls "+Absolute_path).read().split()
services=['docker', 'kubernetes', 'podman']
upservices=['Docker', 'Kubernetes', 'Podman']

for i in range(0,len(systems)):
    find_std = os.popen("find "+Absolute_path+"/"+systems[i]+" -name stdout.txt").read().splitlines()

    docker_good = 0
    docker_vul = 0
    docker_chk = 0

    kuber_good = 0
    kuber_vul = 0
    kuber_chk = 0

    podman_good = 0
    podman_vul = 0
    podman_chk = 0

    #기본 사용하기
    #workbook 생성하기
    workbook = Workbook()

    #현재 workbook의 활성화 된 Sheet 가져오기
    sheet = workbook.active

    #해당 이름으로 시트 추가
    sheet.title = 'Total'
    for n in range(0,len(services)):
        for j in range(0,len(find_std)):
            if find_std[j].find(services[n]) != -1:
                globals()["sheet{}".format(n)] = workbook.create_sheet(upservices[n])
                # cell에 직접 데이터 입력하기
                globals()["sheet{}".format(n)]['A1'] = "진단 대상"
                globals()["sheet{}".format(n)]['B1'] = "분류"
                globals()["sheet{}".format(n)]['C1'] = "항목"
                globals()["sheet{}".format(n)]['D1'] = "진단 결과"
                globals()["sheet{}".format(n)]['E1'] = "점검 날짜"
                globals()["sheet{}".format(n)]['F1'] = "Good"
                globals()["sheet{}".format(n)]['G1'] = "Vulnerable"
                globals()["sheet{}".format(n)]['H1'] = "Check The Configurations"

                df = open(find_std[j], 'r', encoding="UTF-8")
                #줄바꿈 기준으로 자르기
                lines = df.read().splitlines()
                
                good=''; vul=''; chk=''
                for line in lines:
                    if line.find('-') != -1:
                        split_line = line.split('-')
                        number = (split_line[0].split()[0][5:])
                        category = " ".join(split_line[0].split()[1:])
                        if category.find(upservices[n]) != -1:
                            category = category.split()[1]
                        title = split_line[1][1:-4]
                        name = number+" "+title
                        date = dt.datetime.now()
                    if line.find(':') != -1:
                        result = line.split(':')[1].strip()[:-4]
                        if result.find("Good") != -1:
                            good=1
                            if services[n] == 'docker':
                                docker_good += 1
                            elif services[n] == 'kubernetes':
                                kuber_good += 1
                            elif services[n] == 'podman':
                                podman_good += 1
                        elif result.find("Vulnerable") != -1:
                            vul=1
                            if services[n] == 'docker':
                                docker_vul += 1
                            elif services[n] == 'kubernetes':
                                kuber_vul += 1
                            elif services[n] == 'podman':
                                podman_vul += 1
                        elif result.find("Check") != -1:
                            chk=1
                            if services[n] == 'docker':
                                docker_chk += 1
                            elif services[n] == 'kubernetes':
                                kuber_chk += 1
                            elif services[n] == 'podman':
                                podman_chk += 1

                    if line.find('───') != -1:
                        globals()["sheet{}".format(n)].append([services[n], category, name, result, date, good, vul, chk])
                        good = ''; vul = ''; chk=''

    sheet['B1'] = "Good"
    sheet['C1'] = "Vulnerable"
    sheet['D1'] = "Check The Configurations"
    sheet['F1'] = "Category"
    sheet['G1'] = "Results"
    sheet.append(['Docker', docker_good, docker_vul, docker_chk])
    sheet.append(['Kubernetes', kuber_good, kuber_vul, kuber_chk])
    sheet.append(['Podman', podman_good, podman_vul, podman_chk])
    sheet['F2'] = "Good"
    sheet['G2'] = docker_good + kuber_good + podman_good
    sheet['F3'] = "Vulnerable"
    sheet['G3'] = docker_vul + kuber_vul + podman_vul
    sheet['F4'] = "Check The Configurations"
    sheet['G4'] = docker_chk + kuber_chk + podman_chk

    # 파일 저장하기
    workbook.save(Absolute_path+"/"+systems[i]+"/"+systems[i]+"_result.xlsx")
