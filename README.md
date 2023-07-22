# capstone
2022-2 Capstone Design Team DuduEntry

Ansible을 활용한 컨테이너 기반 클라우드 취약점 진단 도구 개발
![최종구성도](https://github.com/hyecu/capstone/assets/137482878/f057e8cf-dc96-4d99-b2fd-ce81c503ec8f)

플레이북 실행 시

scripts 파일은 remote 서버에서 (192.168.16.36) ansible 서버(이하 현재 서버)로 가져옵니다.
scripts.tar.gz 파일은 현재 서버의 /tmp/ 디렉토리 아래에 저장됩니다.
참고

ansible-playbook/diagnose/ready.yml 파일은 플레이북 재실행시 사전 준비 작업 파일입니다.
ansible-playbook/diagnose/visualization/ready.sh 파일은 플레이북 내 시각화 자료 재생성시 사전 준비 작업 파일입니다.
ansible-playbook/diagnose/diagnose.yml 파일은 메인 플레이북 파일입니다.
ansible-playbook/diagnose/kubernetes_diagnose.yml, ansible-playbook/diagnose/podman_diagnose.yml 파일은 메인 플레이북 파일로 실행되는 서브 플레이북 파일입니다.
ansible-playbook/diagnose/hosts.yml 파일에서 진단 대상 시스템을 정의할 수 있습니다.
