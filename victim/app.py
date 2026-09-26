from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = ""
    if request.method == 'POST':
        name = request.form.get('user_input', '')
    
    resp = make_response(render_template('index.html', name=name))
    
    # كوكيز وهمية للعرض التعليمي
    resp.set_cookie('session_id', 'FAKE_SESSION_ABC123XYZ')
    resp.set_cookie('user_role', 'admin')
    resp.set_cookie('username', 'victim_user')
    
    return resp

if __name__ == '__main__':
    print("[*] 🎯 Victim Lab شغال على http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)
