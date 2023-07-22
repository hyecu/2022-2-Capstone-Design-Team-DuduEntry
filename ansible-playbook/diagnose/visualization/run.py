import os
import sys

temp = sys.stdout
flask_path="/home/ansible/flask/main"
html_files = os.popen("find "+flask_path+"/templates/ -type f").read().splitlines()

sys.stdout = open(flask_path+"/main.py", 'w')
print("from flask import Flask, render_template, redirect")
print("")
print("app = Flask(__name__)")
print("")
for i in range(0, len(html_files)):
    filename = html_files[i].split('/')[-1]
    host = '.'.join(filename.split('.')[:-1])
    
    print("@app.route('/"+host+"')")
    print("def host{}():".format(i))
    print("    return render_template('"+filename+"')")
    print("")

print("@app.route('/')")
print("def index():")
print("    return redirect('https://duduentry.creatorlink.net/')")
print("")

print("if __name__ == '__main__':")
print("    app.run(host='0.0.0.0', port=9999, debug=True)")
sys.stdout = temp
os.popen("python3 "+flask_path+"/main.py").read()
