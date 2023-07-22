#!/bin/bash

# OS 확인
if [ `cat /etc/*release* | grep Ubuntu | wc -l` -ne 0 ];
then
	OS=Ubuntu
elif [ `cat /etc/*release* | grep centos | wc -l` -ne 0 ];
then
	OS=centos
fi

# Python3 설치 확인
if [ `python3 -V | wc -l` -eq 0 ];
then
	if [ $OS -eq 'Ubuntu' ];
	then
		apt-get install -y python3
	elif [ $OS -eq 'centos' ];
	then
		yum install -y python3
	fi
fi

# python-dateutil library 확인
if [ `pip3 list 2>tmp | grep dateutil | wc -l` -eq 0 ];
then
	# pip 설치 확인
	pip3 2>tmp
	if [ -s tmp ];
	then
		if [ $OS = 'Ubuntu' ];
		then
			# Ubuntu에 python3-pip 설치
			apt-get update -y
			apt-get install -y python3-pip
		elif [ $OS = 'centos' ];
		then
			# centos에 python3-pip 설치
			curl https://bootstrap.pypa.io/pip/3.6/get-pip.py -o get-pip.py
			python3 get-pip.py
			rm get-pip.py
		fi
	fi
	pip3 install python-dateutil
fi
rm tmp

# 스크립트 실행
scripts=$(find . -name "*.py" | grep -E -w '^..[0-9]' | sort)
for py_file in $scripts
do
	python3 $py_file
done

echo -e "=================================================================" >> verbose