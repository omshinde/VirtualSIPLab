from flask import Flask, render_template, request, make_response, send_from_directory
from werkzeug import secure_filename, datastructures
import os
import Core
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'C:\Users\Ankur\Documents\MATLAB\VSIP Lab\PyDevelop\Code\VirtualSIP\Data'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/uploader', methods=['GET','POST'])
def uploader():
    print "i am in upload if"
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        for file_handle in files:
            if file_handle:
                print file_handle.filename
                fileExt=re.findall('[.]\S+', file_handle.filename)[0]
                print fileExt
                if fileExt=='.img':
                    fname=file_handle.filename #check by javascript that one file is hdr and one file is valid satellite image                    
                filename = secure_filename(file_handle.filename)
                fpath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_handle.save(fpath)
        print "name",fname
        print "path",fpath
        return render_template('exp1.html',fname=fname)
    else:
        print "i am in upload else function"
        return render_template('upload.html')   

@app.route('/display/<fname>')
def display(fname):
    print "i am in display"
    fileExt=re.findall('[.]\S+', fname)[0]
    fpath=UPLOAD_FOLDER+"\\"+fname
    newName=fname
    if fileExt!='.jpg' and fileExt!='jpeg' and fileExt!='gif' and fileExt!='bmp':
        fname=Core.convert(UPLOAD_FOLDER,fname,newName,'jpg')
            
    return send_from_directory(UPLOAD_FOLDER, fname)

@app.route('/log/<fname>')
def log(fname):
    print "i am in log"
    path=UPLOAD_FOLDER+"\\"+fname
    print(path)
    newName=Core.Imagelog(path)
    return render_template('result.html',fname=newName)

if __name__ == '__main__':
   app.run(debug = True)