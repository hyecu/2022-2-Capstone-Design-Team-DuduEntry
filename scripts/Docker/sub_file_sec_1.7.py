import os
os.popen("ausearch -k docker | grep exec | grep user").read()