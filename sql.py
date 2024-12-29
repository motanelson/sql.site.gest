from flask import Flask, request, jsonify, render_template_string, make_response

import sqlite3

app = Flask(__name__)

db_file = 'datas.db'

# Função para inicializar a base de dados
def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa a base de dados ao iniciar o servidor
init_db()

# HTML base
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation System</title>
    <style>
        body {
            background-color:#ffff00;
            color:#ffffff';
            font-family: Arial, sans-serif;
            margin: 20px;
            text-align: center;
        }
        .content {
            background-color:#ffff00;
            color:#ffffff';
            border: 1px solid black;
            padding: 10px;
            min-height: 100px;
            margin-bottom: 20px;
        }
        textarea {
            background-color:#fff000
            color:#ffffff';
            width: 80%;
            height: 100px;
        }
    </style>
    
</head>
<body>
    <h1>Navigation System</h1>
    <div class="content" id="content">{{ No content available }}</div>
    
    <form action="/new" method="post">
        <textarea name="new_text" id="new_text"></textarea><br>
         
        <button type="button" onclick="txt=document.getElementById('new_text').value;document.getElementById('new_text').value =txt.replaceAll('\\n','#0');txt=txt.replaceAll('\\r','#1');txt=txt.replaceAll('<','#2');txt=txt.replaceAll('>','#3');txt=txt.replaceAll('=','#4'); this.form.submit()">New</button>
    </form>
    <form action="/starts" method="post">
     
        <button type="button" onclick="txt=this.form.submit()">&lt&lt</button>
    </form> 

<form action="/backs" method="post">
        
         
        <button type="button" onclick="txt=this.form.submit()">&lt</button>
    </form> 

<form action="/nexts" method="post">
        
         
        <button type="button" onclick="txt=this.form.submit()">&gt</button>
    </form> 
<form action="/ends" method="post">
        
         
        <button type="button" onclick="txt=this.form.submit()">&gt&gt</button>
    </form>    
</body>
</html>
"""

# Rota principal
@app.route('/')
def index():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM content')
    row = cursor.fetchone()

    spages = request.cookies.get('Pages')
    try:
        current_content = HTML_TEMPLATE
        if spages is None:
           pages = 0
        else:
           pages =int(spages)
        if pages > len(row)-1:
           pages = len(row)-1
        
    
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[pages]) 
    except:
        print("page error:")
        response=make_response(current_content)
        response.set_cookie('Pages', str(pages), max_age=60*60*24*365)  # Cookie válido por 1 ano
        return current_content

    for n in row:
        print(row)
    conn.close()
    return current_content

# Rota para adicionar novo conteúdo
@app.route('/new', methods=['POST'])
def new():
    raw_text = request.form.get('new_text', '')
    decoded_text = raw_text.replace('#0', '\n').replace('#1', '\r').replace('#2', '<').replace('#3', '>').replace('#4', '=')
    html_ready_text = decoded_text.replace('\n', '<br>').replace('\r', '<br>')
    html_ready_text = html_ready_text.strip()
    if  html_ready_text !="":
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            print(html_ready_text)
            cursor.execute('INSERT INTO content (text) VALUES (?)', (html_ready_text,))
            conn.commit()
            conn.close()
        except:
            print(f"Erro ao inserir no banco de dados:")
        finally:
            conn.close()
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM content')
    
    row = cursor.fetchone()

    
    
    pages = len(row)-1
    print(pages)
    current_content = HTML_TEMPLATE
    try:
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[pages]) 
    except:
        print("page error:")
    conn.commit()
    conn.close()
    response=make_response(current_content)
    response.set_cookie('Pages', str(pages), max_age=60*60*24*365)  # Cookie válido por 1 ano
    return current_content

@app.route('/nexts', methods=['POST'])
def nexts():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM content')
    row = cursor.fetchone()

    spages = request.cookies.get('Pages')
    if spages is None:
        pages = 0
    else:
        pages =int(spages)+1
    if pages > len(row)-1:
        pages = len(row)-1
    current_content = HTML_TEMPLATE
    try:
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[pages]) 
    except:
        print("page error:")
    for n in row:
        print(row)
    conn.close()
    response=make_response(current_content)
    response.set_cookie('Pages', str(pages), max_age=60*60*24*365)  # Cookie válido por 1 ano
    return current_content
@app.route('/backs', methods=['POST'])
def backs():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM content')
    row = cursor.fetchone()

    spages = request.cookies.get('Pages')
    if spages is None:
        pages = 0
    else:
        pages =int(spages)-1
    if pages > len(row)-1:
        pages = len(row)-1
    if pages <0:
        pages = 0


    current_content = HTML_TEMPLATE
    try:
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[pages]) 
    except:
        print("page error:")
    for n in row:
        print(row)
    conn.close()
    response=make_response(current_content)
    response.set_cookie('Pages', str(pages), max_age=60*60*24*365)  # Cookie válido por 1 ano
    return current_content
@app.route('/starts', methods=['POST'])
def starts():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM content')
    row = cursor.fetchone()

    pages = 0
    
    current_content = HTML_TEMPLATE
    try:
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[pages]) 
    except:
        print("page error:")
    for n in row:
        print(row)
    conn.close()
    response=make_response(current_content)
    response.set_cookie('Pages', str(pages), max_age=60*60*24*365)  # Cookie válido por 1 ano
    return current_content

@app.route('/ends', methods=['POST'])
def ends():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM content')
    row = cursor.fetchone()

    pages = len(row)-1
    
    current_content = HTML_TEMPLATE
    try:
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[pages]) 
    except:
        print("page error:")
    for n in row:
        print(row)
    conn.close()
    response=make_response(current_content)
    response.set_cookie('Pages', str(pages), max_age=60*60*24*365)  # Cookie válido por 1 ano
    return current_content

if __name__ == '__main__':
    app.run(debug=True)

