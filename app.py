import os
from flask import Flask, Response, request, session, redirect

from gerador import gerar_html
from csv_parser import parse_csv, parse_csv_baixados

app = Flask(__name__)
app.secret_key = 'ls-bi-2026-xk9'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

LOGIN_USER = 'logussul'
LOGIN_PASS = 'varlog'

LOGIN_PAGE = '''<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Logus Sul BI — Login</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0c0c0c;color:#e5e7eb;font-family:"Segoe UI",Arial,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:#0d0800;border:2px solid #ea580c;border-radius:12px;padding:36px 40px;width:100%;max-width:380px}
.logo{color:#f97316;font-size:28px;font-weight:900;letter-spacing:-1px;margin-bottom:4px}
.sub{color:#6b4c30;font-size:12px;margin-bottom:28px}
label{display:block;color:#9ca3af;font-size:11px;font-weight:700;letter-spacing:.8px;margin-bottom:6px;margin-top:18px}
input{width:100%;padding:11px 14px;background:#080500;border:1px solid #2a1800;border-radius:6px;color:#e5e7eb;font-size:13px;outline:none;transition:border-color .2s}
input:focus{border-color:#ea580c}
.btn{display:block;width:100%;margin-top:24px;padding:13px;background:#ea580c;color:#fff;font-size:14px;font-weight:900;border:none;border-radius:8px;cursor:pointer;transition:background .2s}
.btn:hover{background:#f97316}
.err{background:#1a0000;border:1px solid #ef4444;color:#f87171;border-radius:6px;padding:10px 14px;font-size:12px;margin-bottom:16px}
</style></head><body>
<div class="card">
  <div style="text-align:center;margin-bottom:20px"><img src="/static/logo.png" style="height:80px;background:#fff;border-radius:10px;padding:8px 16px"></div>
  <div class="sub" style="text-align:center">Painel de Chamados — Regional Sul &amp; Centro Oeste</div>
  {error}
  <form method="POST" action="/login">
    <label>USUÁRIO</label>
    <input type="text" name="usuario" autocomplete="username" autofocus>
    <label>SENHA</label>
    <input type="password" name="senha" autocomplete="current-password">
    <button class="btn" type="submit">Entrar</button>
  </form>
</div>
</body></html>'''

