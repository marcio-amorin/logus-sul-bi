from datetime import date, datetime, timezone, timedelta
from collections import defaultdict
import math, unicodedata, json

def _pnorm(s):
    """Normaliza string de prioridade removendo acentos e lowercasing."""
    return unicodedata.normalize('NFD', s).encode('ascii','ignore').decode('ascii').lower().strip()

def _hoje_brt():
    return datetime.now(timezone(timedelta(hours=-3))).date()

SUL_EMP = {
    'ANGELINA SUPERMERCADO',
    'BARATÃO',
    'BECLER',
    'BECKER SORVETERIA',
    'CASA DE CARNES PETRY',
    'CENTRAL FAMÍLIA',
    'DISTRIBOI',
    'DUKY LANCHES',
    'EMPÓRIO PETRY PRIME',
    'GRÃO PARÁ',
    'GUMZ',
    'JGB',
    'MAIS BRASIL - VAREJUS',
    'MANE FERRAGENS',
    'MARKET EXPRESS',
    'MERCADO DE BEBIDA POP',
    'MERCADO LEAL',
    'MILANI',
    'PARANA SUPERMERCADO',
    'RODRIGUES',
    'SCHUTZE',
    'SOL E MAR',
    'SUPER PRINCESA',
    'SUPERMERCADO KAIO',
    'SUPERMERCADO MATHEUS','Supermercado Matheus',
    'TILL DA CARNE',
    'TODO DIA',
    'VAREJUS',
    'VICARI',
    'YPE SUPERMERCADO',
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
URG_ERP  = {'25628','25647','25648','23301','24846','25173','24807'}
URG_DEV  = {'24760','24621','25368'}
URG_ALL  = URG_PDV | URG_ERP | URG_DEV
RESP_OWN = {'Comercial','Engenharia Software','Desenv. PDV','Sust. Desenv.','Sustentação Desenv.'}
BACKLOG = [{'num': 1, 'ticket': '21979', 'cliente': 'YPÊ', 'desc': 'Emissão de MDF-e', 'est': '16/03', 'status': 'Homologado'}, {'num': 2, 'ticket': '22206', 'cliente': 'YPÊ', 'desc': 'Emissão de NF para CPF com IE', 'est': '16/03', 'status': 'Homologado'}, {'num': 3, 'ticket': '12752', 'cliente': 'LEAL', 'desc': 'Adequação NT 2023.004', 'est': '31/03', 'status': 'Homologado'}, {'num': 4, 'ticket': '6197', 'cliente': 'VICARI', 'desc': 'Parametrização Custo no Balanço Comercial', 'est': '22/04', 'status': 'Em Homologação'}, {'num': 5, 'ticket': '24348', 'cliente': 'GUMZ JARAGUA', 'desc': 'Prazo de pagamento diferenciado por cliente', 'est': '04/05', 'status': 'Homologado'}, {'num': 6, 'ticket': '16783', 'cliente': 'LEAL', 'desc': 'Número do Pedido de Compras em Campo Específico', 'est': '05/05', 'status': 'Em Homologação'}, {'num': 7, 'ticket': '24705', 'cliente': 'LEAL', 'desc': 'ICMS ST retido no cálculo ICMS próprio', 'est': '11/05', 'status': 'Homologado'}, {'num': 8, 'ticket': '24839', 'cliente': 'GUMZ POMERODE', 'desc': 'Trazer produtos ativos por filial na pesquisa', 'est': '19/05', 'status': 'Homologado'}, {'num': 9, 'ticket': '17727', 'cliente': 'GUMZ JARAGUA', 'desc': 'Desconto em Forma de Recebimento', 'est': '14/05', 'status': 'Em Homologação'}, {'num': 10, 'ticket': '11753', 'cliente': 'GUMZ JARAGUA', 'desc': 'Relatório Contas a Receber', 'est': '25/05', 'status': 'Em Homologação'}, {'num': 11, 'ticket': '10223', 'cliente': 'ANGELINO', 'desc': 'Juros Acréscimo não lista na Manutenção de Recebimentos', 'est': '25/05', 'status': 'Em Homologação'}, {'num': 12, 'ticket': '16761', 'cliente': 'SCHUTZE', 'desc': 'Exibir dados históricos no pedido automático', 'est': '03/06', 'status': 'Em Homologação'}, {'num': 13, 'ticket': '12755', 'cliente': 'VICARI', 'desc': 'Crédito de Diferimento - Apuração e Preço de Venda', 'est': '24/07', 'status': 'Em Roadmap'}, {'num': 14, 'ticket': '16219', 'cliente': 'LEAL', 'desc': 'SPED FISCAL - Ajuste de Crédito', 'est': '24/07', 'status': 'Em Roadmap'}, {'num': 15, 'ticket': '6497', 'cliente': 'VICARI', 'desc': 'Baixas Uso/Consumo no Balanço Comercial', 'est': '03/07', 'status': 'Em Roadmap'}, {'num': 16, 'ticket': '20278', 'cliente': 'VICARI', 'desc': 'ICMS Desonerado na Entrada da NF', 'est': '04/09', 'status': 'Em Roadmap'}, {'num': 17, 'ticket': '20484', 'cliente': 'ANGELINO', 'desc': 'Campo Juros Baixa Recebimento', 'est': '', 'status': 'Pendente'}, {'num': 18, 'ticket': '4255', 'cliente': 'PRINCESA', 'desc': 'Troco Solidário', 'est': '', 'status': 'Pendente'}, {'num': 19, 'ticket': '6451', 'cliente': 'PRINCESA', 'desc': 'Emissão Notas Fiscais a partir do PDV', 'est': '', 'status': 'Pendente'}, {'num': 20, 'ticket': '16782', 'cliente': 'LEAL', 'desc': 'Venda a Órgão Público com Retenção do IRRF', 'est': '', 'status': 'Pendente'}, {'num': 21, 'ticket': '23172', 'cliente': 'LEAL', 'desc': 'Sistema não considerando ICMS desonerado', 'est': '', 'status': 'Pendente'}, {'num': 22, 'ticket': '22787', 'cliente': 'LEAL', 'desc': 'Erro ao finalizar NF (#1)', 'est': '', 'status': 'Pendente'}, {'num': 23, 'ticket': '23568', 'cliente': 'LEAL', 'desc': 'Erro ao finalizar NF (#2)', 'est': '', 'status': 'Pendente'}, {'num': 24, 'ticket': '19372', 'cliente': 'LEAL', 'desc': 'Venda para cliente fora do estado', 'est': '', 'status': 'Pendente'}, {'num': 25, 'ticket': '21652', 'cliente': 'LEAL', 'desc': 'Formas de Recebimento - Boleto', 'est': '', 'status': 'Pendente'}, {'num': 26, 'ticket': '25271', 'cliente': 'MILANI', 'desc': 'Filtro de seleção de NF na alteração de preços', 'est': '', 'status': 'Pendente'}, {'num': 27, 'ticket': '22981', 'cliente': 'SCHUTZE', 'desc': 'Seleção de nota em documentos de devolução', 'est': '', 'status': 'Pendente'}, {'num': 28, 'ticket': '25443', 'cliente': 'GUMZ', 'desc': 'Parâmetros PDV – Operações que Exigem Supervisor', 'est': 'URGENTE', 'status': 'Urgente'}, {'num': 29, 'ticket': '24134', 'cliente': 'LEAL', 'desc': 'Limitação Logus PDV – ausência de observação na NF-e', 'est': '', 'status': 'Pendente'}]

# ── shared helpers ────────────────────────────────────────────────────────────

def _dc(d):
    if d<=3:  return '#16a34a','#dcfce7'
    if d<=7:  return '#ca8a04','#fef9c3'
    if d<=14: return '#ea580c','#fff7ed'
    if d<=30: return '#dc2626','#fee2e2'
    return '#991b1b','#fee2e2'

def _sbadge(s):
    m = {'Novo':('16a34a','dcfce7','NOVO'),'Em andamento':('2563eb','dbeafe','EM ANDAMENTO'),'Aguardando':('d97706','fef3c7','AGUARDANDO')}
    c,bg,l = m.get(s,('64748b','f1f5f9',s.upper()))
    return f'<span style="color:#{c};background:#{bg};font-size:10px;font-weight:700;border-radius:4px;padding:3px 8px">{l}</span>'

def _ticon(t):
    return {'Incidente':'🔴','Requisição':'🔵','Dúvida':'🟣'}.get(t,'⚪')

# ── mobile helpers ────────────────────────────────────────────────────────────

def _tk(t, sc=True):
    fc,bg = _dc(t['dias'])
    cli = f'<div style="color:#ea580c;font-size:15px;font-weight:800;margin-bottom:6px">{t["empresa"]}</div>' if sc else ''
    # badges extras do Excel
    extras = ''
    if t.get('sla_venceu'):
        extras += '<span style="background:#fee2e2;color:#b91c1c;font-size:10px;font-weight:800;border-radius:4px;padding:2px 7px;margin-right:4px">⏰ SLA</span>'
    if t.get('abandonado'):
        extras += '<span style="background:#f3f4f6;color:#6b7280;font-size:10px;font-weight:800;border-radius:4px;padding:2px 7px;margin-right:4px">🔕 Abandonado</span>'
    dias_mov = t.get('dias_sem_mov', 0)
    if dias_mov >= 2:
        mc = '#dc2626' if dias_mov > 14 else '#d97706' if dias_mov > 7 else '#64748b'
        extras += f'<span style="background:#f8fafc;color:{mc};font-size:10px;font-weight:800;border-radius:4px;padding:2px 7px">↩ {dias_mov}d s/mov</span>'
    elif dias_mov == 1:
        extras += '<span style="background:#dcfce7;color:#16a34a;font-size:10px;font-weight:800;border-radius:4px;padding:2px 7px">✓ 1d</span>'
    else:
        extras += '<span style="background:#dcfce7;color:#16a34a;font-size:10px;font-weight:800;border-radius:4px;padding:2px 7px">✓ hoje</span>'
    return (f'<div style="background:#ffffff;border-radius:12px;padding:14px 16px;margin-bottom:10px;border-left:6px solid {fc};box-shadow:0 3px 10px rgba(0,0,0,0.1)">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
            f'<span style="color:{fc};font-size:20px;font-weight:900">#{t["code"]}</span>'
            f'<span style="background:{bg};color:{fc};font-size:18px;font-weight:900;padding:4px 12px;border-radius:8px;border:1px solid {fc}33">{t["dias"]}d</span></div>'
            f'{cli}'
            f'<div style="color:#111827;font-size:14px;font-weight:600;line-height:1.5;margin-bottom:10px">{_ticon(t["tipo"])} {t["assunto"]}</div>'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">'
            f'<span style="color:#374151;font-size:13px;font-weight:700">{t["atrib"]}</span>'
            f'{_sbadge(t["status"])}</div>'
            +(f'<div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px">{extras}</div>' if extras else '')
            +'</div>')

def _csec(emp, tks, idx):
    tks_s = sorted(tks, key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias']))
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc, _ = _dc(mx)
    inc_tag = f'<span style="color:#dc2626;font-size:10px;font-weight:900;margin-right:4px">⚠{inc}</span>' if inc else ''
    cards = ''.join(_tk(t, sc=False) for t in tks_s)
    return (
        f'<div style="margin-bottom:4px;border-radius:10px;overflow:hidden;border:1px solid #d1d5db;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
        f'<div onclick="tog({idx})" style="background:#ffffff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;min-height:46px">'
        f'<span style="color:#111827;font-size:15px;font-weight:800;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-right:8px">{emp}</span>'
        f'<div style="display:flex;align-items:center;gap:6px;flex-shrink:0">'
        f'{inc_tag}'
        f'<span style="color:#374151;font-size:12px;font-weight:700">{len(tks)}ch</span>'
        f'<span style="color:{fc};font-size:13px;font-weight:900;min-width:32px;text-align:right">{mx}d</span>'
        f'<span id="chev{idx}" style="color:#64748b;font-size:13px;margin-left:4px">▶</span>'
        f'</div></div>'
        f'<div id="sec{idx}" style="display:none;padding:10px;background:#f8fafc">{cards}</div>'
        f'</div>'
    )

def _rsec(resp, tks, idx, cor='#ea580c'):
    tks_s = sorted(tks, key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias']))
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc, _ = _dc(mx)
    inc_tag = f'<span style="color:#dc2626;font-size:10px;font-weight:900;margin-right:4px">⚠{inc}</span>' if inc else ''
    cards = ''.join(_tk(t, sc=True) for t in tks_s)
    return (
        f'<div style="margin-bottom:4px;border-radius:10px;overflow:hidden;border:1px solid #d1d5db;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
        f'<div onclick="tog({idx})" style="background:#ffffff;padding:12px 14px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;min-height:46px">'
        f'<span style="color:{cor};font-size:15px;font-weight:800;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-right:8px">{resp}</span>'
        f'<div style="display:flex;align-items:center;gap:6px;flex-shrink:0">'
        f'{inc_tag}'
        f'<span style="color:#374151;font-size:12px;font-weight:700">{len(tks)}ch</span>'
        f'<span style="color:{fc};font-size:13px;font-weight:900;min-width:32px;text-align:right">{mx}d</span>'
        f'<span id="chev{idx}" style="color:#64748b;font-size:13px;margin-left:4px">▶</span>'
        f'</div></div>'
        f'<div id="sec{idx}" style="display:none;padding:10px;background:#f8fafc">{cards}</div>'
        f'</div>'
    )

def _ugrp(titulo, cor, bg, tks, sc=True, uid=None):
    if not tks: return ''
    cards = ''.join(_tk(t, sc=sc) for t in sorted(tks, key=lambda x:-x['dias']))
    if uid is None:
        return (f'<div style="margin-bottom:16px">'
                f'<div style="background:{bg};border-left:4px solid {cor};border-radius:8px;padding:10px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center">'
                f'<span style="color:{cor};font-size:13px;font-weight:900">{titulo}</span>'
                f'<span style="color:{cor};font-size:20px;font-weight:900">{len(tks)}</span></div>'
                f'{cards}</div>')
    return (
        f'<div style="margin-bottom:6px;border-radius:10px;overflow:hidden;border:2px solid {cor}44;box-shadow:0 2px 8px {cor}18">'
        f'<div onclick="tog(\'{uid}\')" style="background:{bg};border-left:6px solid {cor};padding:12px 14px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;min-height:46px">'
        f'<span style="color:{cor};font-size:15px;font-weight:900">{titulo}</span>'
        f'<div style="display:flex;align-items:center;gap:8px">'
        f'<span style="color:{cor};font-size:24px;font-weight:900">{len(tks)}</span>'
        f'<span id="chev{uid}" style="color:{cor};font-size:14px">▶</span>'
        f'</div></div>'
        f'<div id="sec{uid}" style="display:none;padding:10px;background:#f8fafc">{cards}</div>'
        f'</div>'
    )

def _ccard(b):
    s = b['status']
    cor = {'Urgente':'#b91c1c','Homologado':'#15803d','Em Homologação':'#c2410c','Em Roadmap':'#1d4ed8'}.get(s,'#475569')
    bg  = {'Urgente':'#fef2f2','Homologado':'#f0fdf4','Em Homologação':'#fff7ed','Em Roadmap':'#eff6ff'}.get(s,'#f8fafc')
    return (f'<div style="background:{bg};border-radius:10px;padding:12px 14px;margin-bottom:8px;border-left:4px solid {cor}">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
            f'<span style="color:#ea580c;font-size:15px;font-weight:900">#{b["ticket"]}</span>'
            f'<span style="color:{cor};background:{bg};font-size:10px;font-weight:700;border:1px solid {cor};border-radius:4px;padding:2px 8px">{s.upper()}</span></div>'
            f'<div style="color:#92400e;font-size:12px;font-weight:700;margin-bottom:4px">{b["cliente"]}</div>'
            f'<div style="color:#1e293b;font-size:13px;line-height:1.4">{b["desc"]}</div>'
            +(f'<div style="color:{cor};font-size:11px;font-weight:700;margin-top:6px">Est.: {b["est"]}</div>' if b['est'] else '')
            +'</div>')

def _bar(lbl, v, tot, cor):
    pct = int(v/tot*100) if tot else 0
    return (f'<div style="margin-bottom:14px">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:5px">'
            f'<span style="color:#374151;font-size:13px">{lbl}</span>'
            f'<span style="color:{cor};font-size:16px;font-weight:900">{v} <span style="color:#64748b;font-size:11px;font-weight:700">{pct}%</span></span></div>'
            f'<div style="background:#e2e8f0;border-radius:6px;height:10px"><div style="width:{pct}%;background:{cor};height:100%;border-radius:6px"></div></div></div>')

# ── desktop helpers ───────────────────────────────────────────────────────────

def _d_safe(s):
    return ''.join(c if c.isalnum() else '_' for c in s)

def _d_stat(label, val, cor, tab=''):
    click = f' onclick="dTab(\'{tab}\')" title="Ir para {label}"' if tab else ''
    return (f'<div class="dstat"{click} style="background:{cor}0d;border:2px solid {cor}55;border-top:3px solid {cor};border-radius:10px;padding:10px 20px;text-align:center;min-width:100px;box-shadow:0 2px 8px {cor}22">'
            f'<div style="color:{cor};font-size:34px;font-weight:900;line-height:1.1">{val}</div>'
            f'<div style="color:#374151;font-size:11px;font-weight:800;margin-top:5px;letter-spacing:.5px">{label}</div></div>')

def _d_row(t, show_cli=False):
    fc,_ = _dc(t['dias'])
    tipo = t['tipo'] or '—'
    tc = '#ef4444' if t['tipo']=='Incidente' else '#3b82f6' if t['tipo']=='Requisição' else '#6b7280'
    ec = {'Novo':'#22c55e','Em andamento':'#3b82f6','Aguardando':'#d97706','Resolvido':'#22c55e','Fechado':'#22c55e'}.get(t['status'],'#6b7280')
    cli = f'<td style="color:#ea580c;font-size:12px;font-weight:700;padding:9px 12px;white-space:nowrap">{t["empresa"]}</td>' if show_cli else ''
    url = f'https://logusretail.tolvdesk.com/webapp/#/tickets/{t["code"]}'
    # badges extras
    sla_tag = '<span style="background:#fee2e2;color:#b91c1c;font-size:9px;font-weight:900;border-radius:3px;padding:1px 5px;margin-left:4px">SLA</span>' if t.get('sla_venceu') else ''
    abnd_tag = '<span style="background:#f3f4f6;color:#6b7280;font-size:9px;font-weight:900;border-radius:3px;padding:1px 5px;margin-left:4px">ABN</span>' if t.get('abandonado') else ''
    dias_mov = t.get('dias_sem_mov', 0)
    if dias_mov >= 2:
        mc = '#dc2626' if dias_mov > 14 else '#d97706' if dias_mov > 7 else '#64748b'
        smov_td = f'<td style="color:{mc};font-weight:800;padding:9px 8px;font-size:12px;text-align:right;white-space:nowrap">{dias_mov}d</td>'
    elif dias_mov == 1:
        smov_td = '<td style="color:#16a34a;font-weight:700;padding:9px 8px;font-size:11px;text-align:right;white-space:nowrap">✓ 1d</td>'
    else:
        smov_td = '<td style="color:#16a34a;font-weight:700;padding:9px 8px;font-size:11px;text-align:right;white-space:nowrap">✓ hoje</td>'
    return (f'<tr style="border-bottom:1px solid #f1f5f9">'
            f'<td style="color:#ea580c;font-weight:900;padding:9px 12px;white-space:nowrap">#{t["code"]}{sla_tag}{abnd_tag}</td>'
            f'{cli}'
            f'<td style="padding:9px 12px"><span style="background:{tc}22;color:{tc};border-radius:4px;padding:3px 8px;font-size:10px;font-weight:900">{tipo.upper()}</span></td>'
            f'<td style="color:#111827;padding:9px 12px;font-size:13px;font-weight:500">{t["assunto"]}</td>'
            f'<td style="padding:9px 12px"><span style="background:{ec}22;color:{ec};border-radius:4px;padding:3px 8px;font-size:10px;font-weight:900">{t["status"].upper()}</span></td>'
            f'<td style="color:#374151;padding:9px 12px;font-size:12px;font-weight:600;white-space:nowrap">{t["atrib"]}</td>'
            f'<td style="color:#64748b;padding:9px 12px;font-size:12px;white-space:nowrap">{t["data"]}</td>'
            f'<td style="color:{fc};font-weight:900;padding:9px 12px;text-align:right;white-space:nowrap">{t["dias"]}</td>'
            f'{smov_td}'
            f'<td style="padding:9px 8px;white-space:nowrap">'
            f'<button onclick="abrirTk(\'{t["code"]}\',this)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:4px 10px;font-size:11px;font-weight:700;cursor:pointer;white-space:nowrap">📋 #{t["code"]}</button>'
            f'</td></tr>')

def _d_tbl_hdr(show_cli=False):
    cli = '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">CLIENTE</th>' if show_cli else ''
    return ('<thead><tr style="border-bottom:2px solid #e2e8f0">'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">TICKET</th>'
            f'{cli}'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">TIPO</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">ASSUNTO</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">ESTADO</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">COM QUEM</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">ABERTURA</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:right;padding:8px 12px;background:#f8fafc">DIAS</th>'
            '<th style="color:#475569;font-size:10px;font-weight:700;text-align:right;padding:8px 8px;background:#f8fafc">S/MOV</th>'
            '<th style="background:#f8fafc;padding:8px 8px"></th>'
            '</tr></thead>')

def _d_clibox(emp, tks):
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc,_ = _dc(mx)
    sid = _d_safe(emp)
    itag = f'<div style="color:#dc2626;font-size:11px;margin-top:2px">⚠ {inc} inc</div>' if inc else ''
    return (f'<div class="dcbox" data-id="{sid}" onclick="dCli(\'{sid}\')" '
            f'style="border:2px solid #e2e8f0;border-radius:10px;padding:14px 16px;cursor:pointer;background:#ffffff;min-width:140px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">'
            f'<div style="color:#ea580c;font-size:14px;font-weight:900;margin-bottom:4px">{emp}</div>'
            f'<div style="color:#1e293b;font-size:13px;font-weight:700">{len(tks)} tickets</div>'
            f'{itag}'
            f'<div style="color:{fc};font-size:15px;font-weight:900;margin-top:6px">{mx}d</div></div>')

def _d_respbox(resp, tks, cor):
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc,_ = _dc(mx)
    sid = _d_safe(resp)
    itag = f'<div style="color:#dc2626;font-size:11px;margin-top:2px">⚠ {inc} inc</div>' if inc else ''
    return (f'<div class="drbox" onclick="dResp(\'{sid}\')" '
            f'style="border:2px solid #e2e8f0;border-radius:10px;padding:14px 16px;cursor:pointer;background:#ffffff;min-width:160px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">'
            f'<div style="color:{cor};font-size:14px;font-weight:900;margin-bottom:4px">{resp}</div>'
            f'<div style="color:#1e293b;font-size:13px;font-weight:700">{len(tks)} chamados</div>'
            f'{itag}'
            f'<div style="color:{fc};font-size:15px;font-weight:900;margin-top:6px">{mx}d</div></div>')

def _d_detail(label, tks, div_id, close_fn):
    inc = sum(1 for t in tks if t['tipo']=='Incidente')
    mx  = max(t['dias'] for t in tks) if tks else 0
    fc,_ = _dc(mx)
    resps = sorted(set(t['atrib'] for t in tks))
    rtags = ''.join(f'<span style="background:#fff7ed;color:#ea580c;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700;margin-right:6px">{r}</span>' for r in resps)
    rows  = ''.join(_d_row(t, show_cli=True) for t in sorted(tks, key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias'])))
    ispn  = f'<span style="color:#dc2626;font-size:12px">⚠ {inc} inc</span> ' if inc else ''
    return (f'<div id="{div_id}" class="ddet" style="display:none;background:#ffffff;border:1px solid #e2e8f0;border-radius:8px;margin-top:10px;padding:16px 20px;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:10px">'
            f'<div style="display:flex;align-items:center;gap:14px">'
            f'<span style="color:#ea580c;font-size:16px;font-weight:900">{label}</span>'
            f'<span style="color:#374151;font-size:12px">{len(tks)} chamados</span>'
            f'{ispn}<span style="color:{fc};font-size:13px;font-weight:700">{mx}d</span></div>'
            f'<button onclick="{close_fn}" style="background:none;border:1px solid #e2e8f0;color:#64748b;border-radius:4px;padding:4px 10px;cursor:pointer;font-size:11px">✕ fechar</button>'
            f'</div>'
            f'<div style="margin-bottom:12px">{rtags}</div>'
            f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">'
            f'{_d_tbl_hdr(show_cli=True)}<tbody>{rows}</tbody></table></div></div>')

def _d_urg_sec(titulo, cor, bg, tks):
    if not tks: return ''
    rows = ''.join(_d_row(t, show_cli=True) for t in sorted(tks, key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias'])))
    return (f'<div style="margin-bottom:24px;background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 3px 12px rgba(0,0,0,0.08)">'
            f'<div style="background:{bg};border-left:6px solid {cor};padding:14px 18px;display:flex;align-items:center;gap:14px">'
            f'<span style="color:{cor};font-size:15px;font-weight:900">{titulo}</span>'
            f'<span style="color:{cor};font-size:30px;font-weight:900;line-height:1">{len(tks)}</span></div>'
            f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">'
            f'{_d_tbl_hdr(show_cli=True)}<tbody>{rows}</tbody></table></div></div>')

def _ugrp_por_cli(titulo, cor, bg, tks, uid='ugp'):
    """Seção mobile com tickets agrupados por cliente — cada cliente colapsável."""
    if not tks: return ''
    by_emp = defaultdict(list)
    for t in tks:
        by_emp[t['empresa']].append(t)
    clientes_ord = sorted(by_emp.keys(), key=lambda e: -max(t['dias'] for t in by_emp[e]))
    inner = ''
    for emp in clientes_ord:
        emp_tks = sorted(by_emp[emp], key=lambda x: (0 if x['tipo']=='Incidente' else 1, -x['dias']))
        inc = sum(1 for t in emp_tks if t['tipo']=='Incidente')
        mx  = max(t['dias'] for t in emp_tks)
        fc, _ = _dc(mx)
        cid = uid + '_' + ''.join(c if c.isalnum() else '_' for c in emp)
        inc_tag = f'<span style="color:#dc2626;font-size:10px;font-weight:900;margin-right:4px">⚠{inc}</span>' if inc else ''
        cards = ''.join(_tk(t, sc=False) for t in emp_tks)
        inner += (
            f'<div style="margin-bottom:2px;border-radius:7px;overflow:hidden;border:1px solid #e2e8f0">'
            f'<div onclick="tog(\'{cid}\')" style="background:#ffffff;padding:9px 12px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;min-height:40px">'
            f'<span style="color:#1e293b;font-size:13px;font-weight:700;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-right:8px">{emp}</span>'
            f'<div style="display:flex;align-items:center;gap:6px;flex-shrink:0">'
            f'{inc_tag}'
            f'<span style="color:#374151;font-size:11px">{len(emp_tks)}ch</span>'
            f'<span style="color:{fc};font-size:11px;font-weight:700;min-width:32px;text-align:right">{mx}d</span>'
            f'<span id="chev{cid}" style="color:#64748b;font-size:12px;margin-left:4px">▶</span>'
            f'</div></div>'
            f'<div id="sec{cid}" style="display:none;padding:10px;background:#f8fafc">{cards}</div>'
            f'</div>'
        )
    return (
        f'<div style="margin-bottom:3px;border-radius:8px;overflow:hidden;border:1px solid #e2e8f0">'
        f'<div onclick="tog(\'{uid}\')" style="background:{bg};border-left:4px solid {cor};padding:10px 14px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;min-height:42px">'
        f'<span style="color:{cor};font-size:13px;font-weight:900">{titulo}</span>'
        f'<div style="display:flex;align-items:center;gap:8px">'
        f'<span style="color:{cor};font-size:16px;font-weight:900">{len(tks)}</span>'
        f'<span id="chev{uid}" style="color:{cor};font-size:12px">▶</span>'
        f'</div></div>'
        f'<div id="sec{uid}" style="display:none;padding:8px;background:#f8fafc">{inner}</div>'
        f'</div>'
    )

def _d_urg_por_cli(titulo, cor, bg, tks):
    """Seção desktop com tickets agrupados por cliente."""
    if not tks: return ''
    by_emp = defaultdict(list)
    for t in tks:
        by_emp[t['empresa']].append(t)
    clientes_ord = sorted(by_emp.keys(), key=lambda e: -max(t['dias'] for t in by_emp[e]))
    rows = ''
    for emp in clientes_ord:
        emp_tks = sorted(by_emp[emp], key=lambda x: (0 if x['tipo']=='Incidente' else 1, -x['dias']))
        mx = max(t['dias'] for t in emp_tks)
        fc, _ = _dc(mx)
        rows += (f'<tr><td colspan="7" style="padding:8px 12px;background:#f8fafc;border-top:2px solid #e2e8f0">'
                 f'<span style="color:{fc};font-size:12px;font-weight:900">{emp}</span>'
                 f'<span style="color:#374151;font-size:11px;margin-left:10px">{len(emp_tks)} chamados · {mx}d</span>'
                 f'</td></tr>')
        rows += ''.join(_d_row(t, show_cli=False) for t in emp_tks)
    return (f'<div style="margin-bottom:24px;background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 3px 12px rgba(0,0,0,0.08)">'
            f'<div style="background:{bg};border-left:6px solid {cor};padding:14px 18px;display:flex;align-items:center;gap:14px">'
            f'<span style="color:{cor};font-size:15px;font-weight:900">{titulo}</span>'
            f'<span style="color:{cor};font-size:30px;font-weight:900;line-height:1">{len(tks)}</span></div>'
            f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">'
            f'{_d_tbl_hdr(show_cli=False)}<tbody>{rows}</tbody></table></div></div>')

def _d_kpi_big(label, val, cor, sub=''):
    sub_html = f'<div style="color:#64748b;font-size:11px;font-weight:700;margin-top:4px">{sub}</div>' if sub else ''
    return (f'<div style="background:{cor}0d;border:2px solid {cor}44;border-top:4px solid {cor};border-radius:12px;padding:18px 22px;flex:1;min-width:120px;box-shadow:0 3px 12px {cor}22">'
            f'<div style="color:{cor};font-size:52px;font-weight:900;line-height:1;font-variant-numeric:tabular-nums">{val}</div>'
            f'<div style="color:#374151;font-size:12px;font-weight:800;letter-spacing:.8px;margin-top:10px;text-transform:uppercase">{label}</div>'
            f'{sub_html}</div>')

def _d_exec_bar_chart(by_cli, clientes):
    """SVG horizontal bar chart — top clientes por tickets."""
    sorted_cli = sorted(clientes, key=lambda c: -len(by_cli[c]))[:14]
    if not sorted_cli: return ''
    max_cnt = max(len(by_cli[c]) for c in sorted_cli) or 1
    COLORS = ['#f97316','#fb923c','#fbbf24','#ef4444','#a78bfa','#34d399',
              '#60a5fa','#f472b6','#4ade80','#38bdf8','#c084fc','#facc15','#fd7c55','#84cc16']
    lbl_w = 175; bar_max = 260; row_h = 30; pad = 10
    h = len(sorted_cli) * row_h + pad * 2
    w = lbl_w + bar_max + 55
    parts = []
    for i, cli in enumerate(sorted_cli):
        cnt = len(by_cli[cli])
        inc = sum(1 for t in by_cli[cli] if t['tipo'] == 'Incidente')
        bw  = max(4, int(bar_max * cnt / max_cnt))
        y   = pad + i * row_h
        cor = COLORS[i % len(COLORS)]
        lbl = (cli[:24]+'…') if len(cli) > 24 else cli
        inc_txt = f' <tspan fill="#dc2626" font-size="10">+{inc}inc</tspan>' if inc else ''
        parts.append(
            f'<text x="{lbl_w-8}" y="{y+18}" text-anchor="end" fill="#1e293b" font-size="11" font-weight="600" font-family="sans-serif">{lbl}</text>'
            f'<rect x="{lbl_w}" y="{y+5}" width="{bw}" height="18" rx="4" fill="{cor}" opacity=".82"/>'
            f'<text x="{lbl_w+bw+8}" y="{y+18}" fill="{cor}" font-size="12" font-weight="bold" font-family="sans-serif">{cnt}{inc_txt}</text>'
        )
    return f'<svg width="100%" viewBox="0 0 {w} {h}" style="display:block">{"".join(parts)}</svg>'

def _d_donut_chart(by_cli, clientes):
    total = sum(len(by_cli[c]) for c in clientes)
    if total == 0 or not clientes:
        return ''
    COLORS = ['#f97316','#ef4444','#fbbf24','#a78bfa','#34d399','#60a5fa',
              '#fb923c','#f472b6','#4ade80','#38bdf8','#c084fc','#facc15',
              '#2dd4bf','#f87171','#818cf8','#e879f9','#86efac','#fda4af']
    sorted_cli = sorted(clientes, key=lambda c: -len(by_cli[c]))
    cx = cy = 120; R = 104; r = 56; GAP = 1.8
    paths = []; angle = -90.0
    for i, cli in enumerate(sorted_cli):
        cnt = len(by_cli[cli])
        pct = cnt / total
        sweep = max(360 * pct - GAP, 0.5)
        color = COLORS[i % len(COLORS)]
        sr = math.radians(angle); er = math.radians(angle + sweep)
        x1 = cx + R*math.cos(sr); y1 = cy + R*math.sin(sr)
        x2 = cx + R*math.cos(er); y2 = cy + R*math.sin(er)
        x3 = cx + r*math.cos(er); y3 = cy + r*math.sin(er)
        x4 = cx + r*math.cos(sr); y4 = cy + r*math.sin(sr)
        lg = 1 if sweep > 180 else 0
        d = (f'M{x1:.2f} {y1:.2f} A{R} {R} 0 {lg} 1 {x2:.2f} {y2:.2f} '
             f'L{x3:.2f} {y3:.2f} A{r} {r} 0 {lg} 0 {x4:.2f} {y4:.2f} Z')
        inc = sum(1 for t in by_cli[cli] if t['tipo'] == 'Incidente')
        tip = f'{cli} · {cnt} tickets ({pct*100:.1f}%)' + (f' · {inc} incidentes' if inc else '')
        paths.append(f'<path class="dslice" d="{d}" fill="{color}" stroke="#f1f5f9" stroke-width="2"><title>{tip}</title></path>')
        angle += sweep + GAP
    svg = (f'<svg width="240" height="240" viewBox="0 0 240 240" style="display:block;flex-shrink:0">'
           f'<style>.dslice{{opacity:.85;transition:opacity .15s,filter .15s}}.dslice:hover{{opacity:1;filter:brightness(1.3)}}</style>'
           + ''.join(paths)
           + f'<text x="{cx}" y="{cy-8}" text-anchor="middle" fill="#ea580c" font-size="26" font-weight="900" font-family="Segoe UI,sans-serif">{total}</text>'
           + f'<text x="{cx}" y="{cy+10}" text-anchor="middle" fill="#374151" font-size="10" font-weight="700" font-family="Segoe UI,sans-serif" letter-spacing="1">TICKETS</text>'
           + f'<text x="{cx}" y="{cy+24}" text-anchor="middle" fill="#374151" font-size="10" font-weight="600" font-family="Segoe UI,sans-serif">{len(clientes)} clientes</text>'
           + '</svg>')
    top_cli = sorted_cli[0];  top_pct = len(by_cli[top_cli]) / total * 100
    bot_cli = sorted_cli[-1]; bot_pct = len(by_cli[bot_cli]) / total * 100
    # callout no topo, largura total
    callout = (f'<div style="display:flex;gap:10px;margin-bottom:14px">'
               f'<div style="background:#fff7ed;border:1px solid #ea580c;border-radius:6px;padding:8px 14px;flex:1">'
               f'<div style="color:#374151;font-size:9px;font-weight:700;letter-spacing:.5px">MAIOR CONCENTRAÇÃO</div>'
               f'<div style="color:#ea580c;font-size:20px;font-weight:900;margin-top:2px">{top_pct:.1f}%</div>'
               f'<div style="color:#b45309;font-size:11px;font-weight:700">{top_cli}</div></div>'
               f'<div style="background:#f0fdf4;border:1px solid #16a34a;border-radius:6px;padding:8px 14px;flex:1">'
               f'<div style="color:#374151;font-size:9px;font-weight:700;letter-spacing:.5px">MENOR CONCENTRAÇÃO</div>'
               f'<div style="color:#16a34a;font-size:20px;font-weight:900;margin-top:2px">{bot_pct:.1f}%</div>'
               f'<div style="color:#15803d;font-size:11px;font-weight:700">{bot_cli}</div></div></div>')
    legend_rows = ''
    for i, cli in enumerate(sorted_cli):
        cnt = len(by_cli[cli]); pct = cnt / total * 100
        color = COLORS[i % len(COLORS)]
        inc = sum(1 for t in by_cli[cli] if t['tipo'] == 'Incidente')
        bw = int(pct * 1.7)
        inc_tag = f'<span style="color:#dc2626;font-size:10px"> ⚠{inc}</span>' if inc else ''
        legend_rows += (f'<div style="margin-bottom:9px">'
                        f'<div style="display:flex;align-items:center;gap:7px;margin-bottom:3px">'
                        f'<div style="width:9px;height:9px;border-radius:2px;background:{color};flex-shrink:0"></div>'
                        f'<span style="color:#1e293b;font-size:11px;font-weight:700;flex:1">{cli}</span>'
                        f'<span style="color:{color};font-size:12px;font-weight:900">{pct:.1f}%</span>'
                        f'<span style="color:#94a3b8;font-size:10px;margin-left:4px">{cnt}tk{inc_tag}</span></div>'
                        f'<div style="background:#e2e8f0;border-radius:3px;height:4px">'
                        f'<div style="width:{min(bw,170)}px;background:{color};height:100%;border-radius:3px"></div></div></div>')
    return (f'<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:18px 22px;margin-top:14px;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
            f'<div style="color:#374151;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:14px">DISTRIBUIÇÃO POR CLIENTE</div>'
            f'{callout}'
            f'<div style="display:flex;gap:20px;align-items:flex-start">'
            f'{svg}'
            f'<div style="flex:1;min-width:180px;max-height:240px;overflow-y:auto;padding-right:6px">'
            f'<div style="color:#374151;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:10px">TODOS OS CLIENTES</div>'
            f'{legend_rows}</div></div></div>')

def _priority_panel_html(tk_lkp, baixados_by_code, urg_pdv=None, urg_erp=None, prefix='prp'):
    groups = [
        ('🟢 PDV — Urgente',      '#15803d', '#f0fdf4', urg_pdv or URG_PDV),
        ('🔴 ERP — Urgente',      '#b91c1c', '#fef2f2', urg_erp or URG_ERP),
        ('💻 Dev / Sustentação',  '#6d28d9', '#f5f3ff', URG_DEV),
    ]
    html = '<div style="margin-bottom:16px;background:#ffffff;border:1px solid #e2e8f0;border-radius:10px;padding:12px 14px;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
    html += '<div style="color:#ea580c;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:10px;background:#ea580c;color:#fff;border-radius:6px;padding:6px 12px">🎯 ACOMPANHAMENTO DE PRIORIDADES</div>'
    for i, (titulo, cor, bg, codes) in enumerate(groups):
        uid = f'{prefix}{i}'
        res_c = sum(1 for c in codes if c in baixados_by_code)
        tot_c = len(codes)
        all_done = res_c == tot_c
        sbadge = ('<span style="background:#f0fdf4;color:#15803d;border-radius:4px;padding:2px 7px;font-size:10px;font-weight:900">✅ OK</span>'
                  if all_done else
                  f'<span style="color:{cor};font-size:11px;font-weight:700">{res_c}/{tot_c}</span>')
        tickets_html = ''
        for code in sorted(codes):
            t     = tk_lkp.get(code)
            assunto = (t['assunto'] if t else f'Ticket #{code}')[:80]
            empresa = t['empresa'] if t else '—'
            res_t = baixados_by_code.get(code)
            if res_t:
                rbadge = f'<span style="color:#15803d;font-size:10px;font-weight:900;white-space:nowrap">✅ {res_t.get("resolucao","")}</span>'
            else:
                st = (t['status'] if t else '—') or '—'
                at = (t['atrib']  if t else '—') or '—'
                rbadge = f'<span style="color:#dc2626;font-size:10px;font-weight:700;white-space:nowrap">⏳ {st}</span>'
            tickets_html += (
                f'<div style="display:flex;align-items:flex-start;gap:8px;padding:7px 10px;border-bottom:1px solid #f1f5f9;flex-wrap:wrap">'
                f'<span style="color:#ea580c;font-size:12px;font-weight:900;min-width:54px">#{code}</span>'
                f'<span style="color:#92400e;font-size:11px;font-weight:700;white-space:nowrap">{empresa}</span>'
                f'<span style="color:#374151;font-size:11px;flex:1;min-width:100px">{assunto}</span>'
                f'{rbadge}</div>'
            )
        html += (
            f'<div style="margin-bottom:3px;border-radius:6px;overflow:hidden;border:1px solid #e2e8f0">'
            f'<div onclick="tog(\'{uid}\')" style="background:{bg};border-left:4px solid {cor};padding:9px 12px;display:flex;align-items:center;justify-content:space-between;cursor:pointer">'
            f'<span style="color:{cor};font-size:12px;font-weight:900">{titulo}</span>'
            f'<div style="display:flex;align-items:center;gap:8px">'
            f'{sbadge}'
            f'<span id="chev{uid}" style="color:{cor};font-size:12px;margin-left:4px">▶</span>'
            f'</div></div>'
            f'<div id="sec{uid}" style="display:none;background:#f8fafc">{tickets_html}</div>'
            f'</div>'
        )
    html += '</div>'
    return html

# ── main ──────────────────────────────────────────────────────────────────────

def gerar_html(all_tks, baixados_hoje=None, urg_tks=None, gerado_em=None):
    today     = _hoje_brt()
    today_str = today.strftime('%d/%m/%Y')
    baixados_hoje = baixados_hoje or []
    urg_tks   = urg_tks or []

    # merge: urg_tks entram no pool geral (sem duplicatas)
    urg_codes_extra = {t['code'] for t in urg_tks}
    all_tks = [t for t in all_tks if t['code'] not in urg_codes_extra] + urg_tks

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
    baixados_by_code = {t['code']: t for t in baixados_hoje}

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

    # urgentes do CSV separado (upload "Urgentes") — mais confiável
    urg_file_codes = {t['code'] for t in urg_tks if t['empresa'] in sul_emp}
    urg_file_pdv   = {c for c in urg_file_codes if 'pdv' in (tk_lkp.get(c,{}).get('produto','') or '').lower()}
    urg_file_erp   = urg_file_codes - urg_file_pdv

    # urgentes dinâmicos: tickets Sul com prioridade=Urgente no CSV principal (fallback)
    csv_urg     = {t['code'] for t in sul if _pnorm(t.get('prioridade','')) == 'urgente'}
    csv_urg_pdv = {c for c in csv_urg if 'pdv' in (tk_lkp.get(c,{}).get('produto','') or '').lower()}
    csv_urg_erp = csv_urg - csv_urg_pdv

    # merge: hardcoded + arquivo urgentes + campo prioridade do CSV
    URG_PDV_EF = URG_PDV | urg_file_pdv | csv_urg_pdv
    URG_ERP_EF = URG_ERP | urg_file_erp | csv_urg_erp
    URG_ALL_EF = URG_PDV_EF | URG_ERP_EF | URG_DEV

    # Regra: atrib define a seção — time ganha sobre lista de urgente
    # 1) Sustentação (atrib) → sempre Sustentação
    # 2) Engenharia Software (atrib) → sempre Eng Software
    # 3) PDV Urgente — exclui Sust e Eng
    # 4) ERP Urgente — exclui PDV, Sust e Eng
    # 5) Comercial   — não urgentes
    # 6) Pendentes   — todo o resto

    # Times dedicados — NUNCA vão para PDV/ERP Urgente, independente de urgência
    SUST_ATRIB = {'Sustentação Desenv.','Sust. Desenv.'}
    DESENV_PDV_ATRIB = {'Desenv. PDV','Sust. Desenv. PDV'}
    HOMOLOG_ATRIB    = {'Homologação','Homologacao'}
    sust_tks      = sorted([t for t in sul if t['atrib'] in SUST_ATRIB], key=lambda x:-x['dias'])
    eng_tks       = sorted([t for t in sul if t['atrib']=='Engenharia Software'], key=lambda x:-x['dias'])
    com_tks       = sorted([t for t in sul if t['atrib']=='Comercial'], key=lambda x:-x['dias'])
    desenv_pdv_tks= sorted([t for t in sul if t['atrib'] in DESENV_PDV_ATRIB], key=lambda x:-x['dias'])
    homolog_tks   = sorted([t for t in sul if t['atrib'] in HOMOLOG_ATRIB], key=lambda x:-x['dias'])

    team_codes = ({t['code'] for t in sust_tks} | {t['code'] for t in eng_tks}
                | {t['code'] for t in com_tks}  | {t['code'] for t in desenv_pdv_tks}
                | {t['code'] for t in homolog_tks})

    # PDV/ERP Urgente — apenas tickets sem time dedicado
    pdv_tks   = sorted([t for t in sul if t['code'] in URG_PDV_EF and t['code'] not in team_codes], key=lambda x:-x['dias'])
    pdv_codes = {t['code'] for t in pdv_tks}

    erp_tks   = sorted([t for t in sul if t['code'] in URG_ERP_EF and t['code'] not in team_codes and t['code'] not in pdv_codes], key=lambda x:-x['dias'])
    erp_codes = {t['code'] for t in erp_tks}

    n_urg_critico = len(pdv_tks) + len(erp_tks)

    _shown_codes = pdv_codes | erp_codes | team_codes
    pendente_tks = sorted([t for t in sul if t['code'] not in _shown_codes], key=lambda x:-x['dias'])

    n_urg=len(pdv_tks)+len(erp_tks)+len(sust_tks)+len(eng_tks)+len(com_tks)+len(desenv_pdv_tks)+len(homolog_tks)+len(pendente_tks)
    n_bklog=len(BACKLOG)

    pct_nov=int(n_nov/tot*100) if tot else 0
    pct_and=int(n_and/tot*100) if tot else 0
    pct_ag =int(tot_ag/tot*100) if tot else 0
    pct_inc=int(tot_inc/tot*100) if tot else 0
    pct_req=int(n_req/tot*100) if tot else 0
    pct_duv=int(n_duv/tot*100) if tot else 0

    # ── WhatsApp text ─────────────────────────────────────────────────────────
    def _wpp_linha(t):
        smov = f' ↩{t["dias_sem_mov"]}d' if t.get('dias_sem_mov', 0) >= 2 else ''
        sla  = ' ⏰SLA' if t.get('sla_venceu') else ''
        assunto = t['assunto'][:55] + ('…' if len(t['assunto']) > 55 else '')
        return f'  #{t["code"]} {t["empresa"]} — {assunto} — {t["dias"]}d{smov}{sla}'
    def _wpp_sec(emoji, nome, tks):
        if not tks: return ''
        return f'\n{emoji} *{nome} ({len(tks)})*\n' + '\n'.join(_wpp_linha(t) for t in tks) + '\n'
    hora_brt = datetime.now(timezone(timedelta(hours=-3))).strftime('%H:%M')
    wpp = f'📊 *Logus Sul BI — {today_str}*\n'
    wpp += f'_{hora_brt} · {tot} chamados · {tot_inc} incidentes · {tot_ag} aguardando · {n_cli} clientes_\n'
    wpp += _wpp_sec('🟢', 'PDV — Urgente',        pdv_tks)
    wpp += _wpp_sec('🔴', 'Corporativo — Urgente', erp_tks)
    wpp += _wpp_sec('🛠️', 'Sustentação',           sust_tks)
    wpp += _wpp_sec('⚙️', 'Engenharia Software',   eng_tks)
    wpp += _wpp_sec('🤝', 'Comercial',             com_tks)
    wpp += _wpp_sec('🖥️', 'Desenv. PDV',           desenv_pdv_tks)
    wpp += _wpp_sec('🧪', 'Homologação',           homolog_tks)
    if pendente_tks:
        wpp += f'\n📋 *Pendentes ({len(pendente_tks)})*\n'
        wpp += '\n'.join(_wpp_linha(t) for t in pendente_tks[:20])
        if len(pendente_tks) > 20:
            wpp += f'\n  ... e mais {len(pendente_tks)-20} tickets'
        wpp += '\n'
    if n_resol:
        wpp += f'\n✅ *Resolvidos hoje: {n_resol}*\n'
    wpp_json = json.dumps(wpp)

    # ── mobile HTML vars ──────────────────────────────────────────────────────
    idx=0
    cli_secs=''
    for emp in sorted(clientes, key=lambda e:(-sum(1 for t in by_cli[e] if t['tipo']=='Incidente'),-len(by_cli[e]))):
        cli_secs+=_csec(emp,by_cli[emp],idx); idx+=1

    resp_secs='<div style="color:#ea580c;font-size:11px;font-weight:700;letter-spacing:1px;padding:8px 4px 6px">🌿 EQUIPE SUL</div>'
    for r in resp_sul:   resp_secs+=_rsec(r,by_resp[r],idx,'#ea580c'); idx+=1
    resp_secs+='<div style="color:#7c3aed;font-size:11px;font-weight:700;letter-spacing:1px;padding:14px 4px 6px">🏢 EQUIPE LOGUS</div>'
    for r in resp_logus: resp_secs+=_rsec(r,by_resp[r],idx,'#7c3aed'); idx+=1

    urg_html=(
        _ugrp('🟢 PDV — Urgente',        '#16a34a','#dcfce7',pdv_tks, uid='ug0')+
        _ugrp('🔴 Corporativo — Urgente', '#dc2626','#fee2e2',erp_tks, uid='ug1')+
        _ugrp('🛠️ Sustentação',           '#7c3aed','#ede9fe',sust_tks,     uid='ug2')+
        _ugrp('⚙️ Engenharia Software',   '#2563eb','#dbeafe',eng_tks,     uid='ug5')+
        _ugrp('🤝 Comercial',             '#d97706','#fef3c7',com_tks,     uid='ug3')+
        _ugrp('🖥️ Desenv. PDV',           '#9333ea','#f3e8ff',desenv_pdv_tks,uid='ug6')+
        _ugrp('🧪 Homologação',           '#0891b2','#cffafe',homolog_tks, uid='ug7')+
        _ugrp_por_cli('📋 Pendentes de Atendimento','#475569','#f8fafc',pendente_tks,uid='ug4')
    )

    cust_html=''
    for st in ['Urgente','Em Homologação','Em Roadmap','Pendente','Homologado']:
        grp=[b for b in BACKLOG if b['status']==st]
        if not grp: continue
        cor={'Urgente':'#b91c1c','Em Homologação':'#c2410c','Em Roadmap':'#1d4ed8','Homologado':'#15803d'}.get(st,'#475569')
        cust_html+=(f'<div style="color:{cor};font-size:11px;font-weight:700;letter-spacing:1px;padding:10px 4px 6px">{st.upper()} — {len(grp)}</div>'
                    +''.join(_ccard(b) for b in grp))

    hoje_cards=''.join(_tk(t) for t in sorted([t for t in sul if t['data']==today_str],key=lambda x:x['empresa']))

    # hoje sempre aparece primeiro no seletor, mesmo sem dados
    datas_show = [today_str] + [d for d in datas_res if d != today_str]

    # seletor de datas para baixados
    date_opts=''
    for dt in datas_show:
        safe=dt.replace('/','_')
        cnt=len(by_res.get(dt,[]))
        lbl=f'{dt} — {cnt} resolvidos  ✅ HOJE' if dt==today_str else f'{dt} — {cnt} resolvidos'
        sel='selected' if dt==today_str else ''
        date_opts+=f'<option value="{safe}" {sel}>{lbl}</option>'

    vazio='<div style="color:#94a3b8;text-align:center;padding:24px;font-size:13px">Nenhum chamado resolvido neste dia.</div>'

    # seções mobile (cards) por data
    mob_bx_chips=''; mob_bx_content=''
    for dt in datas_show:
        safe=dt.replace('/','_')
        tks=sorted(by_res.get(dt,[]),key=lambda x:x.get('empresa',''))
        is_today=dt==today_str
        cnt=len(tks)
        lbl=f'HOJE · {cnt}' if is_today else f'{dt[:5]} · {cnt}'
        bg='#dcfce7' if is_today else '#f1f5f9'
        bdr='#16a34a' if is_today else '#16a34a44'
        cards=''.join(_tk(t) for t in tks) if tks else vazio
        mob_bx_chips+=(f'<button onclick="selDate(\'mbxs\',\'{safe}\')" id="mbxs_btn_{safe}" data-grp="mbxs" data-cor="#16a34a" data-bg="#dcfce7"'
                       f' style="background:{bg};color:#16a34a;border:1px solid {bdr};border-radius:20px;padding:7px 14px;font-size:12px;font-weight:700;white-space:nowrap;cursor:pointer;flex-shrink:0">'
                       f'{lbl}</button>')
        mob_bx_content+=f'<div id="mbxs_c_{safe}" style="display:{"block" if is_today else "none"}">{cards}</div>'
    mob_bx=(f'<div style="overflow-x:auto;display:flex;gap:6px;padding:4px 0 10px;scrollbar-width:none;-webkit-overflow-scrolling:touch">{mob_bx_chips}</div>'
            +mob_bx_content)

    # seções desktop (tabelas) por data
    dt_bx=''
    for dt in datas_show:
        safe=dt.replace('/','_')
        tks=sorted(by_res.get(dt,[]),key=lambda x:x.get('empresa',''))
        show='block' if dt==today_str else 'none'
        rows=''.join(_d_row(t, show_cli=True) for t in tks) if tks else f'<tr><td colspan="8">{vazio}</td></tr>'
        dt_bx+=(f'<div id="dbx-{safe}" class="bx-s" style="display:{show}">'
                f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">'
                f'{_d_tbl_hdr(show_cli=True)}<tbody>{rows}</tbody></table></div></div>')

    # agrupa abertos por data de abertura — apenas últimos 14 dias
    by_data = defaultdict(list)
    for t in sul:
        if t['data'] and t['dias'] <= 14:
            by_data[t['data']].append(t)
    datas_ent = sorted(by_data.keys(), reverse=True)
    datas_ent_show = [today_str] + [d for d in datas_ent if d != today_str]

    ent_opts=''
    for dt in datas_ent_show:
        safe=dt.replace('/','_')
        cnt=len(by_data.get(dt,[]))
        lbl=f'{dt} — {cnt} tickets  📅 HOJE' if dt==today_str else f'{dt} — {cnt} tickets'
        sel='selected' if dt==today_str else ''
        ent_opts+=f'<option value="{safe}" {sel}>{lbl}</option>'

    vazio_ent='<div style="color:#94a3b8;text-align:center;padding:24px;font-size:13px">Nenhum chamado aberto neste dia.</div>'

    mob_ent_chips=''; mob_ent_content=''
    for dt in datas_ent_show:
        safe=dt.replace('/','_')
        tks=sorted(by_data.get(dt,[]),key=lambda x:x.get('empresa',''))
        is_today=dt==today_str
        cnt=len(tks)
        lbl=f'HOJE · {cnt}' if is_today else f'{dt[:5]} · {cnt}'
        bg='#dcfce7' if is_today else '#f1f5f9'
        bdr='#16a34a' if is_today else '#16a34a44'
        cards=''.join(_tk(t) for t in tks) if tks else vazio_ent
        mob_ent_chips+=(f'<button onclick="selDate(\'mbeds\',\'{safe}\')" id="mbeds_btn_{safe}" data-grp="mbeds" data-cor="#16a34a" data-bg="#dcfce7"'
                        f' style="background:{bg};color:#16a34a;border:1px solid {bdr};border-radius:20px;padding:7px 14px;font-size:12px;font-weight:700;white-space:nowrap;cursor:pointer;flex-shrink:0">'
                        f'{lbl}</button>')
        mob_ent_content+=f'<div id="mbeds_c_{safe}" style="display:{"block" if is_today else "none"}">{cards}</div>'
    mob_ent=(f'<div style="overflow-x:auto;display:flex;gap:6px;padding:4px 0 10px;scrollbar-width:none;-webkit-overflow-scrolling:touch">{mob_ent_chips}</div>'
             +mob_ent_content)

    dt_ent=''
    for dt in datas_ent_show:
        safe=dt.replace('/','_')
        tks=sorted(by_data.get(dt,[]),key=lambda x:x.get('empresa',''))
        show='block' if dt==today_str else 'none'
        rows=''.join(_d_row(t,show_cli=True) for t in tks) if tks else f'<tr><td colspan="8">{vazio_ent}</td></tr>'
        dt_ent+=(f'<div id="dbe-{safe}" class="bx-s" style="display:{show}">'
                 f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">'
                 f'{_d_tbl_hdr(show_cli=True)}<tbody>{rows}</tbody></table></div></div>')

    def _mob_kpi(label, val, cor, sub=''):
        sub_html = f'<div style="color:#94a3b8;font-size:9px;margin-top:2px">{sub}</div>' if sub else ''
        return (f'<div style="background:#ffffff;border:1px solid {cor}22;border-top:3px solid {cor};border-radius:10px;padding:12px 10px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
                f'<div style="color:{cor};font-size:28px;font-weight:900;line-height:1">{val}</div>'
                f'<div style="color:#374151;font-size:9px;font-weight:700;letter-spacing:.5px;margin-top:7px">{label}</div>'
                f'{sub_html}</div>')

    mob_res=(
        # KPIs
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">'
        +_mob_kpi('TOTAL ABERTOS',  tot,           '#3b82f6', f'{n_cli} clientes')
        +_mob_kpi('INCIDENTES',     tot_inc,       '#ef4444', f'{pct_inc}%')
        +_mob_kpi('URGENTES',       n_urg_critico, '#f97316', 'PDV+Corp')
        +_mob_kpi('AGUARDANDO',     tot_ag,        '#d97706', f'{pct_ag}%')
        +_mob_kpi('ENTRARAM HOJE',  n_hoje,        '#22c55e')
        +(_mob_kpi('RESOLVIDOS HOJE', n_resol,     '#4ade80') if n_resol else _mob_kpi('RESOLVIDOS HOJE','—','#374151'))
        +f'</div>'
        # STATUS + TIPO em grid compacto
        +f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px">'
        +f'<div style="background:#ffffff;border-radius:10px;padding:12px 14px;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
        +f'<div style="color:#374151;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:10px">STATUS</div>'
        +_bar('Novo',n_nov,tot,'#16a34a')+_bar('Em And.',n_and,tot,'#2563eb')+_bar('Aguard.',tot_ag,tot,'#d97706')
        +f'</div>'
        +f'<div style="background:#ffffff;border-radius:10px;padding:12px 14px;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
        +f'<div style="color:#374151;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:10px">TIPO</div>'
        +_bar('Incidente',tot_inc,tot,'#dc2626')+_bar('Requisição',n_req,tot,'#2563eb')+_bar('Dúvida',n_duv,tot,'#7c3aed')
        +f'</div></div>'
        # ENTRARAM
        +(f'<div style="color:#22c55e;font-size:12px;font-weight:700;letter-spacing:1px;padding:12px 0 6px">📥 ENTRARAM</div>'
          +mob_ent if datas_ent else '')
        # RESOLVIDOS
        +(f'<div style="color:#4ade80;font-size:12px;font-weight:700;letter-spacing:1px;padding:12px 0 6px">📤 RESOLVIDOS</div>'
          +mob_bx if datas_res else '')
    )

    # ── desktop HTML vars ─────────────────────────────────────────────────────
    dt_donut = _d_donut_chart(by_cli, clientes)
    cli_ord = sorted(clientes, key=lambda e:(-sum(1 for t in by_cli[e] if t['tipo']=='Incidente'),-len(by_cli[e])))
    dt_cli_grid    = ''.join(_d_clibox(e,by_cli[e]) for e in cli_ord)
    dt_cli_details = ''.join(_d_detail(e,by_cli[e],f'dtd-{_d_safe(e)}','dCli(null)') for e in clientes)

    dt_rsul_grid    = ''.join(_d_respbox(r,by_resp[r],'#ea580c') for r in resp_sul)
    dt_rlogus_grid  = ''.join(_d_respbox(r,by_resp[r],'#7c3aed') for r in resp_logus)
    dt_rsul_det     = ''.join(_d_detail(r,by_resp[r],f'dtr-{_d_safe(r)}','dResp(null)') for r in resp_sul)
    dt_rlogus_det   = ''.join(_d_detail(r,by_resp[r],f'dtr-{_d_safe(r)}','dResp(null)') for r in resp_logus)

    dt_urg_html=(
        _d_urg_sec('🟢 PDV — Urgente',        '#16a34a','#dcfce7',pdv_tks)+
        _d_urg_sec('🔴 Corporativo — Urgente', '#dc2626','#fee2e2',erp_tks)+
        _d_urg_sec('🛠️ Sustentação',           '#7c3aed','#ede9fe',sust_tks)+
        _d_urg_sec('⚙️ Engenharia Software',   '#2563eb','#dbeafe',eng_tks)+
        _d_urg_sec('🤝 Comercial',             '#d97706','#fef3c7',com_tks)+
        _d_urg_sec('🖥️ Desenv. PDV',           '#9333ea','#f3e8ff',desenv_pdv_tks)+
        _d_urg_sec('🧪 Homologação',           '#0891b2','#cffafe',homolog_tks)+
        _d_urg_por_cli('📋 Pendentes de Atendimento','#475569','#f8fafc',pendente_tks)
    )

    dt_cust_rows=''
    for st in ['Urgente','Em Homologação','Em Roadmap','Pendente','Homologado']:
        for b in [x for x in BACKLOG if x['status']==st]:
            s=b['status']
            cor={'Urgente':'#ef4444','Homologado':'#22c55e','Em Homologação':'#fb923c','Em Roadmap':'#60a5fa'}.get(s,'#6b7280')
            est=b['est'] if b['est'] else '—'
            dt_cust_rows+=(f'<tr style="border-bottom:1px solid #f1f5f9">'
                           f'<td style="color:#ea580c;font-weight:900;padding:9px 12px;white-space:nowrap">#{b["ticket"]}</td>'
                           f'<td style="color:#92400e;padding:9px 12px;font-size:12px;font-weight:700">{b["cliente"]}</td>'
                           f'<td style="color:#1e293b;padding:9px 12px;font-size:13px">{b["desc"]}</td>'
                           f'<td style="color:{cor};padding:9px 12px;font-size:11px;white-space:nowrap">{est}</td>'
                           f'<td style="padding:9px 12px"><span style="background:{cor}22;color:{cor};border-radius:4px;padding:3px 8px;font-size:10px;font-weight:900">{s.upper()}</span></td>'
                           f'</tr>')

    dt_bar_chart = _d_exec_bar_chart(by_cli, clientes)

    dt_res_html=(
        # ── KPI cards ──────────────────────────────────────────────────────────
        f'<div style="display:flex;gap:12px;margin-bottom:22px;flex-wrap:wrap">'
        +_d_kpi_big('Total Abertos',  tot,           '#3b82f6', f'{n_cli} clientes')
        +_d_kpi_big('Incidentes',     tot_inc,       '#ef4444', f'{pct_inc}% do total')
        +_d_kpi_big('Urgentes',       n_urg_critico, '#f97316', 'PDV + Corporativo')
        +_d_kpi_big('Aguardando',     tot_ag,        '#d97706', f'{pct_ag}% do total')
        +_d_kpi_big('Entraram Hoje',  n_hoje,        '#22c55e')
        +(_d_kpi_big('Resolvidos Hoje', n_resol,     '#4ade80') if n_resol else '')
        +f'</div>'
        # ── gráfico de barras + STATUS/TIPO ────────────────────────────────────
        +f'<div style="display:grid;grid-template-columns:3fr 2fr;gap:16px;margin-bottom:20px">'
        +f'<div style="background:#ffffff;border-radius:10px;padding:20px 18px;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
        +f'<div style="color:#374151;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:16px">CHAMADOS POR CLIENTE</div>'
        +dt_bar_chart
        +f'</div>'
        +f'<div style="display:flex;flex-direction:column;gap:12px">'
        +f'<div style="background:#ffffff;border-radius:10px;padding:16px 18px;flex:1;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
        +f'<div style="color:#374151;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:12px">STATUS</div>'
        +_bar('Novo',n_nov,tot,'#16a34a')+_bar('Em Andamento',n_and,tot,'#2563eb')+_bar('Aguardando',tot_ag,tot,'#d97706')
        +f'</div>'
        +f'<div style="background:#ffffff;border-radius:10px;padding:16px 18px;flex:1;box-shadow:0 1px 4px rgba(0,0,0,0.06)">'
        +f'<div style="color:#374151;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:12px">TIPO</div>'
        +_bar('Incidente',tot_inc,tot,'#dc2626')+_bar('Requisição',n_req,tot,'#2563eb')+_bar('Dúvida/Outros',n_duv,tot,'#7c3aed')
        +f'</div></div>'
        +f'</div>'
        # ── ENTRARAM / RESOLVIDOS ───────────────────────────────────────────────
        +(f'<div style="display:flex;align-items:center;gap:14px;margin:20px 0 12px">'
          f'<span style="color:#16a34a;font-size:12px;font-weight:700;letter-spacing:1px">📥 ENTRARAM</span>'
          f'<select onchange="filtrarRes(\'dbe\',this.value)" style="background:#ffffff;color:#1e293b;border:1px solid #e2e8f0;border-radius:6px;padding:6px 12px;font-size:13px">{ent_opts}</select>'
          f'</div>{dt_ent}' if datas_ent else '')
        +(f'<div style="display:flex;align-items:center;gap:14px;margin:20px 0 12px">'
          f'<span style="color:#16a34a;font-size:12px;font-weight:700;letter-spacing:1px">📤 RESOLVIDOS</span>'
          f'<select onchange="filtrarRes(\'dbx\',this.value)" style="background:#ffffff;color:#1e293b;border:1px solid #e2e8f0;border-radius:6px;padding:6px 12px;font-size:13px">{date_opts}</select>'
          f'</div>{dt_bx}' if datas_res else '')
    )

    def _d_stat_sm(label, val, cor, tab=''):
        if not val: return ''
        click = f' onclick="dTab(\'{tab}\')" title="Ir para {label}"' if tab else ''
        return (f'<div class="dstat"{click} style="background:{cor}0d;border:2px solid {cor}44;border-top:3px solid {cor};border-radius:10px;padding:8px 16px;text-align:center;cursor:pointer;box-shadow:0 2px 8px {cor}22">'
                f'<div style="color:{cor};font-size:34px;font-weight:900;line-height:1">{val}</div>'
                f'<div style="color:#374151;font-size:11px;font-weight:800;letter-spacing:.5px;margin-top:5px">{label}</div>'
                f'</div>')

    dt_hdr_stats=(
        _d_stat('CLIENTES',  n_cli,    '#ea580c','cli')
       +_d_stat('CHAMADOS',  tot,      '#ea580c','cli')
       +_d_stat('INCIDENTES',tot_inc,  '#dc2626','urg')
       +_d_stat('AGUARDANDO',tot_ag,   '#d97706','resp')
       +_d_stat('NOVOS',     n_nov,    '#16a34a','res')
       +f'<div style="width:1px;background:#e2e8f0;margin:0 4px"></div>'
       +_d_stat_sm('SUST.',      len(sust_tks),       '#6d28d9','urg')
       +_d_stat_sm('ENG.SW',     len(eng_tks),        '#1d4ed8','urg')
       +_d_stat_sm('COMERCIAL',  len(com_tks),        '#b45309','urg')
       +_d_stat_sm('DESENV.PDV', len(desenv_pdv_tks), '#7e22ce','urg')
       +_d_stat_sm('HOMOLOG.',   len(homolog_tks),    '#0e7490','urg')
    )

    # ── Resumo visual (modal tabela larga) ────────────────────────────────────
    def _rsm_tbl(emoji, cor, bg, nome, tks):
        if not tks: return ''
        rows = ''
        for t in tks:
            fc,_ = _dc(t['dias'])
            sla  = '<span style="background:#fee2e2;color:#b91c1c;font-size:9px;font-weight:900;border-radius:3px;padding:1px 4px;margin-left:3px">SLA</span>' if t.get('sla_venceu') else ''
            dias_mov = t.get('dias_sem_mov',0)
            if dias_mov >= 2:
                mc = '#dc2626' if dias_mov>14 else '#d97706' if dias_mov>7 else '#64748b'
                smov_td = f'<td style="color:{mc};font-weight:800;padding:7px 8px;font-size:12px;text-align:right;white-space:nowrap">{dias_mov}d</td>'
            elif dias_mov == 1:
                smov_td = '<td style="color:#16a34a;font-size:11px;padding:7px 8px;text-align:right">✓ 1d</td>'
            else:
                smov_td = '<td style="color:#16a34a;font-size:11px;padding:7px 8px;text-align:right">✓ hoje</td>'
            tc = '#ef4444' if t['tipo']=='Incidente' else '#3b82f6' if t['tipo']=='Requisição' else '#6b7280'
            ec = {'Novo':'#22c55e','Em andamento':'#3b82f6','Aguardando':'#d97706'}.get(t['status'],'#6b7280')
            rows += (f'<tr style="border-bottom:1px solid #f1f5f9">'
                     f'<td style="color:#ea580c;font-weight:900;padding:7px 10px;white-space:nowrap;font-size:12px">#{t["code"]}{sla}</td>'
                     f'<td style="color:#ea580c;font-weight:700;padding:7px 10px;font-size:12px;white-space:nowrap">{t["empresa"]}</td>'
                     f'<td style="padding:7px 8px"><span style="background:{tc}22;color:{tc};border-radius:3px;padding:2px 6px;font-size:9px;font-weight:900">{t["tipo"].upper()[:3]}</span></td>'
                     f'<td style="color:#111827;padding:7px 10px;font-size:12px">{t["assunto"][:60]}{"…" if len(t["assunto"])>60 else ""}</td>'
                     f'<td style="padding:7px 8px"><span style="background:{ec}22;color:{ec};border-radius:3px;padding:2px 6px;font-size:9px;font-weight:900">{t["status"].upper()[:3]}</span></td>'
                     f'<td style="color:#374151;padding:7px 10px;font-size:12px;white-space:nowrap">{t["atrib"]}</td>'
                     f'<td style="color:{fc};font-weight:900;padding:7px 10px;font-size:13px;text-align:right;white-space:nowrap">{t["dias"]}d</td>'
                     f'{smov_td}</tr>')
        hdr = (f'<thead><tr style="background:{bg}">'
               f'<th style="color:{cor};padding:6px 10px;font-size:10px;text-align:left;white-space:nowrap">{emoji} {nome} ({len(tks)})</th>'
               f'<th style="color:#475569;padding:6px 10px;font-size:10px;text-align:left">CLIENTE</th>'
               f'<th style="color:#475569;padding:6px 8px;font-size:10px">TIPO</th>'
               f'<th style="color:#475569;padding:6px 10px;font-size:10px;text-align:left">ASSUNTO</th>'
               f'<th style="color:#475569;padding:6px 8px;font-size:10px">ESTADO</th>'
               f'<th style="color:#475569;padding:6px 10px;font-size:10px;text-align:left">COM QUEM</th>'
               f'<th style="color:#475569;padding:6px 10px;font-size:10px;text-align:right">DIAS</th>'
               f'<th style="color:#475569;padding:6px 8px;font-size:10px;text-align:right">S/MOV</th>'
               f'</tr></thead>')
        return (f'<table style="width:100%;border-collapse:collapse;margin-bottom:12px;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.08)">'
                f'{hdr}<tbody>{rows}</tbody></table>')

    resumo_secs = (
        _rsm_tbl('🟢','#16a34a','#dcfce7','PDV — Urgente',        pdv_tks)
       +_rsm_tbl('🔴','#dc2626','#fee2e2','Corporativo — Urgente', erp_tks)
       +_rsm_tbl('🛠️','#7c3aed','#ede9fe','Sustentação',           sust_tks)
       +_rsm_tbl('⚙️','#2563eb','#dbeafe','Engenharia Software',   eng_tks)
       +_rsm_tbl('🤝','#d97706','#fef3c7','Comercial',             com_tks)
       +_rsm_tbl('🖥️','#9333ea','#f3e8ff','Desenv. PDV',           desenv_pdv_tks)
       +_rsm_tbl('🧪','#0891b2','#cffafe','Homologação',           homolog_tks)
       +_rsm_tbl('📋','#475569','#f8fafc','Pendentes',             pendente_tks)
    )
    resumo_html = (
        f'<div style="background:#fff7ed;border-bottom:3px solid #ea580c;padding:10px 16px;display:flex;justify-content:space-between;align-items:center;flex-shrink:0">'
        f'<div><div style="color:#ea580c;font-size:15px;font-weight:900">Logus Sul BI</div>'
        f'<div style="color:#64748b;font-size:11px">{today_str} · {hora_brt}</div></div>'
        f'<div style="display:flex;gap:16px">'
        f'<div style="text-align:center"><div style="color:#ea580c;font-size:20px;font-weight:900">{tot}</div><div style="color:#64748b;font-size:9px">CHAMADOS</div></div>'
        f'<div style="text-align:center"><div style="color:#dc2626;font-size:20px;font-weight:900">{tot_inc}</div><div style="color:#64748b;font-size:9px">INCIDENTES</div></div>'
        f'<div style="text-align:center"><div style="color:#f97316;font-size:20px;font-weight:900">{n_urg_critico}</div><div style="color:#64748b;font-size:9px">URGENTES</div></div>'
        f'<div style="text-align:center"><div style="color:#d97706;font-size:20px;font-weight:900">{tot_ag}</div><div style="color:#64748b;font-size:9px">AGUARDANDO</div></div>'
        f'</div></div>'
        f'<div style="padding:12px 16px;overflow-y:auto;flex:1">{resumo_secs}</div>'
    )
    return f"""<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>Logus Sul BI · {today_str}</title>
<link rel="icon" href="/static/favicon.ico">
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#ea580c">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Sul BI">
<link rel="apple-touch-icon" href="/static/icon-192.png">
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
html,body{{background:#f1f5f9;color:#1e293b;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
@keyframes pulse{{0%,100%{{opacity:.6}}50%{{opacity:1}}}}
/* mobile */
#dt{{display:none}}
#mob{{display:block}}
body{{padding-bottom:70px}}
#hdr{{position:sticky;top:0;z-index:100;background:#ffffff;border-bottom:1px solid #e2e8f0;padding:10px 14px;box-shadow:0 1px 4px rgba(0,0,0,0.06)}}
.hdr-top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}}
.hdr-logo{{height:36px;background:#fff;border-radius:7px;padding:3px 8px}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}}
.stat{{background:#ffffff;border-radius:10px;padding:8px 4px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.1)}}
.stat-n{{font-size:26px;font-weight:900}}
.stat-l{{font-size:10px;font-weight:800;letter-spacing:.3px;margin-top:3px;color:#374151}}
#content{{padding:12px 14px}}
.view{{display:none}}.view.on{{display:block}}
#nav{{position:fixed;bottom:0;left:0;right:0;background:#ffffff;border-top:1px solid #e2e8f0;display:flex;z-index:100;padding-bottom:env(safe-area-inset-bottom);box-shadow:0 -1px 8px rgba(0,0,0,0.06)}}
.nb{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:8px 4px 10px;cursor:pointer;border:none;background:none;color:#374151;font-size:9px;font-weight:700;gap:3px;transition:color .15s}}
.nb .ni{{font-size:22px;line-height:1}}
.nb.on{{color:#ea580c}}.nb.on-urg{{color:#dc2626}}.nb.on-res{{color:#16a34a}}.nb.on-cust{{color:#7c3aed}}
.sec-hdr{{color:#374151;font-size:11px;font-weight:700;letter-spacing:1px;padding:6px 0 10px}}
/* desktop */
@media(min-width:768px){{
  body{{padding:0}}
  #dt{{display:block}}
  #mob{{display:none}}
  .dtab{{background:none;border:none;color:#374151;font-size:13px;font-weight:700;padding:11px 22px;cursor:pointer;border-bottom:3px solid transparent;transition:color .15s}}
  .dtab:hover{{color:#1e293b}}
  .dtab.on{{color:#ea580c;border-bottom-color:#ea580c}}
  .dview{{display:none}}.dview.on{{display:block}}
  .dcbox:hover,.drbox:hover{{background:#fff7ed!important;border-color:#ea580c!important}}
  .dcbox.sel{{background:#fff7ed!important;border-color:#ea580c!important}}
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
function abrirTk(code,btn){{
  window.open('https://logusretail.tolvdesk.com/webapp/#/tickets/todos?busca='+code,'tolvdesk');
  navigator.clipboard.writeText(code).catch(function(){{}});
  var orig=btn.innerHTML;
  btn.innerHTML='🔍 Buscando...';
  btn.style.background='#2563eb';
  setTimeout(function(){{btn.innerHTML=orig;btn.style.background='#ea580c';}},2000);
}}
var _wppTxt={wpp_json};
function copiarWpp(btn){{
  navigator.clipboard.writeText(_wppTxt).then(function(){{
    var orig=btn.innerHTML;
    btn.innerHTML='✅ Copiado!';
    btn.style.background='#16a34a';
    setTimeout(function(){{btn.innerHTML=orig;btn.style.background='#25D366';}},2000);
  }});
}}
function _capturarResumo(btn){{
  var inner=document.getElementById('resumo-inner');
  if(!inner) return;
  var orig=btn.innerHTML; btn.innerHTML='⏳ Capturando...'; btn.disabled=true;
  var prevOv=inner.style.overflow; var prevH=inner.style.maxHeight;
  inner.style.overflow='visible'; inner.style.maxHeight='none';
  var dpr=window.devicePixelRatio||1;
  html2canvas(inner,{{scale:Math.max(3,dpr*2),useCORS:true,logging:false,width:inner.scrollWidth,height:inner.scrollHeight}}).then(function(canvas){{
    inner.style.overflow=prevOv; inner.style.maxHeight=prevH;
    canvas.toBlob(function(blob){{
      if(navigator.clipboard&&navigator.clipboard.write){{
        navigator.clipboard.write([new ClipboardItem({{'image/png':blob}})]).then(function(){{
          btn.innerHTML='✅ Imagem copiada! Cole no WhatsApp';
          btn.style.background='#16a34a';
          setTimeout(function(){{btn.innerHTML=orig;btn.style.background='#25D366';btn.disabled=false;}},3000);
        }}).catch(function(){{_downloadCanvas(canvas,btn,orig);}});
      }} else {{ _downloadCanvas(canvas,btn,orig); }}
    }});
  }}).catch(function(){{inner.style.overflow=prevOv;inner.style.maxHeight=prevH;btn.innerHTML=orig;btn.disabled=false;}});
}}
function _downloadCanvas(canvas,btn,orig){{
  var a=document.createElement('a'); a.href=canvas.toDataURL('image/png');
  a.download='logus-sul-bi.png'; a.click();
  btn.innerHTML='✅ Baixado! Envie no WhatsApp'; btn.style.background='#16a34a';
  setTimeout(function(){{btn.innerHTML=orig;btn.style.background='#25D366';btn.disabled=false;}},3000);
}}
function abrirResumo(){{
  var ov=document.getElementById('resumo-ov');
  if(!ov){{
    ov=document.createElement('div');
    ov.id='resumo-ov';
    ov.style.cssText='position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:9999;display:flex;align-items:center;justify-content:center;padding:12px';
    ov.onclick=function(e){{if(e.target===ov)ov.style.display='none';}};
    var box=document.createElement('div');
    box.style.cssText='background:#f1f5f9;border-radius:12px;overflow:hidden;width:95vw;max-width:1100px;height:90vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,0.3)';
    var top=document.createElement('div');
    top.style.cssText='background:#ea580c;padding:8px 12px;display:flex;justify-content:space-between;align-items:center;flex-shrink:0;gap:8px';
    var lbl=document.createElement('span');
    lbl.style.cssText='color:#fff;font-size:12px;font-weight:700;flex:1';
    lbl.textContent='📷 Resumo Visual — Logus Sul BI';
    var copyBtn=document.createElement('button');
    copyBtn.style.cssText='background:#25D366;border:none;color:#fff;font-size:12px;font-weight:700;cursor:pointer;border-radius:6px;padding:6px 12px;white-space:nowrap';
    copyBtn.innerHTML='📋 Copiar Imagem → WhatsApp';
    copyBtn.onclick=function(){{_capturarResumo(copyBtn);}};
    var closeBtn=document.createElement('button');
    closeBtn.style.cssText='background:transparent;border:none;color:#fff;font-size:20px;cursor:pointer;line-height:1;padding:0 4px';
    closeBtn.textContent='✕';
    closeBtn.onclick=function(){{ov.style.display='none';}};
    top.appendChild(lbl); top.appendChild(copyBtn); top.appendChild(closeBtn);
    var content=document.getElementById('resumo-data');
    if(!content){{box.innerHTML='<p style="padding:20px">Sem dados</p>';}}
    else{{
      var inner=document.createElement('div');
      inner.id='resumo-inner';
      inner.style.cssText='overflow-y:auto;flex:1;background:#f1f5f9;padding:12px';
      inner.innerHTML=content.innerHTML;
      box.appendChild(top); box.appendChild(inner);
    }}
    ov.appendChild(box);
    document.body.appendChild(ov);
  }} else {{
    ov.style.display='flex';
  }}
}}
function iniciarRecorte(){{
  var ov=document.createElement('div');
  ov.style.cssText='position:fixed;inset:0;z-index:99999;cursor:crosshair;user-select:none';
  var mask=document.createElement('div');
  mask.style.cssText='position:absolute;inset:0;background:rgba(0,0,0,0.35)';
  ov.appendChild(mask);
  var sel=document.createElement('div');
  sel.style.cssText='position:absolute;border:2px solid #25D366;background:rgba(37,211,102,0.12);display:none;pointer-events:none';
  ov.appendChild(sel);
  var tip=document.createElement('div');
  tip.style.cssText='position:fixed;top:14px;left:50%;transform:translateX(-50%);background:#1e293b;color:#fff;padding:9px 20px;border-radius:8px;font-size:13px;font-weight:700;pointer-events:none;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.4)';
  tip.textContent='✂️ Arraste para selecionar a área — ESC cancela';
  ov.appendChild(tip);
  var sx=0,sy=0,drawing=false;
  function getR(e){{var x=Math.min(e.clientX,sx),y=Math.min(e.clientY,sy);return{{x:x,y:y,w:Math.abs(e.clientX-sx),h:Math.abs(e.clientY-sy)}};}}
  ov.addEventListener('mousedown',function(e){{
    e.preventDefault(); drawing=true; sx=e.clientX; sy=e.clientY;
    sel.style.display='block'; sel.style.left=sx+'px'; sel.style.top=sy+'px'; sel.style.width='0'; sel.style.height='0';
  }});
  ov.addEventListener('mousemove',function(e){{
    if(!drawing) return;
    var r=getR(e); sel.style.left=r.x+'px'; sel.style.top=r.y+'px'; sel.style.width=r.w+'px'; sel.style.height=r.h+'px';
  }});
  ov.addEventListener('mouseup',function(e){{
    if(!drawing) return; drawing=false;
    var r=getR(e); document.body.removeChild(ov); document.removeEventListener('keydown',onEsc);
    if(r.w>10&&r.h>10) _capturarArea(r.x,r.y,r.w,r.h);
  }});
  function onEsc(e){{if(e.key==='Escape'){{document.body.removeChild(ov);document.removeEventListener('keydown',onEsc);}}}}
  document.addEventListener('keydown',onEsc);
  document.body.appendChild(ov);
}}
function _capturarArea(cx,cy,cw,ch){{
  var px=window.scrollX||0, py=window.scrollY||0;
  var dpr=window.devicePixelRatio||1;
  var sc=Math.max(3, dpr*2);
  var load=document.createElement('div');
  load.style.cssText='position:fixed;top:14px;left:50%;transform:translateX(-50%);background:#2563eb;color:#fff;padding:9px 20px;border-radius:8px;font-size:13px;font-weight:700;z-index:99999;white-space:nowrap';
  load.textContent='⏳ Capturando...';
  document.body.appendChild(load);
  html2canvas(document.body,{{scale:sc,useCORS:true,logging:false,x:cx+px,y:cy+py,width:cw,height:ch}}).then(function(fullC){{
    var out=document.createElement('canvas');
    out.width=Math.round(cw*sc); out.height=Math.round(ch*sc);
    out.getContext('2d').drawImage(fullC,0,0);
    document.body.removeChild(load);
    out.toBlob(function(blob){{
      if(navigator.clipboard&&navigator.clipboard.write){{
        navigator.clipboard.write([new ClipboardItem({{'image/png':blob}})]).then(function(){{
          _msgArea('✅ Área copiada! Cole no WhatsApp');
        }}).catch(function(){{_dlArea(out);}});
      }} else {{ _dlArea(out); }}
    }});
  }}).catch(function(){{document.body.removeChild(load);}});
}}
function _msgArea(txt){{
  var m=document.createElement('div');
  m.style.cssText='position:fixed;top:14px;left:50%;transform:translateX(-50%);background:#16a34a;color:#fff;padding:9px 20px;border-radius:8px;font-size:13px;font-weight:700;z-index:99999;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.3)';
  m.textContent=txt; document.body.appendChild(m);
  setTimeout(function(){{document.body.removeChild(m);}},3000);
}}
function _dlArea(canvas){{
  var a=document.createElement('a'); a.href=canvas.toDataURL('image/png');
  a.download='logus-sul-bi-recorte.png'; a.click();
  _msgArea('✅ Salvo! Envie no WhatsApp');
}}
function selDate(grp,safe){{
  document.querySelectorAll('[data-grp="'+grp+'"]').forEach(function(b){{
    b.style.background='#f1f5f9';
    b.style.borderColor=b.getAttribute('data-cor')+'44';
  }});
  var btn=document.getElementById(grp+'_btn_'+safe);
  if(btn){{btn.style.background=btn.getAttribute('data-bg');btn.style.borderColor=btn.getAttribute('data-cor');}}
  document.querySelectorAll('[id^="'+grp+'_c_"]').forEach(function(el){{el.style.display='none'}});
  var el=document.getElementById(grp+'_c_'+safe); if(el)el.style.display='block';
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
  <div style="position:sticky;top:0;z-index:200;background:#ffffff;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
  <div style="background:#ffffff;border-bottom:1px solid #e2e8f0;padding:10px 28px;display:flex;align-items:center;justify-content:space-between">
    <div style="display:flex;align-items:center;gap:14px">
      <img src="/static/logo.png" style="height:42px;background:#fff;border-radius:8px;padding:4px 10px">
      <div>
        <span style="color:#ea580c;font-size:10px;font-weight:900;background:#fff7ed;border:1px solid #ea580c;border-radius:4px;padding:2px 8px;letter-spacing:.5px">SUL</span>
        <div style="margin-top:4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap">
          <span style="color:#374151;font-size:12px;font-weight:900">Painel de Chamados · {today_str}</span>
          <span style="color:#16a34a;font-size:11px;font-weight:800;background:#dcfce7;border:1px solid #86efac;border-radius:12px;padding:2px 10px;white-space:nowrap">🔄 Atualizado: {gerado_em or today_str}</span>
        </div>
      </div>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <button onclick="abrirResumo()" style="background:#2563eb;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap">📷 Resumo</button>
      <button onclick="iniciarRecorte()" style="background:#7c3aed;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap">✂️ Recortar</button>
      <a href="https://logusretail.tolvdesk.com/webapp/#/tickets/todos" target="_blank" title="Abrir Tolvdesk" style="background:#ea580c;color:#fff;border-radius:8px;padding:8px 18px;font-size:13px;font-weight:700;text-decoration:none;white-space:nowrap;display:flex;align-items:center;gap:6px">🔗 Tolvdesk</a>
    </div>
  </div>
  <div style="background:#f8fafc;border-bottom:1px solid #e2e8f0;padding:8px 28px;display:flex;gap:6px;align-items:center;flex-wrap:wrap">
    {dt_hdr_stats}
  </div>
  <div style="background:#f8fafc;border-bottom:1px solid #e2e8f0;padding:8px 28px;display:flex;gap:8px;align-items:center">
    <span style="color:#374151;font-size:10px;font-weight:700;margin-right:4px">DIAS EM ABERTO:</span>
    <span style="background:#dcfce7;color:#16a34a;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">0-3d</span>
    <span style="background:#fef9c3;color:#ca8a04;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">4-7d</span>
    <span style="background:#fff7ed;color:#ea580c;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">8-14d</span>
    <span style="background:#fee2e2;color:#dc2626;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">15-30d</span>
    <span style="background:#fee2e2;color:#991b1b;border-radius:4px;padding:3px 10px;font-size:11px;font-weight:700">+30d</span>
  </div>
  <div style="background:#ffffff;border-bottom:1px solid #e2e8f0;padding:0 28px;display:flex">
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
      {dt_donut}
      {dt_cli_details}
    </div>
    <div id="dv-resp" class="dview">
      <div style="color:#ea580c;font-size:10px;font-weight:700;letter-spacing:1px;margin-bottom:8px">🌿 EQUIPE SUL</div>
      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:12px">{dt_rsul_grid}</div>
      {dt_rsul_det}
      <div style="color:#7c3aed;font-size:10px;font-weight:700;letter-spacing:1px;margin:20px 0 8px">🏢 EQUIPE LOGUS</div>
      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:12px">{dt_rlogus_grid}</div>
      {dt_rlogus_det}
    </div>
    <div id="dv-cust" class="dview">
      <div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">
        <thead><tr style="border-bottom:2px solid #e2e8f0">
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">TICKET</th>
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">CLIENTE</th>
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">DESCRIÇÃO</th>
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">ESTIMATIVA</th>
          <th style="color:#475569;font-size:10px;font-weight:700;text-align:left;padding:8px 12px;background:#f8fafc">STATUS</th>
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
    <div style="display:flex;gap:6px;align-items:center">
      <button onclick="abrirResumo()" style="background:#2563eb;color:#fff;border:none;border-radius:6px;padding:6px 10px;font-size:11px;font-weight:700;cursor:pointer">📷</button>
      <button onclick="iniciarRecorte()" style="background:#7c3aed;color:#fff;border:none;border-radius:6px;padding:6px 10px;font-size:11px;font-weight:700;cursor:pointer">✂️</button>
      <span style="color:#16a34a;font-size:10px;font-weight:800;background:#dcfce7;border:1px solid #86efac;border-radius:10px;padding:3px 8px;white-space:nowrap">🔄 {gerado_em or today_str}</span>
    </div>
  </div>
  <div class="stats">
    <div class="stat"><div class="stat-n" style="color:#ea580c">{n_cli}</div><div class="stat-l">CLIENTES</div></div>
    <div class="stat"><div class="stat-n" style="color:#ea580c">{tot}</div><div class="stat-l">CHAMADOS</div></div>
    <div class="stat"><div class="stat-n" style="color:#dc2626">{tot_inc}</div><div class="stat-l">INCIDENTES</div></div>
    <div class="stat"><div class="stat-n" style="color:#ea580c;animation:pulse 1.4s infinite">{n_urg}</div><div class="stat-l">URGENTES</div></div>
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

<div id="resumo-data" style="display:none">{resumo_html}</div>

</body></html>"""
