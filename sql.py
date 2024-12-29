from flask import Flask, request, jsonify, render_template_string, make_response
import os
import sqlite3
global counters 
counters=0
app = Flask(__name__)
# Nome do arquivo para salvar o contador
counter_file = 'count.txt'
db_file = 'data.db'
# Função para salvar o contador no arquivo
def save_counter(count):
    with open(counter_file, 'w') as file:
        file.write(str(count))

def load_counter():
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as file:
            try:
                ttt=file.read().strip()
                
                return int(ttt)
            except ValueError:
                return 0
    return 0

# Função para inicializar a base de dados
def init_db():
    global counters
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

    counters=load_counter()
    print(counters)
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
    pages =0
    try:
        spages = request.cookies.get('Pages')
        
        current_content = HTML_TEMPLATE
        if spages is None:
           pages = 0
        else:
           pages =int(spages)
        if pages > counters-1:
           pages = counters-1
        print(pages)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT  text FROM content where id='+str(pages+1))
        row = cursor.fetchone()
        
        
    
        
        
        
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[0])
        
        response=make_response(current_content)
        response.set_cookie('Pages', pages, max_age=60*60*24*365)  # Cookie válido por 1 ano
        conn.close()
        return response
    except:
        print("page error:")
        response=make_response(current_content)
        response.set_cookie('Pages', str(0), max_age=60*60*24*365)  # Cookie válido por 1 ano
        return response
        try:
            conn.close()
        except:
            pass
        

  
    return ""



@app.route('/nexts', methods=['POST'])
def nexts():
    pages =0
    try:
        spages = request.cookies.get('Pages')
        current_content = HTML_TEMPLATE
        if spages is None:
           pages = 0
        else:
           pages =int(spages)+1
        if pages > counters-1:
           pages = counters-1
        if pages < 0:
           pages
        print(pages)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT  text FROM content where id='+str(pages+1))
        row = cursor.fetchone()

        
    
        
        
    
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[0]) 
        response=make_response(current_content)
        response.set_cookie('Pages', pages, max_age=60*60*24*365)  # Cookie válido por 1 ano
        conn.close()
        return response
    except:
        print("page error:")
        response=make_response(current_content)
        response.set_cookie('Pages', str(0), max_age=60*60*24*365)  # Cookie válido por 1 ano
        return response
        try:
            conn.close()
        except:
            pass

        return ""

  
    conn.close()
    response=make_response(current_content)
    response.set_cookie('Pages', str(Pages), max_age=60*60*24*365)  # Cookie válido por 1 ano
    return response
@app.route('/backs', methods=['POST'])
def backs():
    pages =0
    try:
        spages = request.cookies.get('Pages')
        current_content = HTML_TEMPLATE
        
        if spages is None:
           pages = 0
        else:
           pages =int(spages)-1
        if pages > counters-1:
           pages = counters-1
        if pages < 0:
           pages=0
        print(pages)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT  text FROM content where id='+str(pages+1))
        row = cursor.fetchone()

        
    
        
        
    
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[0]) 
        response=make_response(current_content)
        response.set_cookie('Pages', pages, max_age=60*60*24*365)  # Cookie válido por 1 ano
        conn.close()
        return response
    except:
        print("page error:")
        response=make_response(current_content)
        response.set_cookie('Pages', counters, max_age=60*60*24*365)  # Cookie válido por 1 ano
        return response
        try:
            conn.close()
        except:
            pass

        return ""

@app.route('/starts', methods=['POST'])
def starts():
    pages =0
    try:
        spages = request.cookies.get('Pages')
        current_content = HTML_TEMPLATE
        if spages is None:
           pages = 0
        else:
           pages =0
        if pages > counters-1:
           pages = counters-1
        if pages < 0:
           pages
        print(pages)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT  text FROM content where id='+str(pages+1))
        row = cursor.fetchone()

        
    
        
        
    
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[0])
        response=make_response(current_content)
        response.set_cookie('Pages', pages, max_age=60*60*24*365)  # Cookie válido por 1 ano
        conn.close()
        return response
    except:
        print("page error:")
        response=make_response(current_content)
        response.set_cookie('Pages', str(0), max_age=60*60*24*365)  # Cookie válido por 1 ano
        return response
        try:
            conn.close()
        except:
            pass

        return ""


@app.route('/ends', methods=['POST'])
def ends():
    pages =0
    try:
        spages = request.cookies.get('Pages')
        current_content = HTML_TEMPLATE
        if spages is None:
           pages = counters
        else:
           pages =int(spages)+1
        if pages > counters-1:
           pages = counters-1
        if pages < 0:
           pages
        print(pages)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT  text FROM content where id='+str(pages+1))
        row = cursor.fetchone()

        
    
        
        
    
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[0])
        response=make_response(current_content)
        response.set_cookie('Pages', pages, max_age=60*60*24*365)  # Cookie válido por 1 ano
        conn.close()
        return response
    except:
        print("page error:")
        response=make_response(current_content)
        response.set_cookie('Pages', str(0), max_age=60*60*24*365)  # Cookie válido por 1 ano
        return response
        try:
            conn.close()
        except:
            pass

        return current_content

# Rota para adicionar novo conteúdo
@app.route('/new', methods=['POST'])
def new():
    global counters 
    raw_text = request.form.get('new_text', '')
    
    decoded_text = raw_text.replace('#0', '<br>').replace('#1', '<br>').replace('#2', '<').replace('#3', '>').replace('#4', '=')
    
    html_ready_text = decoded_text.strip()
    if  html_ready_text !="":
        try:
            
            
            
            counters=counters+1
            
            save_counter(counters)
           
            conn = sqlite3.connect(db_file)
            
            cursor = conn.cursor()
            
            cursor.execute('INSERT INTO content (text) VALUES (?)', (html_ready_text,))
            
            conn.commit()
            conn.close()
        except:
            print(f"Erro ao inserir no banco de dados:")
        finally:
            try:
                conn.close()
            except:
                pass
    pages =0
    try:
       
        current_content = HTML_TEMPLATE
        if spages is None:
           pages = counters
        else:
           pages =int(spages)+1
        if pages > counters-1:
           pages = counters-1
        if pages < 0:
           pages
        print(pages)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT  text FROM content where id='+str(pages+1))
        row = cursor.fetchone()


    
        
        
    
        current_content = HTML_TEMPLATE.replace("{{ No content available }}",row[0]) 
        response=make_response(current_content)
        response.set_cookie('Pages', pages, max_age=60*60*24*365)  # Cookie válido por 1 ano
        conn.close()
        return response
    except:
        print("page error:")
        response=make_response(current_content)
        response.set_cookie('Pages', str(0), max_age=60*60*24*365)  # Cookie válido por 1 ano
        return response
        try:
            conn.close()
        except:
            pass

        return ""


if __name__ == '__main__':
    app.run(debug=True)

