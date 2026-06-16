import os
from datetime import datetime, timezone, timedelta

def _agora_brt():
    return datetime.now(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M')
from flask import Flask, Response, request, session, redirect

from gerador import gerar_html
from csv_parser import parse_csv, parse_csv_baixados

app = Flask(__name__)
app.secret_key = 'ls-bi-2026-xk9'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

ADMIN_USER  = 'logussul'
ADMIN_PASS  = 'varlog'
VIEWER_USER = 'varejus'
VIEWER_PASS = 'varlog'

# painel em memória — gerado pelo admin, visto pela equipe
_painel = {'html': None, 'gerado_em': None}

VIEWER_LOGIN_PAGE = '''<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Logus Sul BI</title>
<link rel="icon" href="/static/favicon.ico">
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#ea580c">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Sul BI">
<link rel="apple-touch-icon" href="/static/icon-192.png">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0c0c0c;color:#e5e7eb;font-family:"Segoe UI",Arial,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:#0d0800;border:2px solid #ea580c;border-radius:12px;padding:36px 40px;width:100%;max-width:360px}
label{display:block;color:#9ca3af;font-size:11px;font-weight:700;letter-spacing:.8px;margin-bottom:6px;margin-top:18px}
input{width:100%;padding:11px 14px;background:#080500;border:1px solid #2a1800;border-radius:6px;color:#e5e7eb;font-size:13px;outline:none;transition:border-color .2s}
input:focus{border-color:#ea580c}
.btn{display:block;width:100%;margin-top:24px;padding:13px;background:#ea580c;color:#fff;font-size:14px;font-weight:900;border:none;border-radius:8px;cursor:pointer;transition:background .2s}
.btn:hover{background:#f97316}
.err{background:#1a0000;border:1px solid #ef4444;color:#f87171;border-radius:6px;padding:10px 14px;font-size:12px;margin-bottom:16px}
.sub{color:#6b4c30;font-size:11px;text-align:center;margin-bottom:20px}
</style></head><body>
<div class="card">
  <div style="text-align:center;margin-bottom:16px"><img src="/static/logo.png" style="height:70px;background:#fff;border-radius:10px;padding:6px 14px"></div>
  <div class="sub">Painel de Chamados — Logus Sul</div>
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

AGUARDANDO_PAGE = '''<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="60">
<title>Logus Sul BI</title>
<link rel="icon" href="/static/favicon.ico">
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#ea580c">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Sul BI">
<link rel="apple-touch-icon" href="/static/icon-192.png">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0c0c0c;color:#e5e7eb;font-family:"Segoe UI",Arial,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:#0d0800;border:2px solid #ea580c;border-radius:12px;padding:40px;width:100%;max-width:420px;text-align:center}
.msg{color:#6b4c30;font-size:13px;margin-top:16px;line-height:1.7}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#ea580c;margin:0 3px;animation:pulse 1.4s ease-in-out infinite}
.dot:nth-child(2){animation-delay:.2s}.dot:nth-child(3){animation-delay:.4s}
@keyframes pulse{0%,100%{opacity:.2}50%{opacity:1}}
</style></head><body>
<div class="card">
  <img src="/static/logo.png" style="height:80px;background:#fff;border-radius:10px;padding:8px 16px;margin-bottom:20px">
  <div class="msg">Painel ainda não foi gerado hoje.<br>Aguarde o gestor atualizar os dados.<br><br>
  <span class="dot"></span><span class="dot"></span><span class="dot"></span><br><br>
  Esta página atualiza automaticamente.</div>
</div>
</body></html>'''

LOGIN_PAGE = '''<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Logus Sul BI — Admin</title>
<link rel="icon" href="/static/favicon.ico">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0c0c0c;color:#e5e7eb;font-family:"Segoe UI",Arial,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:#0d0800;border:2px solid #ea580c;border-radius:12px;padding:36px 40px;width:100%;max-width:380px}
label{display:block;color:#9ca3af;font-size:11px;font-weight:700;letter-spacing:.8px;margin-bottom:6px;margin-top:18px}
input{width:100%;padding:11px 14px;background:#080500;border:1px solid #2a1800;border-radius:6px;color:#e5e7eb;font-size:13px;outline:none;transition:border-color .2s}
input:focus{border-color:#ea580c}
.btn{display:block;width:100%;margin-top:24px;padding:13px;background:#ea580c;color:#fff;font-size:14px;font-weight:900;border:none;border-radius:8px;cursor:pointer;transition:background .2s}
.btn:hover{background:#f97316}
.err{background:#1a0000;border:1px solid #ef4444;color:#f87171;border-radius:6px;padding:10px 14px;font-size:12px;margin-bottom:16px}
.sub{color:#6b4c30;font-size:11px;text-align:center;margin-bottom:20px}
</style></head><body>
<div class="card">
  <div style="text-align:center;margin-bottom:16px"><img src="/static/logo.png" style="height:70px;background:#fff;border-radius:10px;padding:6px 14px"></div>
  <div class="sub">Área do Gestor</div>
  {error}
  <form method="POST" action="/admin/login">
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
<title>Logus Sul BI — Atualizar</title>
<link rel="icon" href="/static/favicon.ico">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0c0c0c;color:#e5e7eb;font-family:"Segoe UI",Arial,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:#0d0800;border:2px solid #ea580c;border-radius:12px;padding:36px 40px;width:100%;max-width:520px}
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
.ok{background:#052e16;border:1px solid #22c55e;color:#4ade80;border-radius:6px;padding:10px 14px;font-size:12px;margin-bottom:16px}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px}
.sair{color:#6b4c30;font-size:10px;text-decoration:none}
.sair:hover{color:#f97316}
.ver{color:#22c55e;font-size:10px;text-decoration:none;margin-right:10px}
</style></head><body>
<div class="card">
  <div class="top">
    <img src="/static/logo.png" style="height:50px;background:#fff;border-radius:8px;padding:4px 10px">
    <div><a href="/" class="ver">Ver painel →</a><a href="/admin/sair" class="sair">Sair</a></div>
  </div>
  {ultimo}
  {error}
  <form method="POST" action="/admin/gerar" enctype="multipart/form-data" id="form">
    <label>CSV PRINCIPAL — Chamados Abertos *</label>
    <div class="drop" id="drop1">
      <input type="file" name="csv_main" accept=".csv" required onchange="setName(this,'n1')">
      <div class="icon">📋</div>
      <div class="hint">ex: <em>Logus Retail-16_06_2026.csv</em></div>
      <div class="fname" id="n1"></div>
    </div>
    <label>CSV BAIXADOS — Chamados Resolvidos <span style="color:#374151;font-weight:400">(opcional)</span></label>
    <div class="drop" id="drop2">
      <input type="file" name="csv_baixados" accept=".csv" onchange="setName(this,'n2')">
      <div class="icon">📤</div>
      <div class="hint">ex: <em>Logus Retail-16_06_2026 (2).csv</em></div>
      <div class="fname" id="n2"></div>
    </div>
    <button class="btn" type="submit" id="btn">🚀 Publicar Painel</button>
    <div class="tip">Após publicar, toda a equipe verá o painel atualizado automaticamente.</div>
  </form>
</div>
<script>
function setName(inp,id){var n=document.getElementById(id);if(inp.files&&inp.files[0]){n.textContent='✓ '+inp.files[0].name;n.style.display='block';}}
document.getElementById('form').addEventListener('submit',function(){var b=document.getElementById('btn');b.disabled=true;b.textContent='⏳ Publicando...';});
['drop1','drop2'].forEach(function(id){var el=document.getElementById(id);
el.addEventListener('dragover',function(e){e.preventDefault();el.classList.add('over');});
el.addEventListener('dragleave',function(){el.classList.remove('over');});
el.addEventListener('drop',function(){el.classList.remove('over');});});
</script></body></html>'''

def admin_logado():
    return session.get('admin') == True

def viewer_logado():
    return session.get('viewer') == True or session.get('admin') == True

# ── rotas públicas ─────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def viewer_login():
    if request.method == 'POST':
        u = request.form.get('usuario', '').strip()
        s = request.form.get('senha', '').strip()
        if u == VIEWER_USER and s == VIEWER_PASS:
            session['viewer'] = True
            return redirect('/')
        if u == ADMIN_USER and s == ADMIN_PASS:
            session['admin'] = True
            return redirect('/admin')
        err = '<div class="err">⚠ Usuário ou senha incorretos.</div>'
        return Response(VIEWER_LOGIN_PAGE.replace('{error}', err), mimetype='text/html', status=401)
    return Response(VIEWER_LOGIN_PAGE.replace('{error}', ''), mimetype='text/html')

@app.route('/sair')
def viewer_sair():
    session.pop('viewer', None)
    return redirect('/login')

@app.route('/')
def index():
    if not viewer_logado():
        return redirect('/login')
    if _painel['html']:
        return Response(_painel['html'], mimetype='text/html')
    return Response(AGUARDANDO_PAGE, mimetype='text/html')

# ── rotas admin ────────────────────────────────────────────────────────────────
@app.route('/admin')
def admin():
    if not admin_logado():
        return redirect('/admin/login')
    ultimo = ''
    if _painel['gerado_em']:
        ultimo = f'<div class="ok">✓ Último painel publicado às {_painel["gerado_em"]}</div>'
    return Response(UPLOAD_PAGE.replace('{error}', '').replace('{ultimo}', ultimo), mimetype='text/html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        u = request.form.get('usuario', '').strip()
        s = request.form.get('senha', '').strip()
        if u == ADMIN_USER and s == ADMIN_PASS:
            session['admin'] = True
            return redirect('/admin')
        err = '<div class="err">⚠ Usuário ou senha incorretos.</div>'
        return Response(LOGIN_PAGE.replace('{error}', err), mimetype='text/html', status=401)
    return Response(LOGIN_PAGE.replace('{error}', ''), mimetype='text/html')

@app.route('/admin/sair')
def admin_sair():
    session.clear()
    return redirect('/admin/login')

@app.route('/admin/gerar', methods=['POST'])
def admin_gerar():
    if not admin_logado():
        return redirect('/admin/login')

    f_main = request.files.get('csv_main')
    if not f_main or not f_main.filename:
        err = '<div class="err">⚠ Selecione o CSV principal antes de continuar.</div>'
        ultimo = f'<div class="ok">✓ Último painel publicado às {_painel["gerado_em"]}</div>' if _painel['gerado_em'] else ''
        return Response(UPLOAD_PAGE.replace('{error}', err).replace('{ultimo}', ultimo), mimetype='text/html', status=400)

    try:
        all_tks = parse_csv(f_main.read())
    except Exception as e:
        err = f'<div class="err">⚠ Erro ao ler CSV: {e}</div>'
        ultimo = f'<div class="ok">✓ Último painel publicado às {_painel["gerado_em"]}</div>' if _painel['gerado_em'] else ''
        return Response(UPLOAD_PAGE.replace('{error}', err).replace('{ultimo}', ultimo), mimetype='text/html', status=400)

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
        ultimo = f'<div class="ok">✓ Último painel publicado às {_painel["gerado_em"]}</div>' if _painel['gerado_em'] else ''
        return Response(UPLOAD_PAGE.replace('{error}', err).replace('{ultimo}', ultimo), mimetype='text/html', status=500)

    _painel['html'] = html
    _painel['gerado_em'] = _agora_brt()
    return redirect('/admin')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
