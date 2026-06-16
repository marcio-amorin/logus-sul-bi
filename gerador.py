from datetime import date
from collections import defaultdict

SUL_EMP = {
    'GUMZ','MERCADO DE BEBIDA POP','MILANI','PARANA SUPERMERCADO',
    'MAIS BRASIL - VAREJUS','MAIS BRASIL - MMR','CASA DE CARNES PETRY',
    'VICARI','MERCADO LEAL','SUPER PRINCESA','YPE SUPERMERCADO',
    'SUPERMERCADO KAIO','BECKER','TILL DA CARNE','ANGELINA SUPERMERCADO',
    'SUPERMERCADO MATHEUS','Supermercado Matheus','SCHUTZE','ANGELINO',
}
SUL_RESP = {'Henrique Wolfram','Carlos Viana','Marcio Amorin','Rafael Beckert','— Sem Responsável —'}
SUL_TEAM = {'Henrique Wolfram','Rafael Beckert'}
PATCHES = {
    '25267': {'atrib':'Desenv. PDV',        'status':'Em andamento'},
    '25232': {'atrib':'Vitor Silva',         'status':'Novo'},
    '4255':  {'atrib':'Engenharia Software', 'status':'Aguardando'},
    '8264':  {'atrib':'Engenharia Software', 'status':'Em andamento'},
    '24621': {'atrib':'Rafael Beckert',      'status':'Aguardando'},
    '24760': {'atrib':'Carlos Viana',        'status':'Aguardando'},
    '20174': {'atrib':'Comercial',           'status':'Aguardando'},
    '21028': {'atrib':'Comercial',           'status':'Em andamento'},
}
URG_PDV  = {'25596','25090','24651'}
URG_ERP  = {'25628','25647','25648','23301','24846','25173'}
URG_DEV  = {'24760','24621','25368'}
URG_ALL  = URG_PDV | URG_ERP | URG_DEV
RESP_OWN = {'Comercial','Engenharia Software','Desenv. PDV','Sust. Desenv.','Sustentação Desenv.'}
BACKLOG = [{'num': 1, 'ticket': '21979', 'cliente': 'YPÊ', 'desc': 'Emissão de MDF-e', 'est': '16/03', 'status': 'Homologado'}, {'num': 2, 'ticket': '22206', 'cliente': 'YPÊ', 'desc': 'Emissão de NF para CPF com IE', 'est': '16/03', 'status': 'Homologado'}, {'num': 3, 'ticket': '12752', 'cliente': 'LEAL', 'desc': 'Adequação NT 2023.004', 'est': '31/03', 'status': 'Homologado'}, {'num': 4, 'ticket': '6197', 'cliente': 'VICARI', 'desc': 'Parametrização Custo no Balanço Comercial', 'est': '22/04', 'status': 'Em Homologação'}, {'num': 5, 'ticket': '24348', 'cliente': 'GUMZ JARAGUA', 'desc': 'Prazo de pagamento diferenciado por cliente', 'est': '04/05', 'status': 'Homologado'}, {'num': 6, 'ticket': '16783', 'cliente': 'LEAL', 'desc': 'Número do Pedido de Compras em Campo Específico', 'est': '05/05', 'status': 'Em Homologação'}, {'num': 7, 'ticket': '24705', 'cliente': 'LEAL', 'desc': 'ICMS ST retido no cálculo ICMS próprio', 'est': '11/05', 'status': 'Homologado'}, {'num': 8, 'ticket': '24839', 'cliente': 'GUMZ POMERODE', 'desc': 'Trazer produtos ativos por filial na pesquisa', 'est': '19/05', 'status': 'Homologado'}, {'num': 9, 'ticket': '17727', 'cliente': 'GUMZ JARAGUA', 'desc': 'Desconto em Forma de Recebimento', 'est': '14/05', 'status': 'Em Homologação'}, {'num': 10, 'ticket': '11753', 'cliente': 'GUMZ JARAGUA', 'desc': 'Relatório Contas a Receber', 'est': '25/05', 'status': 'Em Homologação'}, {'num': 11, 'ticket': '10223', 'cliente': 'ANGELINO', 'desc': 'Juros Acréscimo não lista na Manutenção de Recebimentos', 'est': '25/05', 'status': 'Em Homologação'}, {'num': 12, 'ticket': '16761', 'cliente': 'SCHUTZE', 'desc': 'Exibir dados históricos no pedido automático', 'est': '03/06', 'status': 'Em Homologação'}, {'num': 13, 'ticket': '12755', 'cliente': 'VICARI', 'desc': 'Crédito de Diferimento - Apuração e Preço de Venda', 'est': '24/07', 'status': 'Em Roadmap'}, {'num': 14, 'ticket': '16219', 'cliente': 'LEAL', 'desc': 'SPED FISCAL - Ajuste de Crédito', 'est': '24/07', 'status': 'Em Roadmap'}, {'num': 15, 'ticket': '6497', 'cliente': 'VICARI', 'desc': 'Baixas Uso/Consumo no Balanço Comercial', 'est': '03/07', 'status': 'Em Roadmap'}, {'num': 16, 'ticket': '20278', 'cliente': 'VICARI', 'desc': 'ICMS Desonerado na Entrada da NF', 'est': '04/09', 'status': 'Em Roadmap'}, {'num': 17, 'ticket': '20484', 'cliente': 'ANGELINO', 'desc': 'Campo Juros Baixa Recebimento', 'est': '', 'status': 'Pendente'}, {'num': 18, 'ticket': '4255', 'cliente': 'PRINCESA', 'desc': 'Troco Solidário', 'est': '', 'status': 'Pendente'}, {'num': 19, 'ticket': '6451', 'cliente': 'PRINCESA', 'desc': 'Emissão Notas Fiscais a partir do PDV', 'est': '', 'status': 'Pendente'}, {'num': 20, 'ticket': '16782', 'cliente': 'LEAL', 'desc': 'Venda a Órgão Público com Retenção do IRRF', 'est': '', 'status': 'Pendente'}, {'num': 21, 'ticket': '23172', 'cliente': 'LEAL', 'desc': 'Sistema não considerando ICMS desonerado', 'est': '', 'status': 'Pendente'}, {'num': 22, 'ticket': '22787', 'cliente': 'LEAL', 'desc': 'Erro ao finalizar NF (#1)', 'est': '', 'status': 'Pendente'}, {'num': 23, 'ticket': '23568', 'cliente': 'LEAL', 'desc': 'Erro ao finalizar NF (#2)', 'est': '', 'status': 'Pendente'}, {'num': 24, 'ticket': '19372', 'cliente': 'LEAL', 'desc': 'Venda para cliente fora do estado', 'est': '', 'status': 'Pendente'}, {'num': 25, 'ticket': '21652', 'cliente': 'LEAL', 'desc': 'Formas de Recebimento - Boleto', 'est': '', 'status': 'Pendente'}, {'num': 26, 'ticket': '25271', 'cliente': 'MILANI', 'desc': 'Filtro de seleção de NF na alteração de preços', 'est': '', 'status': 'Pendente'}, {'num': 27, 'ticket': '22981', 'cliente': 'SCHUTZE', 'desc': 'Seleção de nota em documentos de devolução', 'est': '', 'status': 'Pendente'}, {'num': 28, 'ticket': '25443', 'cliente': 'GUMZ', 'desc': 'Parâmetros PDV – Operações que Exigem Supervisor', 'est': 'URGENTE', 'status': 'Urgente'}, {'num': 29, 'ticket': '24134', 'cliente': 'LEAL', 'desc': 'Limitação Logus PDV – ausência de observação na NF-e', 'est': '', 'status': 'Pendente'}]

