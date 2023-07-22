#!/bin/bash

Absolute_path="/home/ansible/ansible-playbook/diagnose"
Flask_path="/home/ansible/flask/main/templates"
systems=$(ls $Absolute_path/result/)

for system in $systems
do
	rm -r $Absolute_path/result/$system/tmp 2>tmp
	cp $Absolute_path/result/$system/$system.html $Flask_path/ 2>tmp
done

if [ -e ./tmp ]; then rm tmp; fi
