import os
from datetime import datetime, timezone, timedelta

def _agora_brt():
    return datetime.now(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M')
from flask import Flask, Response, request, session, redirect

from gerador import gerar_html
from csv_parser import parse_csv, parse_csv_baixados
from excel_parser import parse_excel

app = Flask(__name__)
app.secret_key = 'ls-bi-2026-xk9'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

ADMIN_USER  = 'logussul'
ADMIN_PASS  = 'varlog'
VIEWER_USER = 'varejus'
VIEWER_PASS = 'varlog'
API_TOKEN   = 'ls-sul-pub-2026'

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

UPLOAD_PAGE = """<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Logus Sul BI — Atualizar</title>
<link rel="icon" href="/static/favicon.ico">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0c0c0c;color:#e5e7eb;font-family:"Segoe UI",Arial,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px}
.card{background:#0d0800;border:2px solid #ea580c;border-radius:14px;padding:32px 36px;width:100%;max-width:600px}
.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px}
.sair{color:#6b4c30;font-size:11px;text-decoration:none}.sair:hover{color:#f97316}
.ver{color:#22c55e;font-size:11px;text-decoration:none;margin-right:12px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.slot{border-radius:10px;padding:18px 14px;text-align:center;cursor:pointer;position:relative;transition:border-color .2s,background .2s}
.slot input[type=file]{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.slot .ico{font-size:28px;margin-bottom:8px}
.slot .lbl{font-size:11px;font-weight:900;letter-spacing:.8px;margin-bottom:5px}
.slot .hint{font-size:10px;opacity:.5;line-height:1.5}
.slot .fname{font-size:11px;font-weight:700;margin-top:8px;display:none;word-break:break-all}
.badge{display:inline-block;font-size:9px;font-weight:900;border-radius:4px;padding:2px 6px;margin-left:5px;vertical-align:middle}
.req{background:#ef444422;color:#ef4444;border:1px solid #ef444466}
.opt{background:#37415122;color:#6b7280;border:1px solid #37415166}
.slot-urg{border:2px dashed #ef444455;background:#0f0000}
.slot-urg:hover,.slot-urg.over{border-color:#ef4444;background:#1a0000}
.slot-urg .lbl,.slot-urg .fname{color:#ef4444}
.slot-main{border:2px dashed #f9731655;background:#0a0500}
.slot-main:hover,.slot-main.over{border-color:#f97316;background:#120800}
.slot-main .lbl,.slot-main .fname{color:#f97316}
.slot-bx{border:2px dashed #22c55e55;background:#000f05}
.slot-bx:hover,.slot-bx.over{border-color:#22c55e;background:#001a08}
.slot-bx .lbl,.slot-bx .fname{color:#22c55e}
.btn{display:block;width:100%;margin-top:20px;padding:15px;background:#ea580c;color:#fff;font-size:14px;font-weight:900;border:none;border-radius:10px;cursor:pointer;letter-spacing:.5px;transition:background .2s}
.btn:hover{background:#f97316}.btn:disabled{background:#2a1800;color:#6b4c30;cursor:not-allowed}
.tip{color:#374151;font-size:10px;margin-top:12px;line-height:1.7}
.err{background:#1a0000;border:1px solid #ef4444;color:#f87171;border-radius:8px;padding:10px 14px;font-size:12px;margin-bottom:14px}
.ok{background:#052e16;border:1px solid #22c55e;color:#4ade80;border-radius:8px;padding:10px 14px;font-size:12px;margin-bottom:14px}
</style></head><body>
<div class="card">
  <div class="top">
    <img src="/static/logo.png" style="height:46px;background:#fff;border-radius:8px;padding:4px 10px">
    <div><a href="/" class="ver">Ver painel →</a><a href="/admin/sair" class="sair">Sair</a></div>
  </div>
  {ultimo}
  {error}
  <form method="POST" action="/admin/gerar" enctype="multipart/form-data" id="form">
    <div class="grid2">
      <div class="slot slot-urg" id="drop1">
        <input type="file" name="csv_urg" accept=".csv" onchange="setName(this,'n1')">
        <div class="ico">🚨</div>
        <div class="lbl">URGENTES <span class="badge opt">opcional</span></div>
        <div class="hint">Filtre Prioridade = <strong>Urgente</strong> no Tolvdesk e exporte</div>
        <div class="fname" id="n1"></div>
      </div>
      <div class="slot slot-main" id="drop2">
        <input type="file" name="csv_main" accept=".csv,.xlsx" required onchange="setName(this,'n2')">
        <div class="ico">📋</div>
        <div class="lbl">ABERTOS / EXCEL <span class="badge req">obrigatório</span></div>
        <div class="hint">CSV de abertos <strong>ou</strong> Excel completo do Tolvdesk<br>(Excel já traz baixados automaticamente)</div>
        <div class="fname" id="n2"></div>
      </div>
    </div>
    <div class="slot slot-bx" id="drop3" style="margin-bottom:4px">
      <input type="file" name="csv_baixados" accept=".csv" onchange="setName(this,'n3')">
      <div class="ico">📤</div>
      <div class="lbl">BAIXADOS DO DIA <span class="badge opt">opcional — só se usar CSV</span></div>
      <div class="hint">Não precisa se usar o Excel completo acima</div>
      <div class="fname" id="n3"></div>
    </div>
    <button class="btn" type="submit" id="btn">🚀 Publicar Painel</button>
    <div class="tip">
      <strong style="color:#6b7280">Modo Excel (recomendado):</strong><br>
      1. No Tolvdesk clique em <strong>Exportar tickets</strong> → baixa o Excel completo<br>
      2. Sobe o Excel no campo ABERTOS/EXCEL acima<br>
      3. Baixados do dia são detectados automaticamente<br><br>
      <strong style="color:#6b7280">Modo CSV (antigo):</strong> sobe os 3 CSVs separados como antes
    </div>
  </form>
</div>
<script>
function setName(inp,id){var n=document.getElementById(id);if(inp.files&&inp.files[0]){n.textContent="OK "+inp.files[0].name;n.style.display="block";}}
document.getElementById("form").addEventListener("submit",function(){var b=document.getElementById("btn");b.disabled=true;b.textContent="Publicando...";});
["drop1","drop2","drop3"].forEach(function(id){var el=document.getElementById(id);
el.addEventListener("dragover",function(e){e.preventDefault();el.classList.add("over");});
el.addEventListener("dragleave",function(){el.classList.remove("over");});
el.addEventListener("drop",function(){el.classList.remove("over");});});
</script></body></html>"""

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
        err = '<div class="err">&#9888; Usuário ou senha incorretos.</div>'
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
        ultimo = f'<div class="ok">&#10003; Último painel publicado às {_painel["gerado_em"]}</div>'
    return Response(UPLOAD_PAGE.replace('{error}', '').replace('{ultimo}', ultimo), mimetype='text/html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        u = request.form.get('usuario', '').strip()
        s = request.form.get('senha', '').strip()
        if u == ADMIN_USER and s == ADMIN_PASS:
            session['admin'] = True
            return redirect('/admin')
        err = '<div class="err">&#9888; Usuário ou senha incorretos.</div>'
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
        err = '<div class="err">&#9888; Selecione o CSV de Abertos antes de continuar.</div>'
        ultimo = f'<div class="ok">&#10003; Último painel publicado às {_painel["gerado_em"]}</div>' if _painel['gerado_em'] else ''
        return Response(UPLOAD_PAGE.replace('{error}', err).replace('{ultimo}', ultimo), mimetype='text/html', status=400)

    fname = f_main.filename.lower()
    conteudo = f_main.read()
    baixados_excel = []

    try:
        if fname.endswith('.xlsx'):
            main_tks, baixados_excel = parse_excel(conteudo)
        else:
            main_tks = parse_csv(conteudo)
    except Exception as e:
        err = f'<div class="err">&#9888; Erro ao ler arquivo: {e}</div>'
        ultimo = f'<div class="ok">&#10003; Último painel publicado às {_painel["gerado_em"]}</div>' if _painel['gerado_em'] else ''
        return Response(UPLOAD_PAGE.replace('{error}', err).replace('{ultimo}', ultimo), mimetype='text/html', status=400)

    # CSV Urgentes (opcional)
    urg_tks = []
    f_urg = request.files.get('csv_urg')
    if f_urg and f_urg.filename:
        try:
            urg_tks = parse_csv(f_urg.read())
        except Exception:
            pass

    # CSV Baixados (opcional) — ignorado se Excel já trouxe baixados
    baixados = baixados_excel
    if not baixados:
        f_bx = request.files.get('csv_baixados')
        if f_bx and f_bx.filename:
            try:
                baixados = parse_csv_baixados(f_bx.read())
            except Exception:
                pass

    try:
        html = gerar_html(main_tks, baixados, urg_tks=urg_tks)
    except Exception as e:
        err = f'<div class="err">&#9888; Erro ao gerar painel: {e}</div>'
        ultimo = f'<div class="ok">&#10003; Último painel publicado às {_painel["gerado_em"]}</div>' if _painel['gerado_em'] else ''
        return Response(UPLOAD_PAGE.replace('{error}', err).replace('{ultimo}', ultimo), mimetype='text/html', status=500)

    _painel['html'] = html
    _painel['gerado_em'] = _agora_brt()
    return redirect('/admin')

@app.route('/api/publicar', methods=['POST'])
def api_publicar():
    token = request.form.get('token') or request.headers.get('X-Token', '')
    if token != API_TOKEN:
        return Response('{"erro":"token invalido"}', status=401, mimetype='application/json')

    f_main = request.files.get('csv_main')
    if not f_main or not f_main.filename:
        return Response('{"erro":"arquivo principal obrigatorio"}', status=400, mimetype='application/json')

    fname = f_main.filename.lower()
    conteudo = f_main.read()
    baixados_excel = []

    try:
        if fname.endswith('.xlsx'):
            main_tks, baixados_excel = parse_excel(conteudo)
        else:
            main_tks = parse_csv(conteudo)
    except Exception as e:
        return Response(f'{{"erro":"erro ao ler arquivo: {e}"}}', status=400, mimetype='application/json')

    urg_tks = []
    f_urg = request.files.get('csv_urg')
    if f_urg and f_urg.filename:
        try:
            urg_tks = parse_csv(f_urg.read())
        except Exception:
            pass

    baixados = baixados_excel
    if not baixados:
        f_bx = request.files.get('csv_baixados')
        if f_bx and f_bx.filename:
            try:
                baixados = parse_csv_baixados(f_bx.read())
            except Exception:
                pass

    try:
        html = gerar_html(main_tks, baixados, urg_tks=urg_tks)
    except Exception as e:
        return Response(f'{{"erro":"erro ao gerar painel: {e}"}}', status=500, mimetype='application/json')

    _painel['html'] = html
    _painel['gerado_em'] = _agora_brt()
    return Response(
        f'{{"ok":true,"gerado_em":"{_painel["gerado_em"]}","chamados":{len(main_tks)},"urgentes":{len(urg_tks)},"baixados":{len(baixados)}}}',
        mimetype='application/json'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