def _dc(d):
    if d<=3:  return '#4ade80','#052e16'
    if d<=7:  return '#fde047','#1c1a00'
    if d<=14: return '#fb923c','#1c0a00'
    if d<=30: return '#f87171','#1c0000'
    return '#ef4444','#150000'

def _sbadge(s):
    m = {'Novo':('22c55e','NOVO'),'Em andamento':('3b82f6','EM ANDAMENTO'),'Aguardando':('d97706','AGUARDANDO')}
    c,l = m.get(s,('6b7280',s.upper()))
    return f'<span style="color:#{c};font-size:10px;font-weight:900;border:1px solid #{c};border-radius:4px;padding:3px 8px">{l}</span>'

def _ticon(t):
    return {'Incidente':'🔴','Requisição':'🔵','Dúvida':'🟣'}.get(t,'⚪')

def _tk(t, sc=True):
    fc,bg = _dc(t['dias'])
    cli = f'<div style="color:#f97316;font-size:13px;font-weight:900;margin-bottom:4px">{t["empresa"]}</div>' if sc else ''
    return (f'<div style="background:#161616;border-radius:12px;padding:14px 16px;margin-bottom:10px;border-left:5px solid {fc}">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
            f'<span style="color:{fc};font-size:18px;font-weight:900">#{t["code"]}</span>'
            f'<span style="background:{bg};color:{fc};font-size:20px;font-weight:900;padding:4px 12px;border-radius:8px">{t["dias"]}d</span></div>'
            f'{cli}'
            f'<div style="color:#e2e8f0;font-size:14px;line-height:1.5;margin-bottom:10px">{_ticon(t["tipo"])} {t["assunto"]}</div>'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">'
            f'<span style="color:#94a3b8;font-size:12px">{t["atrib"]}</span>'
            f'{_sbadge(t["status"])}</div></div>')