UPLOAD_PAGE = '''<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Logus Sul BI — Upload</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0c0c0c;color:#e5e7eb;font-family:"Segoe UI",Arial,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:#0d0800;border:2px solid #ea580c;border-radius:12px;padding:36px 40px;width:100%;max-width:520px}
.logo{color:#f97316;font-size:28px;font-weight:900;letter-spacing:-1px;margin-bottom:4px}
.sub{color:#6b4c30;font-size:12px;margin-bottom:28px}
label{display:block;color:#9ca3af;font-size:11px;font-weight:700;letter-spacing:.8px;margin-bottom:6px;margin-top:18px}
.drop{border:2px dashed #2a1800;border-radius:8px;padding:20px;text-align:center;cursor:pointer;transition:border-color .2s;position:relative}
.drop:hover,.drop.over{border-color:#f97316;background:#100700}
.drop input[type=file]{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.drop .icon{font-size:28px;margin-bottom:6px}
.drop .hint{color:#6b4c30;font-size:11px}
.drop .fname{color:#f97316;font-size:12px;font-weight:700;margin-top:4px;display:none}
.btn{display:block;width:100%;margin-top:28px;padding:14px;background:#ea580c;color:#fff;font-size:14px;font-weight:900;border:none;border-radius:8px;cursor:pointer;letter-spacing:.5px;transition:background .2s}
.btn:hover{background:#f97316}
.btn:disabled{background:#2a1800;color:#6b4c30;cursor:not-allowed}
.tip{color:#374151;font-size:10px;margin-top:10px;line-height:1.5}
.err{background:#1a0000;border:1px solid #ef4444;color:#f87171;border-radius:6px;padding:10px 14px;font-size:12px;margin-bottom:16px}
.sair{float:right;color:#6b4c30;font-size:10px;text-decoration:none;margin-top:4px}
.sair:hover{color:#f97316}
</style></head><body>
<div class="card">
  <div style="text-align:center;margin-bottom:14px"><img src="/static/logo.png" style="height:70px;background:#fff;border-radius:10px;padding:6px 14px"></div>
  <div class="sub" style="text-align:center">Painel de Chamados — Regional Sul &amp; Centro Oeste <a href="/sair" class="sair">Sair</a></div>
  {error}
  <form method="POST" action="/gerar" enctype="multipart/form-data" id="form">
    <label>CSV PRINCIPAL — Chamados Abertos *</label>
    <div class="drop" id="drop1">
      <input type="file" name="csv_main" accept=".csv" required onchange="setName(this,'n1')">
      <div class="icon">📋</div>
      <div class="hint">Arraste ou clique — ex: <em>Logus Retail-16_06_2026.csv</em></div>
      <div class="fname" id="n1"></div>
    </div>
    <label>CSV BAIXADOS — Resolvidos Hoje <span style="color:#374151;font-weight:400">(opcional)</span></label>
    <div class="drop" id="drop2">
      <input type="file" name="csv_baixados" accept=".csv" onchange="setName(this,'n2')">
      <div class="icon">📤</div>
      <div class="hint">Arraste ou clique — ex: <em>Logus Retail-16_06_2026 (2).csv</em></div>
      <div class="fname" id="n2"></div>
    </div>
    <button class="btn" type="submit" id="btn">🚀 Gerar Painel</button>
    <div class="tip">O painel abre diretamente no navegador. Você pode salvar a página (Ctrl+S) para ter uma cópia local.</div>
  </form>
</div>
<script>
function setName(inp,id){
  var n=document.getElementById(id);
  if(inp.files&&inp.files[0]){n.textContent='✓ '+inp.files[0].name;n.style.display='block';}
}
document.getElementById('form').addEventListener('submit',function(){
  var b=document.getElementById('btn');b.disabled=true;b.textContent='⏳ Gerando...';
});
['drop1','drop2'].forEach(function(id){
  var el=document.getElementById(id);
  el.addEventListener('dragover',function(e){e.preventDefault();el.classList.add('over');});
  el.addEventListener('dragleave',function(){el.classList.remove('over');});
  el.addEventListener('drop',function(){el.classList.remove('over');});
});
</script></body></html>'''

def logado():
    return session.get('auth') == True

@app.route('/')
def index():
    if not logado():
        return redirect('/login')
    return Response(UPLOAD_PAGE.replace('{error}', ''), mimetype='text/html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('usuario', '').strip()
        s = request.form.get('senha', '').strip()
        if u == LOGIN_USER and s == LOGIN_PASS:
            session['auth'] = True
            return redirect('/')
        err = '<div class="err">⚠ Usuário ou senha incorretos.</div>'
        return Response(LOGIN_PAGE.replace('{error}', err), mimetype='text/html', status=401)
    return Response(LOGIN_PAGE.replace('{error}', ''), mimetype='text/html')

@app.route('/sair')
def sair():
    session.clear()
    return redirect('/login')

@app.route('/gerar', methods=['POST'])
def gerar():
    if not logado():
        return redirect('/login')

    f_main = request.files.get('csv_main')
    if not f_main or not f_main.filename:
        err = '<div class="err">⚠ Selecione o CSV principal antes de continuar.</div>'
        return Response(UPLOAD_PAGE.replace('{error}', err), mimetype='text/html', status=400)

    try:
        all_tks = parse_csv(f_main.read())
    except Exception as e:
        err = f'<div class="err">⚠ Erro ao ler CSV principal: {e}</div>'
        return Response(UPLOAD_PAGE.replace('{error}', err), mimetype='text/html', status=400)

    baixados = []
    f_bx = request.files.get('csv_baixados')
    if f_bx and f_bx.filename:
        try:
            baixados = parse_csv_baixados(f_bx.read())
        except Exception:
            pass

    try:
        html = gerar_html(all_tks, baixados)
    except Exception as e:
        err = f'<div class="err">⚠ Erro ao gerar painel: {e}</div>'
        return Response(UPLOAD_PAGE.replace('{error}', err), mimetype='text/html', status=500)

    return Response(html, mimetype='text/html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
