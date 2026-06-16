from datetime import date, datetime, timezone, timedelta
from collections import defaultdict

def _hoje_brt():
    return datetime.now(timezone(timedelta(hours=-3))).date()

SUL_EMP = {
    'GUMZ','MERCADO DE BEBIDA POP','MILANI','PARANA SUPERMERCADO',
    'MAIS BRASIL - VAREJUS','CASA DE CARNES PETRY',
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

# ── shared helpers ────────────────────────────────────────────────────────────

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

# ── mobile helpers ────────────────────────────────────────────────────────────

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

# ── desktop helpers ───────────────────────────────────────────────────────────

def _d_safe(s):
    return ''.join(c if c.isalnum() else '_' for c in s)

def _d_stat(label, val, cor, tab=''):
    click = f' onclick="dTab(\'{tab}\')" title="Ir para {label}"' if tab else ''
    return (f'<div class="dstat"{click} style="border:1px solid {cor};border-radius:6px;padding:8px 18px;text-align:center;min-width:90px">'
            f'<div style="color:{cor};font-size:26px;font-weight:900;line-height:1.1">{val}</div>'
            f'<div style="color:{cor};font-size:9px;font-weight:700;opacity:.6;margin-top:4px;letter-spacing:.5px">{label}</div></div>')

def _d_row(t):
    fc,_ = _dc(t['dias'])
    tc = '#ef4444' if t['tipo']=='Incidente' else '#3b82f6' if t['tipo']=='Requisição' else '#a78bfa'
    ec = {'Novo':'#22c55e','Em andamento':'#3b82f6','Aguardando':'#d97706'}.get(t['status'],'#6b7280')
    return (f'<tr style="border-bottom:1px solid #111">'
            f'<td style="color:#f97316;font-weight:900;padding:9px 12px;white-space:nowrap">#{t["code"]}</td>'
            f'<td style="padding:9px 12px"><span style="background:{tc}22;color:{tc};border-radius:4px;padding:3px 8px;font-size:10px;font-weight:900">{t["tipo"].upper()}</span></td>'
            f'<td style="color:#e2e8f0;padding:9px 12px;font-size:13px">{t["assunto"]}</td>'
            f'<td style="padding:9px 12px"><span style="background:{ec}22;color:{ec};border-radius:4px;padding:3px 8px;font-size:10px;font-weight:900">{t["status"].upper()}</span></td>'
            f'<td style="color:#94a3b8;padding:9px 12px;font-size:12px;white-space:nowrap">{t["atrib"]}</td>'
            f'<td style="color:#64748b;padding:9px 12px;font-size:12px;white-space:nowrap">{t["data"]}</td>'
            f'<td style="color:{fc};font-weight:900;padding:9px 12px;text-align:right;white-space:nowrap">{t["dias"]}</td>'
            f'</tr>')

def _d_tbl_hdr():
    return ('<thead><tr style="border-bottom:2px solid #1f2937">'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">TICKET</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">TIPO</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">ASSUNTO</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">ESTADO</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">COM QUEM</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">ABERTURA</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:right;padding:8px 12px">DIAS</th>'
            '</tr></thead>')

def _d_clibox(emp, tks):
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc,_ = _dc(mx)
    sid = _d_safe(emp)
    itag = f'<div style="color:#ef4444;font-size:11px;margin-top:2px">⚠ {inc} inc</div>' if inc else ''
    return (f'<div class="dcbox" data-id="{sid}" onclick="dCli(\'{sid}\')" '
            f'style="border:1px solid #3a1800;border-radius:8px;padding:12px 14px;cursor:pointer;background:#0d0800;min-width:130px">'
            f'<div style="color:#f97316;font-size:12px;font-weight:900;margin-bottom:3px">{emp}</div>'
            f'<div style="color:#fb923c;font-size:12px">{len(tks)} tickets</div>'
            f'{itag}'
            f'<div style="color:{fc};font-size:13px;font-weight:700;margin-top:4px">{mx}d</div></div>')

def _d_respbox(resp, tks, cor):
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc,_ = _dc(mx)
    sid = _d_safe(resp)
    itag = f'<div style="color:#ef4444;font-size:11px;margin-top:2px">⚠ {inc} inc</div>' if inc else ''
    return (f'<div class="drbox" onclick="dResp(\'{sid}\')" '
            f'style="border:1px solid #1e1040;border-radius:8px;padding:12px 14px;cursor:pointer;background:#0a0814;min-width:150px">'
            f'<div style="color:{cor};font-size:12px;font-weight:900;margin-bottom:3px">{resp}</div>'
            f'<div style="color:#64748b;font-size:12px">{len(tks)} chamados</div>'
            f'{itag}'
            f'<div style="color:{fc};font-size:13px;font-weight:700;margin-top:4px">{mx}d</div></div>')

def _d_detail(label, tks, div_id, close_fn):
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc,_ = _dc(mx)
    resps = sorted(set(t['atrib'] for t in tks))
    rtags = ''.join(f'<span style="background:#ea580c22;color:#f97316;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700;margin-right:6px">{r}</span>' for r in resps)
    rows  = ''.join(_d_row(t) for t in sorted(tks, key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias'])))
    ispn  = f'<span style="color:#ef4444;font-size:12px">⚠ {inc} inc</span> ' if inc else ''
    return (f'<div id="{div_id}" class="ddet" style="display:none;background:#090500;border:1px solid #3a1800;border-radius:8px;margin-top:10px;padding:16px 20px">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:10px">'
            f'<div style="display:flex;align-items:center;gap:14px">'
            f'<span style="color:#f97316;font-size:16px;font-weight:900">{label}</span>'
            f'<span style="color:#94a3b8;font-size:12px">{len(tks)} chamados</span>'
            f'{ispn}<span style="color:{fc};font-size:13px;font-weight:700">{mx}d</span></div>'
            f'<button onclick="{close_fn}" style="background:none;border:1px solid #333;color:#6b7280;border-radius:4px;padding:4px 10px;cursor:pointer;font-size:11px">✕ fechar</button>'
            f'</div>'
            f'<div style="margin-bottom:12px">{rtags}</div>'
            f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">'
            f'{_d_tbl_hdr()}<tbody>{rows}</tbody></table></div></div>')

def _d_urg_sec(titulo, cor, bg, tks):
    if not tks: return ''
    rows = ''.join(_d_row(t) for t in sorted(tks, key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias'])))
    return (f'<div style="margin-bottom:20px">'
            f'<div style="background:{bg};border-left:4px solid {cor};border-radius:6px;padding:10px 16px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between">'
            f'<span style="color:{cor};font-size:13px;font-weight:900">{titulo}</span>'
            f'<span style="color:{cor};font-size:18px;font-weight:900">{len(tks)}</span></div>'
            f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">'
            f'{_d_tbl_hdr()}<tbody>{rows}</tbody></table></div></div>')

# ── main ──────────────────────────────────────────────────────────────────────

def gerar_html(all_tks, baixados_hoje=None):
    today     = _hoje_brt()
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

    # filtra baixados para conter apenas clientes da base Sul
    baixados_hoje = [t for t in baixados_hoje if t['empresa'] in sul_emp]

    # agrupa por data de resolução
    by_res = defaultdict(list)
    for t in baixados_hoje:
        if t['resolucao']:
            by_res[t['resolucao']].append(t)
    datas_res = sorted(by_res.keys(), reverse=True)

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
    n_cli=len(clientes); n_nov=sum(1 for t in sul if t['status']=='Novo')
    n_and=sum(1 for t in sul if t['status']=='Em andamento')
    n_req=sum(1 for t in sul if t['tipo']=='Requisição')
    n_duv=sum(1 for t in sul if t['tipo'] not in ('Incidente','Requisição'))
    n_resol=len(by_res.get(today_str,[])); n_hoje=sum(1 for t in sul if t['data']==today_str)

    tk_lkp = {t['code']:t for t in all_tks}
    def _sec(codes): return [t for t in sul if t['code'] in codes]
    def _sa(atr): return sorted([t for t in sul if t['atrib']==atr and t['code'] not in URG_ALL], key=lambda x:-x['dias'])

    pdv_tks=_sec(URG_PDV); erp_tks=_sec(URG_ERP)
    eng_tks=_sa('Engenharia Software'); pdvd_tks=_sa('Desenv. PDV')
    sust_tks=_sa('Sustentação Desenv.'); com_tks=_sa('Comercial')
    alta_tks=[t for t in sul if t['code'] not in URG_ALL and t['atrib'] not in RESP_OWN]

    def _dtk(code,emp,desc):
        t=tk_lkp.get(code)
        return t if t else {'code':code,'empresa':emp,'assunto':desc,'atrib':'—','status':'—','tipo':'Requisição','dias':0,'data':'','resolucao':''}
    dev_tks=[_dtk('24760','GUMZ','Erro Finalização notas simples nacional'),
             _dtk('24621','VICARI','Controle de trocas — Erro filtro Filiais'),
             _dtk('25368','BEBIDA POP','Emissão de NF — Transformar Pedido em NF')]

    n_urg=len(pdv_tks)+len(erp_tks)+len(alta_tks)+len(eng_tks)+len(pdvd_tks)+len(sust_tks)+3+len(com_tks)
    n_bklog=len(BACKLOG)

    # ── mobile HTML vars ──────────────────────────────────────────────────────
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

    hoje_cards=''.join(_tk(t) for t in sorted([t for t in sul if t['data']==today_str],key=lambda x:x['empresa']))

    # seletor de datas para baixados
    date_opts=''
    for i,dt in enumerate(datas_res):
        safe=dt.replace('/','_')
        lbl=f'{dt}  ✅ hoje' if dt==today_str else dt
        sel='selected' if i==0 else ''
        date_opts+=f'<option value="{safe}" {sel}>{lbl}</option>'

    # seções mobile (cards) por data
    mob_bx=''
    for i,dt in enumerate(datas_res):
        safe=dt.replace('/','_')
        tks=sorted(by_res[dt],key=lambda x:x.get('empresa',''))
        show='block' if i==0 else 'none'
        mob_bx+=f'<div id="mbx-{safe}" class="bx-s" style="display:{show}">'+\
                ''.join(_tk(t) for t in tks)+'</div>'

    # seções desktop (tabelas) por data
    dt_bx=''
    for i,dt in enumerate(datas_res):
        safe=dt.replace('/','_')
        tks=sorted(by_res[dt],key=lambda x:x.get('empresa',''))
        show='block' if i==0 else 'none'
        rows=''.join(_d_row(t) for t in tks)
        dt_bx+=(f'<div id="dbx-{safe}" class="bx-s" style="display:{show}">'
                f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">'
                f'{_d_tbl_hdr()}<tbody>{rows}</tbody></table></div></div>')

    mob_res=(
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
        +(f'<div style="color:#22c55e;font-size:12px;font-weight:700;letter-spacing:1px;padding:8px 0 6px">📤 RESOLVIDOS</div>'
          f'<select onchange="filtrarRes(\'mbx\',this.value)" style="width:100%;background:#161616;color:#e5e7eb;border:1px solid #333;border-radius:6px;padding:8px 10px;font-size:13px;margin-bottom:10px">{date_opts}</select>'
          +mob_bx if datas_res else '')
    )

    # ── desktop HTML vars ─────────────────────────────────────────────────────
    cli_ord = sorted(clientes, key=lambda e:(-sum(1 for t in by_cli[e] if t['tipo']=='Incidente'),-len(by_cli[e])))
    dt_cli_grid    = ''.join(_d_clibox(e,by_cli[e]) for e in cli_ord)
    dt_cli_details = ''.join(_d_detail(e,by_cli[e],f'dtd-{_d_safe(e)}','dCli(null)') for e in clientes)

    dt_rsul_grid    = ''.join(_d_respbox(r,by_resp[r],'#f97316') for r in resp_sul)
    dt_rlogus_grid  = ''.join(_d_respbox(r,by_resp[r],'#a78bfa') for r in resp_logus)
    dt_rsul_det     = ''.join(_d_detail(r,by_resp[r],f'dtr-{_d_safe(r)}','dResp(null)') for r in resp_sul)
    dt_rlogus_det   = ''.join(_d_detail(r,by_resp[r],f'dtr-{_d_safe(r)}','dResp(null)') for r in resp_logus)

    dt_urg_html=(
        _d_urg_sec('🟢 PDV — Urgente','#4ade80','#052e16',pdv_tks)+
        _d_urg_sec('🔴 ERP — Urgente','#ef4444','#1a0000',erp_tks)+
        _d_urg_sec('📋 Em Alta','#60a5fa','#05152a',alta_tks)+
        _d_urg_sec('💻 Dev / Sustentação','#a78bfa','#0d0520',dev_tks)+
        _d_urg_sec('🔩 Engenharia','#94a3b8','#111827',eng_tks)+
        _d_urg_sec('🖥️ Desenv. PDV','#2dd4bf','#051a17',pdvd_tks)+
        _d_urg_sec('🛠️ Sustentação Desenv.','#818cf8','#0d0f20',sust_tks)+
        _d_urg_sec('🤝 Comercial','#fbbf24','#1a1000',com_tks)
    )

    dt_cust_rows=''
    for st in ['Urgente','Em Homologação','Em Roadmap','Pendente','Homologado']:
        for b in [x for x in BACKLOG if x['status']==st]:
            s=b['status']
            cor={'Urgente':'#ef4444','Homologado':'#22c55e','Em Homologação':'#fb923c','Em Roadmap':'#60a5fa'}.get(s,'#6b7280')
            est=b['est'] if b['est'] else '—'
            dt_cust_rows+=(f'<tr style="border-bottom:1px solid #111">'
                           f'<td style="color:#f97316;font-weight:900;padding:9px 12px;white-space:nowrap">#{b["ticket"]}</td>'
                           f'<td style="color:#fed7aa;padding:9px 12px;font-size:12px;font-weight:700">{b["cliente"]}</td>'
                           f'<td style="color:#e2e8f0;padding:9px 12px;font-size:13px">{b["desc"]}</td>'
                           f'<td style="color:{cor};padding:9px 12px;font-size:11px;white-space:nowrap">{est}</td>'
                           f'<td style="padding:9px 12px"><span style="background:{cor}22;color:{cor};border-radius:4px;padding:3px 8px;font-size:10px;font-weight:900">{s.upper()}</span></td>'
                           f'</tr>')

    pct_nov=int(n_nov/tot*100) if tot else 0
    pct_and=int(n_and/tot*100) if tot else 0
    pct_ag =int(tot_ag/tot*100) if tot else 0
    pct_inc=int(tot_inc/tot*100) if tot else 0
    pct_req=int(n_req/tot*100) if tot else 0
    pct_duv=int(n_duv/tot*100) if tot else 0

    dt_res_html=(
        f'<div style="display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap">'
        +_d_stat('ENTRARAM HOJE',n_hoje,'#22c55e')
        +_d_stat('TOTAL ABERTOS',tot,'#3b82f6')
        +_d_stat('INCIDENTES',tot_inc,'#ef4444')
        +_d_stat('AGUARDANDO',tot_ag,'#d97706')
        +(_d_stat('RESOLVIDOS HOJE',n_resol,'#22c55e') if n_resol else '')
        +f'</div>'
        +f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'
        +f'<div style="background:#161616;border-radius:10px;padding:18px">'
        +f'<div style="color:#64748b;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:14px">STATUS</div>'
        +_bar('Novo',n_nov,tot,'#22c55e')+_bar('Em Andamento',n_and,tot,'#3b82f6')+_bar('Aguardando',tot_ag,tot,'#d97706')
        +f'</div>'
        +f'<div style="background:#161616;border-radius:10px;padding:18px">'
        +f'<div style="color:#64748b;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:14px">TIPO</div>'
        +_bar('Incidente',tot_inc,tot,'#ef4444')+_bar('Requisição',n_req,tot,'#3b82f6')+_bar('Dúvida/Outros',n_duv,tot,'#a78bfa')
        +f'</div></div>'
        +(f'<div style="color:#22c55e;font-size:12px;font-weight:700;letter-spacing:1px;margin:20px 0 10px">📥 ENTRARAM HOJE</div>'
          +f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">{_d_tbl_hdr()}<tbody>'
          +''.join(_d_row(t) for t in sorted([t for t in sul if t['data']==today_str],key=lambda x:x['empresa']))
          +f'</tbody></table></div>' if n_hoje else '')
        +(f'<div style="display:flex;align-items:center;gap:14px;margin:20px 0 12px">'
          f'<span style="color:#22c55e;font-size:12px;font-weight:700;letter-spacing:1px">📤 RESOLVIDOS</span>'
          f'<select onchange="filtrarRes(\'dbx\',this.value)" style="background:#161616;color:#e5e7eb;border:1px solid #333;border-radius:6px;padding:6px 12px;font-size:13px">{date_opts}</select>'
          f'</div>{dt_bx}' if datas_res else '')
    )

    dt_hdr_stats=(_d_stat('CLIENTES',n_cli,'#f97316','cli')
                  +_d_stat('CHAMADOS',tot,'#fb923c','cli')
                  +_d_stat('INCIDENTES',tot_inc,'#ef4444','urg')
                  +_d_stat('AGUARDANDO',tot_ag,'#d97706','resp')
                  +_d_stat('NOVOS',n_nov,'#22c55e','res'))

    return f"""<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Logus Sul BI · {today_str}</title>
<link rel="icon" href="/static/favicon.ico">
<style>
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
html,body{{background:#0c0c0c;color:#e5e7eb;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
@keyframes pulse{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
/* ── mobile (padrão) ── */
#dt{{display:none}}
#mob{{display:block}}
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
/* ── desktop (sobrescreve mobile acima de 768px) ── */
@media(min-width:768px){{
  body{{padding:0}}
  #dt{{display:block}}
  #mob{{display:none}}
  .dtab{{background:none;border:none;color:#64748b;font-size:13px;font-weight:700;padding:11px 22px;cursor:pointer;border-bottom:3px solid transparent;transition:color .15s}}
  .dtab:hover{{color:#e5e7eb}}
  .dtab.on{{color:#f97316;border-bottom-color:#f97316}}
  .dview{{display:none}}.dview.on{{display:block}}
  .dcbox:hover,.drbox:hover{{background:#1a0800!important}}
  .dcbox.sel{{background:#1a0800!important;border-color:#f97316!important}}
  .dstat{{cursor:pointer;transition:opacity .15s}}.dstat:hover{{opacity:.75}}
}}
</style>
<script>
/* desktop */
function dTab(t){{
  document.querySelectorAll('.dview').forEach(function(v){{v.style.display='none'}});
  var el=document.getElementById('dv-'+t); if(el)el.style.display='block';
  document.querySelectorAll('.dtab').forEach(function(b){{b.classList.remove('on')}});
  var tb=document.getElementById('dtb-'+t); if(tb)tb.classList.add('on');
}}
function dCli(id){{
  document.querySelectorAll('.ddet').forEach(function(d){{d.style.display='none'}});
  document.querySelectorAll('.dcbox').forEach(function(b){{b.classList.remove('sel')}});
  if(id){{
    var d=document.getElementById('dtd-'+id); if(d)d.style.display='block';
    document.querySelectorAll('[data-id="'+id+'"]').forEach(function(b){{b.classList.add('sel')}});
  }}
}}
function dResp(id){{
  document.querySelectorAll('.ddet').forEach(function(d){{d.style.display='none'}});
  if(id){{var d=document.getElementById('dtr-'+id); if(d)d.style.display='block';}}
}}
/* mobile */
function showTab(t){{
  document.querySelectorAll('.view').forEach(function(v){{v.classList.remove('on')}});
  var el=document.getElementById('v-'+t); if(el)el.classList.add('on');
  document.querySelectorAll('.nb').forEach(function(b){{b.className='nb'}});
  var cls={{'cli':'on','resp':'on','urg':'on-urg','res':'on-res','cust':'on-cust'}};
  var nb=document.getElementById('nb-'+t); if(nb)nb.className='nb '+(cls[t]||'on');
  window.scrollTo(0,0);
}}
function filtrarRes(prefix,val){{
  document.querySelectorAll('[id^="'+prefix+'-"]').forEach(function(el){{el.style.display='none'}});
  var el=document.getElementById(prefix+'-'+val); if(el)el.style.display='block';
}}
function tog(i){{
  var s=document.getElementById('sec'+i);
  var c=document.getElementById('chev'+i);
  var open=s.style.display!=='none';
  s.style.display=open?'none':'block';
  c.textContent=open?'▶':'▼';
}}
window.onload=function(){{showTab('cli');dTab('cli')}};
</script></head><body>

<!-- ═══════════════════════════════════════════════ DESKTOP -->
<div id="dt">
  <div style="position:sticky;top:0;z-index:100">
  <div style="background:#0c0c0c;border-bottom:1px solid #1a1a1a;padding:14px 28px;display:flex;align-items:center;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:14px">
      <img src="/static/logo.png" style="height:46px;background:#fff;border-radius:8px;padding:4px 10px">
      <div>
        <span style="color:#ea580c;font-size:10px;font-weight:900;background:#1a0800;border:1px solid #ea580c;border-radius:4px;padding:2px 8px;letter-spacing:.5px">SUL</span>
        <div style="color:#6b4c30;font-size:11px;margin-top:4px">Painel de Chamados · {today_str}</div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:center">{dt_hdr_stats}</div>
  </div>
  <div style="background:#0a0a0a;border-bottom:1px solid #111;padding:8px 28px;display:flex;gap:8px;align-items:center">
    <span style="color:#4b5563;font-size:10px;font-weight:700;margin-right:4px">DIAS EM ABERTO:</span>
    <span style="background:#052e16;color:#4ade80;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">0-3d</span>
    <span style="background:#1c1a00;color:#fde047;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">4-7d</span>
    <span style="background:#1c0a00;color:#fb923c;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">8-14d</span>
    <span style="background:#1c0000;color:#f87171;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">15-30d</span>
    <span style="background:#150000;color:#ef4444;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">+30d</span>
  </div>
  <div style="background:#0c0c0c;border-bottom:1px solid #1a1a1a;padding:0 28px;display:flex">
    <button id="dtb-cli"  class="dtab on" onclick="dTab('cli')">Por Cliente</button>
    <button id="dtb-resp" class="dtab"    onclick="dTab('resp')">Por Responsável</button>
    <button id="dtb-cust" class="dtab"    onclick="dTab('cust')">Customizações {n_bklog}</button>
    <button id="dtb-urg"  class="dtab"    onclick="dTab('urg')">Urgentes do Dia {n_urg}</button>
    <button id="dtb-res"  class="dtab"    onclick="dTab('res')">Resultados {n_resol} hoje</button>
  </div>
  </div>
  <div style="padding:20px 28px">
    <div id="dv-cli" class="dview on">
      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px">{dt_cli_grid}</div>
      {dt_cli_details}
    </div>
    <div id="dv-resp" class="dview">
      <div style="color:#f97316;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:8px">🌿 EQUIPE SUL</div>
      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:12px">{dt_rsul_grid}</div>
      {dt_rsul_det}
      <div style="color:#a78bfa;font-size:10px;font-weight:700;letter-spacing:1px;margin:20px 0 8px">🏢 EQUIPE LOGUS</div>
      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:12px">{dt_rlogus_grid}</div>
      {dt_rlogus_det}
    </div>
    <div id="dv-cust" class="dview">
      <div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">
        <thead><tr style="border-bottom:2px solid #1f2937">
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">TICKET</th>
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">CLIENTE</th>
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">DESCRIÇÃO</th>
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">ESTIMATIVA</th>
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px">STATUS</th>
        </tr></thead>
        <tbody>{dt_cust_rows}</tbody>
      </table></div>
    </div>
    <div id="dv-urg" class="dview">{dt_urg_html}</div>
    <div id="dv-res" class="dview">{dt_res_html}</div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════ MOBILE -->
<div id="mob">
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
  <div id="v-res" class="view"><div class="sec-hdr">📊 RESULTADOS — {today_str}</div>{mob_res}</div>
  <div id="v-cust" class="view"><div class="sec-hdr">🔧 CUSTOMIZAÇÕES — {n_bklog} itens</div>{cust_html}</div>
</div>
<nav id="nav">
  <button class="nb on"  id="nb-cli"  onclick="showTab('cli')"><span class="ni">👥</span>Clientes</button>
  <button class="nb"     id="nb-resp" onclick="showTab('resp')"><span class="ni">👤</span>Responsável</button>
  <button class="nb"     id="nb-urg"  onclick="showTab('urg')"><span class="ni">🚨</span>Urgentes</button>
  <button class="nb"     id="nb-res"  onclick="showTab('res')"><span class="ni">📊</span>Resultados</button>
  <button class="nb"     id="nb-cust" onclick="showTab('cust')"><span class="ni">🔧</span>Customiz.</button>
</nav>
</div>

</body></html>"""
