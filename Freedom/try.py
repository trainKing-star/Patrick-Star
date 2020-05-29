from Freedom import Freedom,Response,redirect
from globals import request,g,current_app,session
import redis
import os
app = Freedom()
app.set_static('upload')
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.way('/',methods=['GET','POST'])
def index():
    if 'username' in session:
        return redirect('/show')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password1')
        repassword = request.form.get('password2')
        if password==repassword:
            r.hset(username,'password',password)
            session['username']=username
            return redirect('/show')
        return redirect('/')
    return app.drawing_template('index.html')

@app.way('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect('/show')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password1')
        if r.hget(username,'password') is not None:
            ps = r.hget(username,'password')
            if ps == password:
                session['username']=username
                return redirect('/show')
            return redirect('/login')
        return redirect('/login')
    return app.drawing_template('login.html')

@app.way('/show',methods=['GET','POST'])
def show():
    if 'username' not in session:
        return redirect('/login')
    name = session['username']
    password = r.hget(name,'password')
    if request.method == 'POST':
        images  = request.files.getlist('images')
        for image in images:
            image.save(os.path.join(app.app_path, image.filename))
            r.sadd('images',image.filename)
        return redirect('/show')
    images = r.smembers('images')
    return app.drawing_template('show.html',name=name,password=password,images=images)

@app.way('/logout',methods=['GET'])
def logout():
    if 'username' in session:
        del session['username']
        print(session)
        return redirect('/login')
    return '未登录'

if __name__ =='__main__':
    app.fly(debug=True)