def _csec(emp, tks, idx):
    tks_s = sorted(tks, key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias']))
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc,_ = _dc(mx)
    itag = f' · <span style="color:#ef4444">⚠ {inc} inc</span>' if inc else ''
    cards = ''.join(_tk(t, sc=False) for t in tks_s)
    return (f'<div style="margin-bottom:8px;border-radius:12px;overflow:hidden;border:1px solid #222">'
            f'<div onclick="tog({idx})" style="background:#1a1a1a;padding:16px;display:flex;justify-content:space-between;align-items:center;cursor:pointer">'
            f'<div><div style="color:#fff;font-size:15px;font-weight:900">{emp}</div>'
            f'<div style="color:#64748b;font-size:12px;margin-top:2px">{len(tks)} chamados{itag} · até <span style="color:{fc}">{mx}d</span></div></div>'
            f'<span id="chev{idx}" style="color:#475569;font-size:18px">▶</span></div>'
            f'<div id="sec{idx}" style="display:none;padding:12px">{cards}</div></div>')

def _rsec(resp, tks, idx, cor='#ea580c'):
    tks_s = sorted(tks, key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias']))
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc,_ = _dc(mx)
    itag = f' · <span style="color:#ef4444">⚠ {inc} inc</span>' if inc else ''
    cards = ''.join(_tk(t, sc=True) for t in tks_s)
    return (f'<div style="margin-bottom:8px;border-radius:12px;overflow:hidden;border:1px solid #222">'
            f'<div onclick="tog({idx})" style="background:#1a1a1a;padding:16px;display:flex;justify-content:space-between;align-items:center;cursor:pointer">'
            f'<div><div style="color:{cor};font-size:15px;font-weight:900">{resp}</div>'
            f'<div style="color:#64748b;font-size:12px;margin-top:2px">{len(tks)} chamados{itag} · até <span style="color:{fc}">{mx}d</span></div></div>'
            f'<span id="chev{idx}" style="color:#475569;font-size:18px">▶</span></div>'
            f'<div id="sec{idx}" style="display:none;padding:12px">{cards}</div></div>')

def _ugrp(titulo, cor, bg, tks, sc=True):
    if not tks: return ''
    cards = ''.join(_tk(t, sc=sc) for t in sorted(tks, key=lambda x:-x['dias']))
    return (f'<div style="margin-bottom:16px">'
            f'<div style="background:{bg};border-left:4px solid {cor};border-radius:8px;padding:10px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center">'
            f'<span style="color:{cor};font-size:13px;font-weight:900">{titulo}</span>'
            f'<span style="color:{cor};font-size:20px;font-weight:900">{len(tks)}</span></div>'
            f'{cards}</div>')

def _ccard(b):
    s = b['status']
    cor = {'Urgente':'#ef4444','Homologado':'#22c55e','Em Homologação':'#fb923c','Em Roadmap':'#60a5fa'}.get(s,'#6b7280')
    bg  = {'Urgente':'#1a0000','Homologado':'#052e16','Em Homologação':'#1a0800','Em Roadmap':'#051525'}.get(s,'#111')
    return (f'<div style="background:{bg};border-radius:10px;padding:12px 14px;margin-bottom:8px;border-left:4px solid {cor}">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
            f'<span style="color:#f97316;font-size:15px;font-weight:900">#{b["ticket"]}</span>'
            f'<span style="color:{cor};font-size:10px;font-weight:900;border:1px solid {cor};border-radius:4px;padding:2px 8px">{s.upper()}</span></div>'
            f'<div style="color:#fed7aa;font-size:12px;font-weight:700;margin-bottom:4px">{b["cliente"]}</div>'
            f'<div style="color:#e2e8f0;font-size:13px;line-height:1.4">{b["desc"]}</div>'
            +(f'<div style="color:{cor};font-size:11px;font-weight:700;margin-top:6px">Est.: {b["est"]}</div>' if b['est'] else '')
            +'</div>')

def _bar(lbl, v, tot, cor):
    pct = int(v/tot*100) if tot else 0
    return (f'<div style="margin-bottom:14px">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:5px">'
            f'<span style="color:#9ca3af;font-size:13px">{lbl}</span>'
            f'<span style="color:{cor};font-size:16px;font-weight:900">{v} <span style="color:#374151;font-size:11px">{pct}%</span></span></div>'
            f'<div style="background:#1f2937;border-radius:6px;height:10px"><div style="width:{pct}%;background:{cor};height:100%;border-radius:6px"></div></div></div>')

def gerar_html(all_tks, baixados_hoje=None):
    today     = date.today()
    today_str = today.strftime('%d/%m/%Y')
    baixados_hoje = baixados_hoje or []

    for t in all_tks:
        if t['code'] in PATCHES:
            t.update(PATCHES[t['code']])

    sul_emp = set(SUL_EMP)
    for t in all_tks:
        if 'logus sul' in t.get('grupo','').lower() or t.get('ordem') or t.get('atrib') in SUL_TEAM:
            if t['empresa'] not in ('LOGUS','SEM EMPRESA',''):
                sul_emp.add(t['empresa'])
    sul_emp -= {'LOGUS','SEM EMPRESA',''}

    sul = [t for t in all_tks if t['empresa'] in sul_emp]
    by_cli  = defaultdict(list)
    by_resp = defaultdict(list)
    for t in sul:
        by_cli[t['empresa']].append(t)
        by_resp[t['atrib']].append(t)

    clientes   = sorted(by_cli.keys())
    sr = lambda r: (-(sum(1 for t in by_resp[r] if t['tipo']=='Incidente')), -len(by_resp[r]))
    resp_sul   = sorted([r for r in by_resp if r in SUL_RESP],    key=sr)
    resp_logus = sorted([r for r in by_resp if r not in SUL_RESP], key=sr)

    tot=len(sul); tot_inc=sum(1 for t in sul if t['tipo']=='Incidente')
    tot_ag=sum(1 for t in sul if t['status']=='Aguardando')
    n_cli=len(clientes)

    tk_lkp = {t['code']:t for t in all_tks}
    def _sec(codes): return [t for t in sul if t['code'] in codes]
    def _sa(atr): return sorted([t for t in sul if t['atrib']==atr and t['code'] not in URG_ALL], key=lambda x:-x['dias'])

    pdv_tks=_sec(URG_PDV); erp_tks=_sec(URG_ERP)
    eng_tks=_sa('Engenharia Software'); pdvd_tks=_sa('Desenv. PDV')
    sust_tks=_sa('Sustentação Desenv.'); com_tks=_sa('Comercial')
    alta_tks=[t for t in sul if t['code'] not in URG_ALL and t['atrib'] not in RESP_OWN]

    def _dtk(code,emp,desc):
        t=tk_lkp.get(code)
        return t if t else {'code':code,'empresa':emp,'assunto':desc,'atrib':'—','status':'—','tipo':'Requisição','dias':0}
    dev_tks=[_dtk('24760','GUMZ','Erro Finalização notas simples nacional'),
             _dtk('24621','VICARI','Controle de trocas — Erro filtro Filiais'),
             _dtk('25368','BEBIDA POP','Emissão de NF — Transformar Pedido em NF')]

    n_urg=len(pdv_tks)+len(erp_tks)+len(alta_tks)+len(eng_tks)+len(pdvd_tks)+len(sust_tks)+3+len(com_tks)

    idx=0
    cli_secs=''
    for emp in sorted(clientes, key=lambda e:(-sum(1 for t in by_cli[e] if t['tipo']=='Incidente'),-len(by_cli[e]))):
        cli_secs+=_csec(emp,by_cli[emp],idx); idx+=1

    resp_secs='<div style="color:#f97316;font-size:11px;font-weight:700;letter-spacing:1px;padding:8px 4px 6px">🌿 EQUIPE SUL</div>'
    for r in resp_sul:   resp_secs+=_rsec(r,by_resp[r],idx,'#f97316'); idx+=1
    resp_secs+='<div style="color:#a78bfa;font-size:11px;font-weight:700;letter-spacing:1px;padding:14px 4px 6px">🏢 EQUIPE LOGUS</div>'
    for r in resp_logus: resp_secs+=_rsec(r,by_resp[r],idx,'#a78bfa'); idx+=1

    urg_html=(
        _ugrp('🟢 PDV — Urgente','#4ade80','#052e16',pdv_tks)+
        _ugrp('🔴 ERP — Urgente','#ef4444','#1a0000',erp_tks)+
        _ugrp('📋 Em Alta','#60a5fa','#05152a',alta_tks)+
        _ugrp('💻 Dev / Sustentação','#a78bfa','#0d0520',dev_tks)+
        _ugrp('🔩 Engenharia','#94a3b8','#111827',eng_tks)+
        _ugrp('🖥️ Desenv. PDV','#2dd4bf','#051a17',pdvd_tks)+
        _ugrp('🛠️ Sustentação Desenv.','#818cf8','#0d0f20',sust_tks)+
        _ugrp('🤝 Comercial','#fbbf24','#1a1000',com_tks)
    )

    cust_html=''
    for st in ['Urgente','Em Homologação','Em Roadmap','Pendente','Homologado']:
        grp=[b for b in BACKLOG if b['status']==st]
        if not grp: continue
        cor={'Urgente':'#ef4444','Em Homologação':'#fb923c','Em Roadmap':'#60a5fa','Homologado':'#22c55e'}.get(st,'#6b7280')
        cust_html+=(f'<div style="color:{cor};font-size:11px;font-weight:700;letter-spacing:1px;padding:10px 4px 6px">{st.upper()} — {len(grp)}</div>'
                    +''.join(_ccard(b) for b in grp))

    n_nov=sum(1 for t in sul if t['status']=='Novo')
    n_and=sum(1 for t in sul if t['status']=='Em andamento')
    n_req=sum(1 for t in sul if t['tipo']=='Requisição')
    n_duv=sum(1 for t in sul if t['tipo'] not in ('Incidente','Requisição'))
    n_resol=len(baixados_hoje); n_hoje=sum(1 for t in sul if t['dias']==0)
    hoje_cards=''.join(_tk(t) for t in sorted([t for t in sul if t['dias']==0],key=lambda x:x['empresa']))
    bx_cards=''.join(_tk(t) for t in sorted(baixados_hoje,key=lambda x:x.get('empresa','')))

    res_html=(
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:18px">'
        +f'<div style="background:#052e16;border:2px solid #22c55e;border-radius:12px;padding:14px;text-align:center"><div style="color:#4ade80;font-size:32px;font-weight:900">{n_hoje}</div><div style="color:#22c55e;font-size:11px;font-weight:700">ENTRARAM HOJE</div></div>'
        +f'<div style="background:#0a0a16;border:2px solid #3b82f6;border-radius:12px;padding:14px;text-align:center"><div style="color:#60a5fa;font-size:32px;font-weight:900">{tot}</div><div style="color:#3b82f6;font-size:11px;font-weight:700">TOTAL ABERTOS</div></div>'
        +f'<div style="background:#1a0000;border:2px solid #ef4444;border-radius:12px;padding:14px;text-align:center"><div style="color:#f87171;font-size:32px;font-weight:900">{tot_inc}</div><div style="color:#ef4444;font-size:11px;font-weight:700">INCIDENTES</div></div>'
        +(f'<div style="background:#052e16;border:2px solid #22c55e;border-radius:12px;padding:14px;text-align:center"><div style="color:#4ade80;font-size:32px;font-weight:900">{n_resol}</div><div style="color:#22c55e;font-size:11px;font-weight:700">RESOLVIDOS HOJE</div></div>' if n_resol else f'<div style="background:#111;border:2px solid #1f2937;border-radius:12px;padding:14px;text-align:center"><div style="color:#374151;font-size:32px;font-weight:900">—</div><div style="color:#374151;font-size:11px;font-weight:700">RESOLVIDOS HOJE</div></div>')
        +f'</div>'
        +f'<div style="background:#161616;border-radius:12px;padding:16px;margin-bottom:14px">'
        +f'<div style="color:#64748b;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:14px">STATUS</div>'
        +_bar('Novo',n_nov,tot,'#22c55e')+_bar('Em Andamento',n_and,tot,'#3b82f6')+_bar('Aguardando',tot_ag,tot,'#d97706')
        +f'</div>'
        +f'<div style="background:#161616;border-radius:12px;padding:16px;margin-bottom:14px">'
        +f'<div style="color:#64748b;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:14px">TIPO</div>'
        +_bar('Incidente',tot_inc,tot,'#ef4444')+_bar('Requisição',n_req,tot,'#3b82f6')+_bar('Dúvida/Outros',n_duv,tot,'#a78bfa')
        +f'</div>'
        +(f'<div style="color:#22c55e;font-size:12px;font-weight:700;letter-spacing:1px;padding:4px 0 8px">📥 ENTRARAM HOJE</div>'+hoje_cards if n_hoje else '')
        +(f'<div style="color:#22c55e;font-size:12px;font-weight:700;letter-spacing:1px;padding:4px 0 8px">📤 RESOLVIDOS HOJE</div>'+bx_cards if n_resol else '')
    )

    return f"""<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Logus Sul BI · {today_str}</title>
<link rel="icon" href="/static/favicon.ico">
<style>
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
html,body{{height:100%;background:#0c0c0c;color:#e5e7eb;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
body{{padding-bottom:70px}}
#hdr{{position:sticky;top:0;z-index:100;background:#0c0c0c;border-bottom:1px solid #1a1a1a;padding:10px 14px}}
.hdr-top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}}
.hdr-logo{{height:36px;background:#fff;border-radius:7px;padding:3px 8px}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}}
.stat{{background:#161616;border-radius:8px;padding:7px 4px;text-align:center}}
.stat-n{{font-size:20px;font-weight:900}}
.stat-l{{font-size:9px;font-weight:700;letter-spacing:.3px;margin-top:1px}}
#content{{padding:12px 14px}}
.view{{display:none}}.view.on{{display:block}}
#nav{{position:fixed;bottom:0;left:0;right:0;background:#111;border-top:1px solid #1f2937;display:flex;z-index:100;padding-bottom:env(safe-area-inset-bottom)}}
.nb{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:8px 4px 10px;cursor:pointer;border:none;background:none;color:#4b5563;font-size:9px;font-weight:700;gap:3px;transition:color .15s}}
.nb .ni{{font-size:22px;line-height:1}}
.nb.on{{color:#f97316}}.nb.on-urg{{color:#ef4444}}.nb.on-res{{color:#22c55e}}.nb.on-cust{{color:#a78bfa}}
.sec-hdr{{color:#64748b;font-size:11px;font-weight:700;letter-spacing:1px;padding:6px 0 10px}}
@keyframes pulse{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
</style>
<script>
function showTab(t){{
  document.querySelectorAll('.view').forEach(function(v){{v.classList.remove('on')}});
  document.getElementById('v-'+t).classList.add('on');
  document.querySelectorAll('.nb').forEach(function(b){{b.className='nb'}});
  var cls={{'cli':'on','resp':'on','urg':'on-urg','res':'on-res','cust':'on-cust'}};
  document.getElementById('nb-'+t).className='nb '+(cls[t]||'on');
  window.scrollTo(0,0);
}}
function tog(i){{
  var s=document.getElementById('sec'+i);
  var c=document.getElementById('chev'+i);
  var open=s.style.display!=='none';
  s.style.display=open?'none':'block';
  c.textContent=open?'▶':'▼';
}}
window.onload=function(){{showTab('cli')}};
</script></head><body>
<div id="hdr">
  <div class="hdr-top">
    <img class="hdr-logo" src="/static/logo.png">
    <span style="color:#6b4c30;font-size:11px">📅 {today_str}</span>
  </div>
  <div class="stats">
    <div class="stat"><div class="stat-n" style="color:#f97316">{n_cli}</div><div class="stat-l" style="color:#6b4c30">CLIENTES</div></div>
    <div class="stat"><div class="stat-n" style="color:#fb923c">{tot}</div><div class="stat-l" style="color:#6b4c30">CHAMADOS</div></div>
    <div class="stat"><div class="stat-n" style="color:#ef4444">{tot_inc}</div><div class="stat-l" style="color:#6b4c30">INCIDENTES</div></div>
    <div class="stat"><div class="stat-n" style="color:#f97316;animation:pulse 1.4s infinite">{n_urg}</div><div class="stat-l" style="color:#6b4c30">URGENTES</div></div>
  </div>
</div>
<div id="content">
  <div id="v-cli" class="view"><div class="sec-hdr">POR CLIENTE — {n_cli} clientes</div>{cli_secs}</div>
  <div id="v-resp" class="view"><div class="sec-hdr">POR RESPONSÁVEL</div>{resp_secs}</div>
  <div id="v-urg" class="view"><div class="sec-hdr">🚨 URGENTES — {n_urg} chamados</div>{urg_html}</div>
  <div id="v-res" class="view"><div class="sec-hdr">📊 RESULTADOS — {today_str}</div>{res_html}</div>
  <div id="v-cust" class="view"><div class="sec-hdr">🔧 CUSTOMIZAÇÕES — {len(BACKLOG)} itens</div>{cust_html}</div>
</div>
<nav id="nav">
  <button class="nb on"  id="nb-cli"  onclick="showTab('cli')"><span class="ni">👥</span>Clientes</button>
  <button class="nb"     id="nb-resp" onclick="showTab('resp')"><span class="ni">👤</span>Responsável</button>
  <button class="nb"     id="nb-urg"  onclick="showTab('urg')"><span class="ni">🚨</span>Urgentes</button>
  <button class="nb"     id="nb-res"  onclick="showTab('res')"><span class="ni">📊</span>Resultados</button>
  <button class="nb"     id="nb-cust" onclick="showTab('cust')"><span class="ni">🔧</span>Customiz.</button>
</nav>
</body></html>"""
