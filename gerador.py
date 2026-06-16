from datetime import date
from collections import defaultdict

SUL_EMP = {
    'GUMZ','MERCADO DE BEBIDA POP','MILANI','PARANA SUPERMERCADO',
    'MAIS BRASIL - VAREJUS','MAIS BRASIL - MMR','CASA DE CARNES PETRY',
    'VICARI','MERCADO LEAL','SUPER PRINCESA','YPE SUPERMERCADO',
    'SUPERMERCADO KAIO','BECKER','TILL DA CARNE','ANGELINA SUPERMERCADO',
    'SUPERMERCADO MATHEUS','Supermercado Matheus','SCHUTZE','ANGELINO',
}
SUL_RESP  = {'Henrique Wolfram','Carlos Viana','Marcio Amorin','Rafael Beckert','— Sem Responsável —'}
SUL_TEAM  = {'Henrique Wolfram','Rafael Beckert'}

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

URG_PDV   = {'25596','25090','24651'}
URG_ERP   = {'25628','25647','25648','23301','24846','25173'}
URG_DEV   = {'24760','24621','25368'}
URG_ALL   = URG_PDV | URG_ERP | URG_DEV
RESP_OWN  = {'Comercial','Engenharia Software','Desenv. PDV','Sustentação Desenv.'}

BACKLOG = [
    {'num':1,  'data':'10/12/2025','ticket':'21979','cliente':'YPÊ',          'desc':'Emissão de MDF-e',                                                               'est':'16/03','status':'Homologado'},
    {'num':2,  'data':'23/12/2025','ticket':'22206','cliente':'YPÊ',          'desc':'Emissão de NF para CPF com IE',                                                  'est':'16/03','status':'Homologado'},
    {'num':3,  'data':'28/10/2024','ticket':'12752','cliente':'LEAL',         'desc':'Adequação a mudança de Legislação - NT 2023.004',                                'est':'31/03','status':'Homologado'},
    {'num':4,  'data':'06/10/2023','ticket':'6197', 'cliente':'VICARI',       'desc':'Parametrização Custo no Balanço Comercial',                                      'est':'22/04','status':'Em Homologação'},
    {'num':5,  'data':'09/04/2026','ticket':'24348','cliente':'GUMZ JARAGUA', 'desc':'Prazo de pagamento diferenciado por cliente',                                    'est':'04/05','status':'Homologado'},
    {'num':6,  'data':'16/05/2025','ticket':'16783','cliente':'LEAL',         'desc':'Número do Pedido de Compras em Campo Específico',                                'est':'05/05','status':'Em Homologação'},
    {'num':7,  'data':'28/04/2026','ticket':'24705','cliente':'LEAL',         'desc':'Sistema não abatendo ICMS ST retido da Base no cálculo ICMS próprio',           'est':'11/05','status':'Homologado'},
    {'num':8,  'data':'06/05/2026','ticket':'24839','cliente':'GUMZ POMERODE','desc':'Trazer produtos ativos por filial na tela de pesquisa de produtos',              'est':'19/05','status':'Homologado'},
    {'num':9,  'data':'24/06/2025','ticket':'17727','cliente':'GUMZ JARAGUA', 'desc':'Desconto em Forma de Recebimento',                                               'est':'14/05','status':'Em Homologação'},
    {'num':10, 'data':'06/09/2024','ticket':'11753','cliente':'GUMZ JARAGUA', 'desc':'Relatório Contas a Receber',                                                     'est':'25/05','status':'Em Homologação'},
    {'num':11, 'data':'12/06/2024','ticket':'10223','cliente':'ANGELINO',     'desc':'Juros Acréscimo não lista na Manutenção de Recebimentos e no Relatório',        'est':'25/05','status':'Em Homologação'},
    {'num':12, 'data':'16/05/2025','ticket':'16761','cliente':'SCHUTZE',      'desc':'Exibir dados históricos na manutenção do pedido automático',                    'est':'03/06','status':'Em Homologação'},
    {'num':13, 'data':'28/10/2024','ticket':'12755','cliente':'VICARI',       'desc':'Crédito de Diferimento - Apuração e Preço de Venda',                            'est':'24/07','status':'Em Roadmap'},
    {'num':14, 'data':'22/04/2025','ticket':'16219','cliente':'LEAL',         'desc':'SPED FISCAL - Ajuste de Crédito (junto com #12755)',                            'est':'24/07','status':'Em Roadmap'},
    {'num':15, 'data':'26/10/2023','ticket':'6497', 'cliente':'VICARI',       'desc':'Baixas Uso/Consumo no Balanço Comercial',                                       'est':'03/07','status':'Em Roadmap'},
    {'num':16, 'data':'02/10/2025','ticket':'20278','cliente':'VICARI',       'desc':'ICMS Desonerado na Entrada da NF',                                              'est':'04/09','status':'Em Roadmap'},
    {'num':17, 'data':'10/10/2025','ticket':'20484','cliente':'ANGELINO',     'desc':'Campo Juros Baixa Recebimento',                                                 'est':'',     'status':'Pendente'},
    {'num':18, 'data':'12/06/2023','ticket':'4255', 'cliente':'PRINCESA',     'desc':'Troco Solidário',                                                               'est':'',     'status':'Pendente'},
    {'num':19, 'data':'23/10/2023','ticket':'6451', 'cliente':'PRINCESA',     'desc':'Emissão Notas Fiscais a partir do PDV',                                         'est':'',     'status':'Pendente'},
    {'num':20, 'data':'16/05/2025','ticket':'16782','cliente':'LEAL',         'desc':'Venda a Órgão Público com Retenção do IRRF',                                    'est':'',     'status':'Pendente'},
    {'num':21, 'data':'11/02/2026','ticket':'23172','cliente':'LEAL',         'desc':'Sistema não considerando abatimento do ICMS desonerado',                        'est':'',     'status':'Pendente'},
    {'num':22, 'data':'26/01/2026','ticket':'22787','cliente':'LEAL',         'desc':'Erro ao finalizar NF',                                                          'est':'',     'status':'Pendente'},
    {'num':23, 'data':'02/03/2026','ticket':'23568','cliente':'LEAL',         'desc':'Erro ao finalizar NF',                                                          'est':'',     'status':'Pendente'},
    {'num':24, 'data':'28/08/2025','ticket':'19372','cliente':'LEAL',         'desc':'Venda para cliente fora do estado',                                             'est':'',     'status':'Pendente'},
    {'num':25, 'data':'27/11/2025','ticket':'21652','cliente':'LEAL',         'desc':'Formas de Recebimento - Boleto',                                                'est':'',     'status':'Pendente'},
    {'num':26, 'data':'27/05/2026','ticket':'25271','cliente':'MILANI',       'desc':'Adicionar filtro de seleção de NF na tela de alteração de preços',              'est':'',     'status':'Pendente'},
    {'num':27, 'data':'03/02/2026','ticket':'22981','cliente':'SCHUTZE',      'desc':'Cliente só consegue selecionar uma nota em documentos de devolução referenciados','est':'','status':'Pendente'},
    {'num':28, 'data':'03/06/2026','ticket':'25443','cliente':'GUMZ',         'desc':'Parâmetros PDV - Operações que Exigem Supervisor',                             'est':'URGENTE','status':'Urgente'},
    {'num':29, 'data':'30/03/2026','ticket':'24134','cliente':'LEAL',         'desc':'Limitação no Logus PDV – ausência de observação na NF-e',                      'est':'',     'status':'Pendente'},
]

# ── helpers ────────────────────────────────────────────────────────────────────
def dias_style(d):
    if d<=3:  return '#4ade80','#052e16','#14532d'
    if d<=7:  return '#fde047','#1c1a00','#3a3500'
    if d<=14: return '#fb923c','#1c0a00','#3a1a00'
    if d<=30: return '#f87171','#1c0000','#3a0000'
    if d<=90: return '#ef4444','#1a0000','#380000'
    return '#dc2626','#150000','#2e0000'

def status_html(s):
    cfg = {'Novo':('1d4ed8','bfdbfe','3b82f6','NOVO'),'Em andamento':('15803d','bbf7d0','22c55e','ANDAMENTO'),'Aguardando':('92400e','fde68a','d97706','AGUARDANDO')}
    bg,txt,bd,lbl = cfg.get(s,('374151','d1d5db','6b7280',s.upper()))
    return f'<span style="background:#{bg};color:#{txt};border:1px solid #{bd};border-radius:3px;padding:2px 8px;font-size:8px;font-weight:900;white-space:nowrap">{lbl}</span>'

def tipo_html(t):
    cfg = {'Incidente':('7f1d1d','fca5a5','ef4444','🔴 INCIDENTE'),'Requisição':('1e3a8a','bfdbfe','60a5fa','🔵 REQUISIÇÃO'),'Dúvida':('4c1d95','ddd6fe','a78bfa','🟣 DÚVIDA')}
    bg,txt,bd,lbl = cfg.get(t,('1f2937','9ca3af','6b7280',t or '?'))
    return f'<span style="background:#{bg};color:#{txt};border:1px solid #{bd};border-radius:3px;padding:2px 6px;font-size:8px;font-weight:700;white-space:nowrap">{lbl}</span>'

def anchor(s):
    for ch in ' /-.—': s=s.replace(ch,'_')
    return s

def summary_cards(tks):
    cnt=len(tks); inc=sum(1 for t in tks if t['tipo']=='Incidente')
    req=sum(1 for t in tks if t['tipo']=='Requisição')
    nov=sum(1 for t in tks if t['status']=='Novo'); ag=sum(1 for t in tks if t['status']=='Aguardando')
    mx=max(t['dias'] for t in tks) if tks else 0; mc='#ef4444' if mx>30 else '#fde047' if mx>7 else '#4ade80'
    def card(bg,bd,val,lbl): return (f'<div style="background:{bg};border:1px solid {bd};border-radius:4px;padding:4px 10px;text-align:center">'
        f'<div style="color:{bd};font-size:17px;font-weight:900">{val}</div><div style="color:{bd};font-size:7px;opacity:.7">{lbl}</div></div>')
    h=card('#0f0f0f','#475569',cnt,'TOTAL')
    if inc: h+=card('#1a0000','#ef4444',inc,'INCIDENTE')
    if req: h+=card('#0f1a30','#3b82f6',req,'REQUISIÇÃO')
    if ag:  h+=card('#150e00','#d97706',ag,'AGUARDANDO')
    if nov: h+=card('#0a1a0a','#22c55e',nov,'NOVOS')
    h+=card('#0a0a0a',mc,f'{mx}d','MAIS ANTIGO')
    return h

def ticket_table(tks_s, show_cliente=False, show_resp=False):
    th=lambda lbl,w='': f'<th style="color:#64748b;font-size:7.5px;padding:4px 8px;text-align:left{chr(59)+"white-space:nowrap" if w else ""}">{lbl}</th>'
    thead=('<thead><tr style="background:#060606;border-bottom:1px solid #1f2937">'
           f'<th style="color:#a3e635;font-size:7.5px;padding:4px 8px;text-align:left;white-space:nowrap">TICKET</th>'
           +(th('CLIENTE') if show_cliente else '')+th('TIPO')+th('ASSUNTO')+th('ESTADO')
           +(th('COM QUEM','1') if show_resp else '')+th('ABERTURA','1')
           +'<th style="color:#64748b;font-size:7.5px;padding:4px 8px;text-align:center">DIAS</th></tr></thead>')
    rows=''
    for i,t in enumerate(tks_s):
        fc,bg,bd=dias_style(t['dias']); zb='#080808' if i%2==0 else '#0d0d0d'
        rows+=(f'<tr style="background:{zb};border-bottom:1px solid #111">'
               f'<td style="padding:4px 8px;white-space:nowrap"><span style="color:#a3e635;font-weight:900;font-size:11px">#{t["code"]}</span></td>'
               +(f'<td style="padding:4px 9px;color:#f1f5f9;font-size:9px;font-weight:700;white-space:nowrap">{t["empresa"]}</td>' if show_cliente else '')
               +f'<td style="padding:4px 8px">{tipo_html(t["tipo"])}</td>'
               +f'<td style="padding:4px 8px;color:#e2e8f0;font-size:9.5px;max-width:310px;word-break:break-word">{t["assunto"]}</td>'
               +f'<td style="padding:4px 8px">{status_html(t["status"])}</td>'
               +(f'<td style="padding:4px 9px;color:#94a3b8;font-size:8.5px;white-space:nowrap">{t["atrib"]}</td>' if show_resp else '')
               +f'<td style="padding:4px 8px;color:#475569;font-size:8.5px;white-space:nowrap">{t["data"]}</td>'
               +f'<td style="background:{bg};border-left:3px solid {fc};padding:4px 10px;text-align:center;white-space:nowrap">'
               +f'<span style="color:{fc};font-weight:900;font-size:13px">{t["dias"]}</span>'
               +f'<span style="color:{fc};font-size:7px;opacity:.7"> d</span></td></tr>')
    return f'<table style="width:100%;border-collapse:collapse"><thead>{thead}</thead><tbody>{rows}</tbody></table>'

def _dc(d): return 'd0' if d<=3 else 'd3' if d<=7 else 'd7' if d<=14 else 'd14' if d<=30 else 'd99'

def _urg_row(t,cls):
    return (f'<tr><td class="{cls}">#{t["code"]}</td>'
            f'<td class="dt">{t["data"]}</td><td class="{_dc(t["dias"])}">{t["dias"]} dias</td>'
            f'<td class="cli">{t["empresa"]}</td><td class="desc">{t["assunto"]}</td>'
            f'<td class="resp">{t["atrib"]}</td><td>{status_html(t["status"])}</td></tr>')

def _bar(val,total,color):
    pct=(val/total*100) if total else 0
    return (f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:2px">'
            f'<div style="flex:1;background:#0f172a;border-radius:3px;height:14px;overflow:hidden">'
            f'<div style="width:{pct:.0f}%;background:{color};height:100%;border-radius:3px"></div></div>'
            f'<span style="color:{color};font-weight:900;font-size:11px;min-width:22px">{val}</span>'
            f'<span style="color:#374151;font-size:8px;min-width:26px">{pct:.0f}%</span></div>')

# ── entry point ────────────────────────────────────────────────────────────────
def gerar_html(all_tks, baixados_hoje=None):
    today     = date.today()
    today_str = today.strftime('%d/%m/%Y')
    baixados_hoje = baixados_hoje or []

    # patches
    for t in all_tks:
        if t['code'] in PATCHES:
            t.update(PATCHES[t['code']])

    # Sul set dinâmico
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
    sort_resp  = lambda r: (-(sum(1 for t in by_resp[r] if t['tipo']=='Incidente')), -len(by_resp[r]))
    resp_sul   = sorted([r for r in by_resp if r in SUL_RESP],    key=sort_resp)
    resp_logus = sorted([r for r in by_resp if r not in SUL_RESP], key=sort_resp)

    tot=len(sul); tot_inc=sum(1 for t in sul if t['tipo']=='Incidente')
    tot_ag=sum(1 for t in sul if t['status']=='Aguardando'); tot_nov=sum(1 for t in sul if t['status']=='Novo')

    # resp blocks
    def build_resp_block(resp_list, prefix):
        nav=''
        for resp in resp_list:
            tks=by_resp[resp]; inc=sum(1 for t in tks if t['tipo']=='Incidente')
            mx=max(t['dias'] for t in tks) if tks else 0
            bdr='#ef4444' if inc else '#3b82f6'; bgc='#1a0000' if inc else '#0a0f1a'
            nav+=(f'<a href="#{prefix}_{anchor(resp)}" style="display:flex;flex-direction:column;align-items:center;background:{bgc};border:1px solid {bdr};border-radius:5px;padding:4px 9px;text-decoration:none;min-width:110px;gap:1px">'
                  f'<span style="color:#e5e7eb;font-size:8.5px;font-weight:900;text-align:center">{resp}</span>'
                  f'<span style="color:{bdr};font-size:10px;font-weight:900">{len(tks)} tickets</span>'
                  +(f'<span style="color:#ef4444;font-size:7px">⚠ {inc} inc</span>' if inc else '')
                  +(f'<span style="color:#f87171;font-size:7px">{mx}d</span>' if mx>30 else '')+'</a>')
        secs=''
        for resp in resp_list:
            tks=by_resp[resp]; tks_s=sorted(tks,key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias']))
            inc=sum(1 for t in tks if t['tipo']=='Incidente')
            if inc>=5: hb,bd='#7f1d1d','#ef4444'
            elif inc>=2: hb,bd='#78350f','#f59e0b'
            elif inc>=1: hb,bd='#451a03','#d97706'
            else: hb,bd='#1e3a8a','#3b82f6'
            tags_cli=''.join(f'<span style="background:#0f172a;color:#94a3b8;border:1px solid #1e293b;border-radius:3px;padding:2px 7px;font-size:8px;font-weight:600">{c}</span> ' for c in dict.fromkeys(t['empresa'] for t in tks))
            secs+=(f'<div id="{prefix}_{anchor(resp)}" style="margin-bottom:18px;border:1px solid {bd};border-radius:6px;overflow:hidden">'
                   f'<div style="background:{hb};padding:7px 13px;border-bottom:1px solid {bd}">'
                   f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px">'
                   f'<div><div style="color:rgba(255,255,255,.45);font-size:7.5px;font-weight:700;letter-spacing:1px">RESPONSÁVEL</div>'
                   f'<div style="color:#fff;font-size:16px;font-weight:900">{resp}</div></div>'
                   f'<a href="#topo" style="color:rgba(255,255,255,.35);font-size:8px;text-decoration:none;margin-left:auto">↑ topo</a></div>'
                   f'<div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:6px">{summary_cards(tks)}</div>'
                   f'<div style="display:flex;align-items:center;gap:5px;flex-wrap:wrap"><span style="color:rgba(255,255,255,.4);font-size:7.5px;font-weight:700">CLIENTES:</span>{tags_cli}</div></div>'
                   +ticket_table(tks_s,show_cliente=True,show_resp=False)+'</div>')
        return nav,secs

    # cliente nav+secs
    nav_cli=''
    for emp in clientes:
        tks=by_cli[emp]; inc=sum(1 for t in tks if t['tipo']=='Incidente'); mx=max(t['dias'] for t in tks) if tks else 0
        bdr='#ef4444' if inc else '#ea580c'; bgc='#1a0000' if inc else '#1a0800'
        nav_cli+=(f'<a href="#cli_{anchor(emp)}" style="display:flex;flex-direction:column;align-items:center;background:{bgc};border:1px solid {bdr};border-radius:5px;padding:4px 9px;text-decoration:none;min-width:100px;gap:1px">'
                  f'<span style="color:#e5e7eb;font-size:8.5px;font-weight:900;text-align:center">{emp}</span>'
                  f'<span style="color:{bdr};font-size:10px;font-weight:900">{len(tks)} tickets</span>'
                  +(f'<span style="color:#ef4444;font-size:7px">⚠ {inc} inc</span>' if inc else '')
                  +(f'<span style="color:#f87171;font-size:7px">{mx}d</span>' if mx>30 else '')+'</a>')

    secs_cli=''
    for emp in clientes:
        tks=by_cli[emp]; tks_s=sorted(tks,key=lambda x:(0 if x['tipo']=='Incidente' else 1,-x['dias']))
        inc=sum(1 for t in tks if t['tipo']=='Incidente')
        if inc>=3: hb,bd='#7f1d1d','#ef4444'
        elif inc>=1: hb,bd='#78350f','#f59e0b'
        else: hb,bd='#180e00','#ea580c'
        tags_resp=''.join(f'<span style="background:#0f172a;color:#94a3b8;border:1px solid #1e293b;border-radius:3px;padding:2px 7px;font-size:8px;font-weight:600">{r}</span> ' for r in dict.fromkeys(t['atrib'] for t in tks))
        secs_cli+=(f'<div id="cli_{anchor(emp)}" style="margin-bottom:18px;border:1px solid {bd};border-radius:6px;overflow:hidden">'
                   f'<div style="background:{hb};padding:7px 13px;border-bottom:1px solid {bd}">'
                   f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px">'
                   f'<span style="color:#fff;font-size:15px;font-weight:900">{emp}</span>'
                   f'<a href="#topo" style="color:rgba(255,255,255,.35);font-size:8px;text-decoration:none;margin-left:auto">↑ topo</a></div>'
                   f'<div style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:6px">{summary_cards(tks)}</div>'
                   f'<div style="display:flex;align-items:center;gap:5px;flex-wrap:wrap"><span style="color:rgba(255,255,255,.4);font-size:7.5px;font-weight:700">COM QUEM:</span>{tags_resp}</div></div>'
                   +ticket_table(tks_s,show_cliente=False,show_resp=True)+'</div>')

    nav_rs,secs_rs=build_resp_block(resp_sul,'rs')
    nav_rl,secs_rl=build_resp_block(resp_logus,'rl')
    tot_rs_tks=sum(len(by_resp[r]) for r in resp_sul); tot_rs_inc=sum(sum(1 for t in by_resp[r] if t['tipo']=='Incidente') for r in resp_sul)
    tot_rl_tks=sum(len(by_resp[r]) for r in resp_logus); tot_rl_inc=sum(sum(1 for t in by_resp[r] if t['tipo']=='Incidente') for r in resp_logus)

    legenda=''.join(f'<span style="background:{bg};color:{fc};border:1px solid {bd};border-radius:3px;padding:2px 7px;font-size:8px;font-weight:700">{lbl}</span> '
                    for fc,bg,bd,lbl in [dias_style(2)+('0–3d',),dias_style(5)+('4–7d',),dias_style(10)+('8–14d',),dias_style(20)+('15–30d',),dias_style(60)+('31–90d',),dias_style(200)+('+90d',)])

    # customizações
    grp_urg=[b for b in BACKLOG if b['status']=='Urgente']; grp_hom=[b for b in BACKLOG if b['status']=='Homologado']
    grp_hom2=[b for b in BACKLOG if b['status']=='Em Homologação']; grp_road=[b for b in BACKLOG if b['status']=='Em Roadmap']
    grp_pend=[b for b in BACKLOG if b['status']=='Pendente']
    tot_cust=len(BACKLOG); tot_hom=len(grp_hom); tot_hom2=len(grp_hom2); tot_road=len(grp_road); tot_pend=len(grp_pend); tot_urg_c=len(grp_urg)

    def _badge_cust(s):
        if s=='Urgente':        return '<span style="background:#1a0000;color:#f87171;border:1px solid #ef4444;border-radius:3px;padding:2px 9px;font-size:8px;font-weight:900">🔴 URGENTE</span>'
        if s=='Homologado':     return '<span style="background:#052e16;color:#4ade80;border:1px solid #22c55e;border-radius:3px;padding:2px 9px;font-size:8px;font-weight:900">✓ Homologado</span>'
        if s=='Em Homologação': return '<span style="background:#1c0a00;color:#fdba74;border:1px solid #fb923c;border-radius:3px;padding:2px 9px;font-size:8px;font-weight:900">◎ Em Homologação</span>'
        if s=='Em Roadmap':     return '<span style="background:#0a0f1a;color:#93c5fd;border:1px solid #60a5fa;border-radius:3px;padding:2px 9px;font-size:8px;font-weight:900">◉ Em Roadmap</span>'
        return '<span style="background:#111;color:#9ca3af;border:1px solid #374151;border-radius:3px;padding:2px 9px;font-size:8px;font-weight:900">— Pendente</span>'

    def _table_cust(items):
        rows=''
        for i,b in enumerate(items):
            zb='#080808' if i%2==0 else '#0e0e0e'
            est_txt=(f'<span style="color:#f87171;font-weight:900">{b["est"]}</span>' if b['est']=='URGENTE' else f'<span style="color:#94a3b8">{b["est"]}</span>')
            rows+=(f'<tr style="background:{zb};border-bottom:1px solid #111">'
                   f'<td style="padding:4px 8px;color:#6b4c30;font-size:9px;font-weight:900;text-align:center">{b["num"]}</td>'
                   f'<td style="padding:4px 8px;white-space:nowrap"><span style="color:#f97316;font-weight:900;font-size:11px">#{b["ticket"]}</span></td>'
                   f'<td style="padding:4px 9px;color:#fed7aa;font-size:9px;font-weight:700;white-space:nowrap">{b["cliente"]}</td>'
                   f'<td style="padding:4px 9px;color:#e2e8f0;font-size:9.5px">{b["desc"]}</td>'
                   f'<td style="padding:4px 8px;color:#64748b;font-size:8px;white-space:nowrap">{b["data"]}</td>'
                   f'<td style="padding:4px 9px;text-align:center">{est_txt}</td>'
                   f'<td style="padding:4px 9px">{_badge_cust(b["status"])}</td></tr>')
        return rows

    def _grp_h(titulo,cor,bg,n):
        return (f'<div style="background:{bg};border-left:4px solid {cor};border-radius:4px;padding:7px 14px;margin:14px 0 4px;display:flex;align-items:center;gap:10px">'
                f'<span style="color:{cor};font-size:12px;font-weight:900">{titulo}</span>'
                f'<span style="background:rgba(0,0,0,.3);color:{cor};border-radius:3px;padding:1px 9px;font-size:9px;font-weight:700">{n} item{"s" if n!=1 else ""}</span></div>')

    thead_c=('<table style="width:100%;border-collapse:collapse;margin-bottom:4px"><thead><tr style="background:#060606;border-bottom:1px solid #1f2937">'
             '<th style="color:#6b4c30;font-size:7.5px;padding:3px 8px;width:34px;text-align:center">#</th>'
             '<th style="color:#6b4c30;font-size:7.5px;padding:3px 8px;text-align:left">TICKET</th>'
             '<th style="color:#6b4c30;font-size:7.5px;padding:3px 8px;text-align:left">CLIENTE</th>'
             '<th style="color:#64748b;font-size:7.5px;padding:3px 9px;text-align:left">DESCRIÇÃO</th>'
             '<th style="color:#64748b;font-size:7.5px;padding:3px 8px;text-align:left">ABERTURA</th>'
             '<th style="color:#64748b;font-size:7.5px;padding:3px 9px;text-align:center">EST. HOMOLOG.</th>'
             '<th style="color:#64748b;font-size:7.5px;padding:3px 9px;text-align:left">STATUS</th>'
             '</tr></thead><tbody>')

    sec_cust=''
    if grp_urg:  sec_cust+=_grp_h('🔴 URGENTE','#ef4444','#1a0000',len(grp_urg))+thead_c+_table_cust(grp_urg)+'</tbody></table>'
    if grp_hom2: sec_cust+=_grp_h('◎ Em Homologação','#fb923c','#1a0800',len(grp_hom2))+thead_c+_table_cust(grp_hom2)+'</tbody></table>'
    if grp_road: sec_cust+=_grp_h('◉ Em Roadmap','#60a5fa','#050f1a',len(grp_road))+thead_c+_table_cust(grp_road)+'</tbody></table>'
    if grp_pend: sec_cust+=_grp_h('— Pendente','#6b7280','#0a0a0a',len(grp_pend))+thead_c+_table_cust(grp_pend)+'</tbody></table>'
    if grp_hom:  sec_cust+=_grp_h('✓ Homologado','#22c55e','#041a04',len(grp_hom))+thead_c+_table_cust(grp_hom)+'</tbody></table>'

    # urgentes
    _tk_lkp={t['code']:t for t in all_tks}
    def _sec(codes): return sorted([t for t in sul if t['code'] in codes],key=lambda x:-x['dias'])
    def _sec_a(atrib): return sorted([t for t in sul if t['atrib']==atrib and t['code'] not in URG_ALL],key=lambda x:-x['dias'])

    pdv_tks=_sec(URG_PDV); erp_tks=_sec(URG_ERP)
    eng_tks=_sec_a('Engenharia Software'); pdvd_tks=_sec_a('Desenv. PDV')
    sust_tks=_sec_a('Sustentação Desenv.'); com_tks=_sec_a('Comercial')

    alta_tks=[t for t in sul if t['code'] not in URG_ALL and t['atrib'] not in RESP_OWN]
    alta_by_cli=defaultdict(list)
    for _t in alta_tks: alta_by_cli[_t['empresa']].append(_t)
    alta_clis=sorted(alta_by_cli,key=lambda c:-max(t['dias'] for t in alta_by_cli[c]))

    def _alta_cli_rows(emp,tks):
        n=len(tks); mx=max(t['dias'] for t in tks); mc='#ef4444' if mx>30 else '#fde047' if mx>7 else '#4ade80'
        hdr=(f'<tr style="background:#060e1e"><td colspan="7" style="padding:5px 10px;border-top:2px solid #1e3a8a">'
             f'<span style="color:#93c5fd;font-size:9px;font-weight:900;letter-spacing:.8px">{emp}</span>'
             f'&nbsp;&nbsp;<span style="color:#475569;font-size:8px">{n} ticket{"s" if n>1 else ""}</span>'
             f'&nbsp;&nbsp;<span style="color:{mc};font-size:8px;font-weight:700">até {mx}d</span></td></tr>')
        return hdr+''.join(_urg_row(t,'num-e') for t in sorted(tks,key=lambda x:-x['dias']))

    n_pdv=len(pdv_tks); n_erp=len(erp_tks); n_alta=len(alta_tks)
    n_eng=len(eng_tks); n_pdvd=len(pdvd_tks); n_sust=len(sust_tks); n_com=len(com_tks)
    n_urg_tot=n_pdv+n_erp+n_alta+n_eng+n_pdvd+n_sust+n_com+3

    alta_rows=''.join(_alta_cli_rows(c,alta_by_cli[c]) for c in alta_clis)
    pdv_rows=''.join(_urg_row(t,'num-p') for t in pdv_tks)
    erp_rows=''.join(_urg_row(t,'num-a') for t in erp_tks)
    eng_rows=''.join(_urg_row(t,'num-en') for t in eng_tks)
    pdvd_rows=''.join(_urg_row(t,'num-dp') for t in pdvd_tks)
    sust_rows=''.join(_urg_row(t,'num-st') for t in sust_tks)
    com_rows=''.join(_urg_row(t,'num-c') for t in com_tks)

    def _dev_row(code,fallback_emp,fallback_desc):
        t=_tk_lkp.get(code)
        if t: return _urg_row(t,'num-d')
        return f'<tr><td class="num-d">#{code}</td><td class="dt">—</td><td>—</td><td class="cli">{fallback_emp}</td><td class="desc">{fallback_desc}</td><td class="resp">—</td><td>—</td></tr>'

    dev_rows=(_dev_row('24760','GUMZ','Erro Finalização notas do simples nacional')
             +_dev_row('24621','VICARI','Controle de trocas — Erro filtro Filiais')
             +_dev_row('25368','BEBIDA POP','Emissão de NF — Transformar Pedido em NF'))

    # resultados
    hoje_tks=sorted([t for t in sul if t['dias']==0],key=lambda x:x['empresa'])
    n_hoje=len(hoje_tks); n_hoje_inc=sum(1 for t in hoje_tks if t['tipo']=='Incidente')
    resol_hoje=sorted(baixados_hoje,key=lambda x:x.get('empresa',''))
    n_resol=len(resol_hoje)

    n_nov=sum(1 for t in sul if t['status']=='Novo')
    n_and=sum(1 for t in sul if t['status']=='Em andamento')
    n_agu=sum(1 for t in sul if t['status']=='Aguardando')
    n_inc=sum(1 for t in sul if t['tipo']=='Incidente')
    n_req=sum(1 for t in sul if t['tipo']=='Requisição')
    n_duv=sum(1 for t in sul if t['tipo']=='Dúvida')

    cli_rank=sorted([(e,len(by_cli[e]),sum(1 for t in by_cli[e] if t['tipo']=='Incidente')) for e in clientes],key=lambda x:-x[1])
    all_r=set(t['atrib'] for t in sul)
    resp_rank=sorted([(r,len(by_resp[r]),sum(1 for t in by_resp[r] if t['tipo']=='Incidente')) for r in all_r],key=lambda x:-x[1])[:12]

    hoje_rows=''.join(
        f'<tr style="background:{"#080808" if i%2==0 else "#0d0d0d"};border-bottom:1px solid #111">'
        f'<td style="padding:4px 8px;white-space:nowrap"><span style="color:#22c55e;font-weight:900;font-size:11px">#{t["code"]}</span></td>'
        f'<td style="padding:4px 9px;color:#f1f5f9;font-size:9px;font-weight:700">{t["empresa"]}</td>'
        f'<td style="padding:4px 8px">{tipo_html(t["tipo"])}</td>'
        f'<td style="padding:4px 8px;color:#e2e8f0;font-size:9.5px;max-width:320px;word-break:break-word">{t["assunto"]}</td>'
        f'<td style="padding:4px 9px;color:#94a3b8;font-size:8.5px">{t["atrib"]}</td>'
        f'<td style="padding:4px 8px">{status_html(t["status"])}</td></tr>'
        for i,t in enumerate(hoje_tks))

    max_cli=cli_rank[0][1] if cli_rank else 1
    cli_bars=''.join(
        f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:5px">'
        f'<div style="min-width:120px;color:#e2e8f0;font-size:8px;font-weight:700;text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{e}</div>'
        f'<div style="flex:1;background:#0f172a;border-radius:3px;height:18px;overflow:hidden">'
        f'<div style="width:{c/max_cli*100:.0f}%;background:#1d4ed8;height:100%;border-radius:3px;display:flex;align-items:center;padding-left:6px">'
        f'<span style="color:#93c5fd;font-size:9px;font-weight:900">{c}</span></div></div>'
        +(f' <span style="color:#ef4444;font-size:8px">⚠{i}</span>' if i else '')+'</div>'
        for e,c,i in cli_rank[:10])

    max_resp=resp_rank[0][1] if resp_rank else 1
    resp_bars=''.join(
        f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:5px">'
        f'<div style="min-width:110px;color:#e2e8f0;font-size:8px;font-weight:700;text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{r}</div>'
        f'<div style="flex:1;background:#0f172a;border-radius:3px;height:18px;overflow:hidden">'
        f'<div style="width:{c/max_resp*100:.0f}%;background:{"#ea580c" if r in SUL_RESP else "#7c3aed"};height:100%;border-radius:3px;display:flex;align-items:center;padding-left:6px">'
        f'<span style="color:#fed7aa;font-size:9px;font-weight:900">{c}</span></div></div>'
        +(f' <span style="color:#ef4444;font-size:8px">⚠{i}</span>' if i else '')+'</div>'
        for r,c,i in resp_rank)

    baixados_rows=''.join(
        f'<tr style="background:{"#080808" if i%2==0 else "#0d0d0d"};border-bottom:1px solid #111">'
        f'<td style="padding:4px 8px;white-space:nowrap"><span style="color:#22c55e;font-weight:900;font-size:11px">#{t["code"]}</span></td>'
        f'<td style="padding:4px 9px;color:#f1f5f9;font-size:9px;font-weight:700">{t.get("empresa","")}</td>'
        f'<td style="padding:4px 8px">{tipo_html(t.get("tipo",""))}</td>'
        f'<td style="padding:4px 8px;color:#e2e8f0;font-size:9.5px;max-width:320px;word-break:break-word">{t.get("assunto","")}</td>'
        f'<td style="padding:4px 9px;color:#94a3b8;font-size:8.5px">{t.get("atrib","")}</td>'
        f'<td style="padding:4px 8px;color:#4ade80;font-size:8.5px;font-weight:700">{t.get("resolucao","")}</td></tr>'
        for i,t in enumerate(resol_hoje))

    LOGO='''<svg width="110" height="34" viewBox="0 0 110 34" fill="none" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="26" font-family="Arial,sans-serif" font-weight="900" font-size="28" fill="#f97316" letter-spacing="-1">l</text>
  <circle cx="30" cy="17" r="10" stroke="#f97316" stroke-width="3.5" fill="none"/><circle cx="30" cy="17" r="4" fill="#f97316"/>
  <text x="43" y="26" font-family="Arial,sans-serif" font-weight="900" font-size="28" fill="#f97316" letter-spacing="-1">gus</text></svg>'''

    return f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta http-equiv="refresh" content="1800">
<title>Logus Sul BI · {today_str}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0c0c0c;color:#e5e7eb;font-family:"Segoe UI",Arial,sans-serif;padding:10px 14px}}
.tab{{cursor:pointer;padding:9px 22px;font-size:12px;font-weight:900;border-radius:6px 6px 0 0;border:1px solid #2a1800;border-bottom:none;color:#6b4c30;background:#0d0800;transition:all .15s;letter-spacing:.3px}}
.tab.on{{background:#1a0e00;color:#f97316;border-color:#ea580c;border-bottom:2px solid #f97316}}
.tab.on-cust{{background:#06050f;color:#a78bfa;border-color:#7c3aed;border-bottom:2px solid #a78bfa}}
.tab.on-urg{{background:#1a0505;color:#f87171;border-color:#dc2626;border-bottom:2px solid #ef4444;animation:none}}
.tab.on-res{{background:#020f02;color:#4ade80;border-color:#166534;border-bottom:2px solid #22c55e}}
@keyframes urgPulse{{0%,100%{{box-shadow:0 0 6px #dc2626,0 0 16px rgba(220,38,38,.4);border-color:#dc2626;color:#f87171;background:#160303}}50%{{box-shadow:0 0 18px #ef4444,0 0 36px rgba(239,68,68,.7);border-color:#ef4444;color:#fca5a5;background:#220606}}}}
#tab-urg:not(.on-urg){{animation:urgPulse 1.4s ease-in-out infinite;border-color:#dc2626;color:#f87171;background:#160303}}
.subtab{{cursor:pointer;padding:5px 18px;font-size:10px;font-weight:900;border-radius:5px 5px 0 0;border:1px solid #2a1800;border-bottom:none;color:#6b4c30;background:#080500;transition:all .15s}}
.subtab.on-sul{{background:#180e00;color:#f97316;border-color:#ea580c;border-bottom:2px solid #f97316}}
.subtab.on-logus{{background:#06050f;color:#a78bfa;border-color:#7c3aed;border-bottom:2px solid #a78bfa}}
#view-resp,#view-cust,#view-urg,#view-res{{display:none}}
#sub-logus{{display:none}}
#view-urg .u-header{{display:flex;justify-content:space-between;align-items:center;background:#0d1b3e;border-radius:6px;padding:6px 14px;margin-bottom:6px;border:1px solid #2563eb;border-left:5px solid #2563eb;position:sticky;top:120px;z-index:100;box-shadow:0 4px 12px rgba(0,0,0,.7)}}
#view-urg .ubadge{{font-size:10px;font-weight:900;padding:4px 12px;border-radius:4px;letter-spacing:.5px}}
#view-urg .u-sec{{font-size:9px;font-weight:900;letter-spacing:1.5px;text-transform:uppercase;padding:4px 12px;border-radius:5px 5px 0 0;margin-top:6px;display:flex;justify-content:space-between;align-items:center}}
#view-urg .u-cnt{{font-size:11px;font-weight:700}}
#view-urg .u-wrap{{border-radius:0 5px 5px 5px;overflow:hidden;margin-bottom:2px}}
#view-urg .u-wrap table{{width:100%;border-collapse:collapse}}
#view-urg .u-wrap thead th{{font-weight:900;font-size:8px;padding:3px 9px;text-align:left;white-space:nowrap;letter-spacing:.8px;border-bottom:2px solid rgba(255,255,255,.2)}}
#view-urg .u-wrap tbody tr{{border-bottom:1px solid rgba(255,255,255,.08)}}
#view-urg .u-wrap tbody td{{padding:3px 9px;font-size:10.5px;white-space:nowrap;line-height:1.4}}
#view-urg .ua-bg tbody tr{{background:#1a0303}} #view-urg .ua-bg tbody tr:nth-child(even){{background:#220505}} #view-urg .ua-th{{background:#7f1d1d;color:#fecaca}}
#view-urg .ue-bg tbody tr{{background:#050d20}} #view-urg .ue-bg tbody tr:nth-child(even){{background:#08122a}} #view-urg .ue-th{{background:#1e3a8a;color:#93c5fd}}
#view-urg .ud-bg tbody tr{{background:#0c0518}} #view-urg .ud-bg tbody tr:nth-child(even){{background:#110720}} #view-urg .ud-th{{background:#4c1d95;color:#ddd6fe}}
#view-urg .up-bg tbody tr{{background:#050f08}} #view-urg .up-bg tbody tr:nth-child(even){{background:#091408}} #view-urg .up-th{{background:#14532d;color:#bbf7d0}}
#view-urg .uen-bg tbody tr{{background:#0c1220}} #view-urg .uen-bg tbody tr:nth-child(even){{background:#111827}} #view-urg .uen-th{{background:#1e293b;color:#94a3b8}}
#view-urg .udp-bg tbody tr{{background:#061510}} #view-urg .udp-bg tbody tr:nth-child(even){{background:#0a1e17}} #view-urg .udp-th{{background:#0d3a2e;color:#5eead4}}
#view-urg .ust-bg tbody tr{{background:#0a0a1a}} #view-urg .ust-bg tbody tr:nth-child(even){{background:#10101f}} #view-urg .ust-th{{background:#312e81;color:#c7d2fe}}
#view-urg .uc-bg tbody tr{{background:#120a00}} #view-urg .uc-bg tbody tr:nth-child(even){{background:#1a1000}} #view-urg .uc-th{{background:#92400e;color:#fde68a}}
#view-urg .num-a{{color:#ff6b6b;font-weight:900;font-size:12px}} #view-urg .num-e{{color:#60a5fa;font-weight:900;font-size:12px}}
#view-urg .num-d{{color:#a78bfa;font-weight:900;font-size:12px}} #view-urg .num-p{{color:#4ade80;font-weight:900;font-size:12px}}
#view-urg .num-c{{color:#fbbf24;font-weight:900;font-size:12px}} #view-urg .num-en{{color:#94a3b8;font-weight:900;font-size:12px}}
#view-urg .num-dp{{color:#2dd4bf;font-weight:900;font-size:12px}} #view-urg .num-st{{color:#818cf8;font-weight:900;font-size:12px}}
#view-urg .ub-pdv{{background:#14532d;color:#bbf7d0;border:1px solid #22c55e}} #view-urg .ub-erp{{background:#7f1d1d;color:#fecaca;border:1px solid #ef4444}}
#view-urg .ub-aten{{background:#dc2626;color:#fff;border:1px solid #ef4444}} #view-urg .ub-eng{{background:#1e293b;color:#94a3b8;border:1px solid #475569}}
#view-urg .ub-pdvd{{background:#0d3a2e;color:#5eead4;border:1px solid #14b8a6}} #view-urg .ub-sust{{background:#312e81;color:#c7d2fe;border:1px solid #6366f1}}
#view-urg .ub-dev{{background:#7c3aed;color:#fff;border:1px solid #8b5cf6}} #view-urg .ub-com{{background:#78350f;color:#fde68a;border:1px solid #f59e0b}}
#view-urg .dt{{color:#94a3b8;font-size:9px}} #view-urg .desc{{color:#e2e8f0;white-space:normal;max-width:480px;word-break:break-word}}
#view-urg .cli{{color:#fbbf24;font-weight:700}} #view-urg .resp{{color:#94a3b8;font-size:8.5px;white-space:nowrap}}
#view-urg .d0{{color:#4ade80;font-weight:700}} #view-urg .d3{{color:#fde047;font-weight:700}} #view-urg .d7{{color:#fb923c;font-weight:700}}
#view-urg .d14{{color:#f87171;font-weight:700}} #view-urg .d99{{color:#dc2626;font-weight:900}}
</style>
<script>
function showMain(v){{
  ['cli','resp','cust','urg','res'].forEach(function(x){{document.getElementById('view-'+x).style.display=v===x?'block':'none'}});
  document.getElementById('tab-cli').className='tab'+(v==='cli'?' on':'');
  document.getElementById('tab-resp').className='tab'+(v==='resp'?' on':'');
  document.getElementById('tab-cust').className='tab'+(v==='cust'?' on-cust':'');
  document.getElementById('tab-urg').className='tab'+(v==='urg'?' on-urg':'');
  document.getElementById('tab-res').className='tab'+(v==='res'?' on-res':'');
}}
function showSub(v){{
  document.getElementById('sub-sul').style.display=v==='sul'?'block':'none';
  document.getElementById('sub-logus').style.display=v==='logus'?'block':'none';
  document.getElementById('stab-sul').className='subtab'+(v==='sul'?' on-sul':'');
  document.getElementById('stab-logus').className='subtab'+(v==='logus'?' on-logus':'');
}}
function fixUrgHeader(){{var h=document.getElementById('sticky-header');var u=document.querySelector('#view-urg .u-header');if(h&&u)u.style.top=h.offsetHeight+'px';}}
window.addEventListener('load',fixUrgHeader);window.addEventListener('resize',fixUrgHeader);
</script></head><body>

<div id="sticky-header" style="position:sticky;top:0;z-index:200;background:#0c0c0c;box-shadow:0 2px 12px rgba(0,0,0,.8)">
<div id="topo" style="background:#0d0800;border:2px solid #ea580c;border-radius:8px 8px 0 0;padding:10px 16px 8px;margin-bottom:0">
  <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-bottom:8px">
    <div style="display:flex;flex-direction:column;gap:2px">{LOGO}
      <div style="display:flex;align-items:center;gap:6px">
        <span style="background:#f97316;color:#000;font-size:8px;font-weight:900;padding:1px 8px;border-radius:3px;letter-spacing:1px">SUL</span>
        <span style="color:#6b4c30;font-size:9px">Painel de Chamados · {today_str}</span>
      </div></div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-left:auto">
      <div style="background:#180e00;border:1px solid #ea580c;border-radius:6px;padding:5px 13px;text-align:center"><div style="color:#fed7aa;font-size:20px;font-weight:900">{len(clientes)}</div><div style="color:#f97316;font-size:7px;font-weight:700;letter-spacing:.5px">CLIENTES</div></div>
      <div style="background:#180e00;border:1px solid #c2410c;border-radius:6px;padding:5px 13px;text-align:center"><div style="color:#fed7aa;font-size:20px;font-weight:900">{tot}</div><div style="color:#f97316;font-size:7px;font-weight:700;letter-spacing:.5px">CHAMADOS</div></div>
      <div style="background:#1a0505;border:1px solid #ef4444;border-radius:6px;padding:5px 13px;text-align:center"><div style="color:#fca5a5;font-size:20px;font-weight:900">{tot_inc}</div><div style="color:#f87171;font-size:7px;font-weight:700;letter-spacing:.5px">INCIDENTES</div></div>
      <div style="background:#1a1200;border:1px solid #d97706;border-radius:6px;padding:5px 13px;text-align:center"><div style="color:#fde68a;font-size:20px;font-weight:900">{tot_ag}</div><div style="color:#d97706;font-size:7px;font-weight:700;letter-spacing:.5px">AGUARDANDO</div></div>
      <div style="background:#0a1a0a;border:1px solid #22c55e;border-radius:6px;padding:5px 13px;text-align:center"><div style="color:#bbf7d0;font-size:20px;font-weight:900">{tot_nov}</div><div style="color:#22c55e;font-size:7px;font-weight:700;letter-spacing:.5px">NOVOS</div></div>
    </div></div>
  <div style="display:flex;align-items:center;gap:5px;flex-wrap:wrap;padding-top:7px;border-top:1px solid #2a1500">
    <span style="color:#6b4c30;font-size:8px;font-weight:700">DIAS EM ABERTO:</span>{legenda}</div>
</div>
<div style="display:flex;gap:3px;padding:0 2px;border-bottom:2px solid #ea580c;margin-bottom:0">
  <button id="tab-cli"  class="tab on"  onclick="showMain('cli')">📋&nbsp; Por Cliente</button>
  <button id="tab-resp" class="tab"     onclick="showMain('resp')">👤&nbsp; Por Responsável</button>
  <button id="tab-cust" class="tab"     onclick="showMain('cust')">🔧&nbsp; Customizações&nbsp;<span style="background:#1f0a40;color:#a78bfa;border-radius:3px;padding:1px 6px;font-size:9px">{tot_cust}</span></button>
  <button id="tab-urg"  class="tab"     onclick="showMain('urg')">🚨&nbsp; Urgentes do Dia&nbsp;<span style="background:#3a0000;color:#f87171;border-radius:3px;padding:1px 6px;font-size:9px">{n_urg_tot}</span></button>
  <button id="tab-res"  class="tab"     onclick="showMain('res')">📊&nbsp; Resultados&nbsp;<span style="background:#020f02;color:#4ade80;border-radius:3px;padding:1px 6px;font-size:9px">{n_hoje} hoje</span></button>
</div></div>
<div style="height:10px"></div>

<div id="view-cli">
  <div style="background:#100800;border:1px solid #ea580c;border-radius:6px;padding:7px 12px;margin-bottom:10px">
    <div style="color:#f97316;font-size:8px;font-weight:700;letter-spacing:.5px;margin-bottom:5px">CLIENTES — ACESSO RÁPIDO</div>
    <div style="display:flex;flex-wrap:wrap;gap:5px">{nav_cli}</div></div>
  {secs_cli}</div>

<div id="view-resp">
  <div style="display:flex;gap:4px;padding:8px 0 0;border-bottom:2px solid #2a1500;margin-bottom:12px;flex-wrap:wrap">
    <button id="stab-sul" class="subtab on-sul" onclick="showSub('sul')" style="display:flex;flex-direction:column;align-items:flex-start;padding:7px 16px;gap:2px">
      <span style="font-size:11px;font-weight:900">🌿 Logus Sul — Regional Sul</span>
      <span style="font-size:9px;opacity:.75;font-weight:400">Equipe própria: Henrique · Carlos · Marcio · Rafael</span>
      <span style="font-size:9px;font-weight:700">{len(resp_sul)} responsáveis · {tot_rs_tks} tickets · {tot_rs_inc} incidentes</span></button>
    <button id="stab-logus" class="subtab" onclick="showSub('logus')" style="display:flex;flex-direction:column;align-items:flex-start;padding:7px 16px;gap:2px">
      <span style="font-size:11px;font-weight:900">🏢 Logus — Equipe Matriz</span>
      <span style="font-size:9px;opacity:.75;font-weight:400">Suporte N2/N3, Sustentação, Desenvolvimento</span>
      <span style="font-size:9px;font-weight:700">{len(resp_logus)} responsáveis · {tot_rl_tks} tickets · {tot_rl_inc} incidentes</span></button>
  </div>
  <div id="sub-sul">
    <div style="background:#120900;border:1px solid #ea580c;border-radius:6px;padding:7px 12px;margin-bottom:10px">
      <div style="color:#f97316;font-size:8px;font-weight:700;letter-spacing:.5px;margin-bottom:5px">🌿 EQUIPE LOGUS SUL — ACESSO RÁPIDO</div>
      <div style="display:flex;flex-wrap:wrap;gap:5px">{nav_rs}</div></div>{secs_rs}</div>
  <div id="sub-logus">
    <div style="background:#06050f;border:1px solid #7c3aed;border-radius:6px;padding:7px 12px;margin-bottom:10px">
      <div style="color:#a78bfa;font-size:8px;font-weight:700;letter-spacing:.5px;margin-bottom:5px">🏢 EQUIPE LOGUS MATRIZ — ACESSO RÁPIDO</div>
      <div style="display:flex;flex-wrap:wrap;gap:5px">{nav_rl}</div></div>{secs_rl}</div>
</div>

<div id="view-cust">
  <div style="background:#06050f;border:1px solid #7c3aed;border-radius:6px;padding:10px 14px;margin-bottom:12px">
    <div style="color:#a78bfa;font-size:9px;font-weight:700;letter-spacing:.5px;margin-bottom:8px">🔧 BACKLOG CUSTOMIZAÇÕES LOGUS SUL</div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      <div style="background:#0d0b1a;border:1px solid #7c3aed;border-radius:6px;padding:5px 14px;text-align:center"><div style="color:#c4b5fd;font-size:20px;font-weight:900">{tot_cust}</div><div style="color:#a78bfa;font-size:7px;font-weight:700">TOTAL</div></div>
      <div style="background:#1a0800;border:1px solid #fb923c;border-radius:6px;padding:5px 14px;text-align:center"><div style="color:#fdba74;font-size:20px;font-weight:900">{tot_hom2}</div><div style="color:#fb923c;font-size:7px;font-weight:700">EM HOMOLOGAÇÃO</div></div>
      <div style="background:#050f1a;border:1px solid #60a5fa;border-radius:6px;padding:5px 14px;text-align:center"><div style="color:#93c5fd;font-size:20px;font-weight:900">{tot_road}</div><div style="color:#60a5fa;font-size:7px;font-weight:700">EM ROADMAP</div></div>
      <div style="background:#0a0a0a;border:1px solid #374151;border-radius:6px;padding:5px 14px;text-align:center"><div style="color:#9ca3af;font-size:20px;font-weight:900">{tot_pend}</div><div style="color:#6b7280;font-size:7px;font-weight:700">PENDENTE</div></div>
      <div style="background:#041a04;border:1px solid #22c55e;border-radius:6px;padding:5px 14px;text-align:center"><div style="color:#bbf7d0;font-size:20px;font-weight:900">{tot_hom}</div><div style="color:#4ade80;font-size:7px;font-weight:700">HOMOLOGADO</div></div>
    </div></div>
  {sec_cust}</div>

<div id="view-urg">
  <div class="u-header">
    <div><div style="color:#fff;font-size:14px;font-weight:900">🚨 Chamados Urgentes — {today_str}</div>
    <div style="font-size:9px;color:#7ba7ff;margin-top:2px">Emergencial → Alta → Desenvolvimento</div></div>
    <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">
      <span class="ubadge ub-pdv">PDV 🔴 {n_pdv}</span><span class="ubadge ub-erp">ERP 🔴 {n_erp}</span>
      <span class="ubadge ub-aten">ALTA {n_alta}</span><span class="ubadge ub-eng">ENG {n_eng}</span>
      <span class="ubadge ub-pdvd">DEV PDV {n_pdvd}</span><span class="ubadge ub-sust">SUST {n_sust}</span>
      <span class="ubadge ub-dev">DEV 3</span><span class="ubadge ub-com">COMERCIAL {n_com}</span>
      <span style="color:#374151;font-size:16px;margin:0 4px">|</span>
      <span style="font-size:9px;color:#93c5fd;font-weight:700">{n_urg_tot} chamados</span>
    </div></div>
  <div class="u-sec" style="background:#14532d;color:#bbf7d0;margin-top:0">🟢 PDV — Urgente <span class="u-cnt">{n_pdv} chamados</span></div>
  <div class="u-wrap up-bg"><table><thead><tr><th class="up-th">Chamado</th><th class="up-th">Abertura</th><th class="up-th">Dias</th><th class="up-th">Cliente</th><th class="up-th">Descrição</th><th class="up-th">Responsável</th><th class="up-th">Status</th></tr></thead><tbody>{pdv_rows}</tbody></table></div>
  <div class="u-sec" style="background:#7f1d1d;color:#fecaca">🔴 ERP — Urgente <span class="u-cnt">{n_erp} chamados</span></div>
  <div class="u-wrap ua-bg"><table><thead><tr><th class="ua-th">Chamado</th><th class="ua-th">Abertura</th><th class="ua-th">Dias</th><th class="ua-th">Cliente</th><th class="ua-th">Descrição</th><th class="ua-th">Responsável</th><th class="ua-th">Status</th></tr></thead><tbody>{erp_rows}</tbody></table></div>
  <div class="u-sec" style="background:#1d4ed8;color:#fff">📋 Todos em Alta <span class="u-cnt">{n_alta} chamados</span></div>
  <div class="u-wrap ue-bg"><table><thead><tr><th class="ue-th">Chamado</th><th class="ue-th">Abertura</th><th class="ue-th">Dias</th><th class="ue-th">Cliente</th><th class="ue-th">Descrição</th><th class="ue-th">Responsável</th><th class="ue-th">Status</th></tr></thead><tbody>{alta_rows}</tbody></table></div>
  <div class="u-sec" style="background:#7c3aed;color:#fff">💻 Dev / Sustentação <span class="u-cnt">3 chamados</span></div>
  <div class="u-wrap ud-bg"><table><thead><tr><th class="ud-th">Chamado</th><th class="ud-th">Abertura</th><th class="ud-th">Dias</th><th class="ud-th">Cliente</th><th class="ud-th">Descrição</th><th class="ud-th">Responsável</th><th class="ud-th">Status</th></tr></thead><tbody>{dev_rows}</tbody></table></div>
  <div class="u-sec" style="background:#1e293b;color:#94a3b8">🔩 Engenharia Software <span class="u-cnt">{n_eng} chamados</span></div>
  <div class="u-wrap uen-bg"><table><thead><tr><th class="uen-th">Chamado</th><th class="uen-th">Abertura</th><th class="uen-th">Dias</th><th class="uen-th">Cliente</th><th class="uen-th">Descrição</th><th class="uen-th">Responsável</th><th class="uen-th">Status</th></tr></thead><tbody>{eng_rows}</tbody></table></div>
  <div class="u-sec" style="background:#0d3a2e;color:#5eead4">🖥️ Desenvolvimento PDV <span class="u-cnt">{n_pdvd} chamados</span></div>
  <div class="u-wrap udp-bg"><table><thead><tr><th class="udp-th">Chamado</th><th class="udp-th">Abertura</th><th class="udp-th">Dias</th><th class="udp-th">Cliente</th><th class="udp-th">Descrição</th><th class="udp-th">Responsável</th><th class="udp-th">Status</th></tr></thead><tbody>{pdvd_rows}</tbody></table></div>
  <div class="u-sec" style="background:#312e81;color:#c7d2fe">🛠️ Sustentação Desenv. <span class="u-cnt">{n_sust} chamados</span></div>
  <div class="u-wrap ust-bg"><table><thead><tr><th class="ust-th">Chamado</th><th class="ust-th">Abertura</th><th class="ust-th">Dias</th><th class="ust-th">Cliente</th><th class="ust-th">Descrição</th><th class="ust-th">Responsável</th><th class="ust-th">Status</th></tr></thead><tbody>{sust_rows}</tbody></table></div>
  <div class="u-sec" style="background:#92400e;color:#fde68a">🤝 Negociação Comercial <span class="u-cnt">{n_com} chamados</span></div>
  <div class="u-wrap uc-bg"><table><thead><tr><th class="uc-th">Chamado</th><th class="uc-th">Abertura</th><th class="uc-th">Dias</th><th class="uc-th">Cliente</th><th class="uc-th">Descrição</th><th class="uc-th">Responsável</th><th class="uc-th">Status</th></tr></thead><tbody>{com_rows}</tbody></table></div>
</div>

<div id="view-res">
  <div style="background:#020f02;border:1px solid #166534;border-radius:8px;padding:10px 16px;margin-bottom:10px">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
      <div><div style="color:#4ade80;font-size:14px;font-weight:900">📊 Resultados — {today_str}</div>
      <div style="color:#16a34a;font-size:9px;margin-top:2px">Atualização automática a cada 30 minutos</div></div>
      <div style="display:flex;gap:6px;flex-wrap:wrap">
        <div style="background:#0a2a0a;border:2px solid #22c55e;border-radius:6px;padding:6px 16px;text-align:center">
          <div style="color:#4ade80;font-size:24px;font-weight:900">{n_hoje}</div>
          <div style="color:#22c55e;font-size:7px;font-weight:700">📥 ENTRARAM HOJE</div>
          {'<div style="color:#f87171;font-size:8px;font-weight:700;margin-top:2px">⚠ '+str(n_hoje_inc)+' incidente'+'s'*(n_hoje_inc!=1)+'</div>' if n_hoje_inc else ''}
        </div>
        <div style="background:#0a0a16;border:2px solid #1d4ed8;border-radius:6px;padding:6px 16px;text-align:center">
          <div style="color:#93c5fd;font-size:24px;font-weight:900">{tot}</div>
          <div style="color:#3b82f6;font-size:7px;font-weight:700">BASE TOTAL ABERTA</div>
        </div>
        <div style="background:{'#0a2a0a' if n_resol else '#080808'};border:2px {'solid #22c55e' if n_resol else 'dashed #374151'};border-radius:6px;padding:6px 16px;text-align:center">
          <div style="color:{'#4ade80' if n_resol else '#4b5563'};font-size:24px;font-weight:900">{n_resol if n_resol else '—'}</div>
          <div style="color:{'#22c55e' if n_resol else '#374151'};font-size:7px;font-weight:700">📤 RESOLVIDOS HOJE</div>
        </div>
      </div></div></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
    <div style="background:#0a0a0a;border:1px solid #1e293b;border-radius:6px;padding:10px 14px">
      <div style="color:#64748b;font-size:8px;font-weight:700;letter-spacing:1px;margin-bottom:10px">DISTRIBUIÇÃO POR STATUS</div>
      <div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#86efac;font-size:9px;font-weight:700">🟢 Novo</span><span style="color:#4ade80;font-weight:900">{n_nov}</span></div>{_bar(n_nov,tot,'#22c55e')}</div>
      <div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#93c5fd;font-size:9px;font-weight:700">🔵 Em Andamento</span><span style="color:#60a5fa;font-weight:900">{n_and}</span></div>{_bar(n_and,tot,'#3b82f6')}</div>
      <div><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#fde68a;font-size:9px;font-weight:700">🟡 Aguardando</span><span style="color:#fbbf24;font-weight:900">{n_agu}</span></div>{_bar(n_agu,tot,'#d97706')}</div>
    </div>
    <div style="background:#0a0a0a;border:1px solid #1e293b;border-radius:6px;padding:10px 14px">
      <div style="color:#64748b;font-size:8px;font-weight:700;letter-spacing:1px;margin-bottom:10px">DISTRIBUIÇÃO POR TIPO</div>
      <div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#fca5a5;font-size:9px;font-weight:700">🔴 Incidente</span><span style="color:#f87171;font-weight:900">{n_inc}</span></div>{_bar(n_inc,tot,'#ef4444')}</div>
      <div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#93c5fd;font-size:9px;font-weight:700">🔵 Requisição</span><span style="color:#60a5fa;font-weight:900">{n_req}</span></div>{_bar(n_req,tot,'#3b82f6')}</div>
      <div><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="color:#ddd6fe;font-size:9px;font-weight:700">🟣 Dúvida/Outros</span><span style="color:#a78bfa;font-weight:900">{n_duv+tot-n_inc-n_req-n_duv}</span></div>{_bar(n_duv+tot-n_inc-n_req-n_duv,tot,'#7c3aed')}</div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
    <div style="background:#0a0a0a;border:1px solid #1e293b;border-radius:6px;padding:10px 14px">
      <div style="color:#64748b;font-size:8px;font-weight:700;letter-spacing:1px;margin-bottom:10px">CLIENTES — VOLUME (TOP 10)</div>{cli_bars}</div>
    <div style="background:#0a0a0a;border:1px solid #1e293b;border-radius:6px;padding:10px 14px">
      <div style="color:#64748b;font-size:8px;font-weight:700;letter-spacing:1px;margin-bottom:6px">RESPONSÁVEIS — CARGA</div>
      <div style="display:flex;gap:10px;margin-bottom:8px"><span style="color:#ea580c;font-size:7.5px;font-weight:700">● Sul</span><span style="color:#7c3aed;font-size:7.5px;font-weight:700">● Logus</span></div>{resp_bars}</div>
  </div>
  {'<div style="background:#020f02;border:1px solid #166534;border-radius:6px;overflow:hidden;margin-bottom:10px"><div style="background:#14532d;padding:6px 14px;display:flex;justify-content:space-between;align-items:center"><span style="color:#bbf7d0;font-size:11px;font-weight:900">📥 Entraram Hoje</span><span style="color:#4ade80;font-size:10px;font-weight:700">'+str(n_hoje)+' chamado'+"s"*(n_hoje!=1)+'</span></div><table style="width:100%;border-collapse:collapse"><thead><tr style="background:#060606;border-bottom:1px solid #1f2937"><th style="color:#22c55e;font-size:7.5px;padding:4px 8px;text-align:left">TICKET</th><th style="color:#64748b;font-size:7.5px;padding:4px 8px;text-align:left">CLIENTE</th><th style="color:#64748b;font-size:7.5px;padding:4px 8px;text-align:left">TIPO</th><th style="color:#64748b;font-size:7.5px;padding:4px 9px;text-align:left">ASSUNTO</th><th style="color:#64748b;font-size:7.5px;padding:4px 9px;text-align:left">RESPONSÁVEL</th><th style="color:#64748b;font-size:7.5px;padding:4px 8px;text-align:left">STATUS</th></tr></thead><tbody>'+hoje_rows+'</tbody></table></div>' if n_hoje else ''}
  {'<div style="background:#020a02;border:1px solid #166534;border-radius:6px;overflow:hidden;margin-bottom:10px"><div style="background:#14532d;padding:6px 14px;display:flex;justify-content:space-between;align-items:center"><span style="color:#bbf7d0;font-size:11px;font-weight:900">📤 Resolvidos Hoje</span><span style="color:#4ade80;font-size:10px;font-weight:700">'+str(n_resol)+' chamado'+"s"*(n_resol!=1)+'</span></div><table style="width:100%;border-collapse:collapse"><thead><tr style="background:#060606;border-bottom:1px solid #1f2937"><th style="color:#22c55e;font-size:7.5px;padding:4px 8px;text-align:left">TICKET</th><th style="color:#64748b;font-size:7.5px;padding:4px 8px;text-align:left">CLIENTE</th><th style="color:#64748b;font-size:7.5px;padding:4px 8px;text-align:left">TIPO</th><th style="color:#64748b;font-size:7.5px;padding:4px 9px;text-align:left">ASSUNTO</th><th style="color:#64748b;font-size:7.5px;padding:4px 9px;text-align:left">RESPONSÁVEL</th><th style="color:#64748b;font-size:7.5px;padding:4px 8px;text-align:left">RESOLUÇÃO</th></tr></thead><tbody>'+baixados_rows+'</tbody></table></div>' if n_resol else ''}
  <div style="background:#080808;border:1px solid #1e293b;border-radius:6px;padding:10px 14px">
    <div style="color:#475569;font-size:8.5px;font-weight:700;margin-bottom:6px">📈 SALDO DO DIA — {today_str}</div>
    <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">
      <div style="color:#4ade80;font-size:13px;font-weight:900">📥 +{n_hoje} entradas</div>
      <div style="color:#475569;font-size:13px">—</div>
      <div style="color:{'#f87171' if n_resol else '#4b5563'};font-size:13px;font-weight:900">📤 -{n_resol} saídas</div>
      <div style="color:#475569;font-size:13px">{'>' if n_hoje>n_resol else '<' if n_hoje<n_resol else '='}</div>
      <div style="color:{'#fbbf24' if n_hoje!=n_resol else '#4ade80'};font-size:16px;font-weight:900">
        {'+' if n_hoje>=n_resol else ''}{n_hoje-n_resol} {'acumulando' if n_hoje>n_resol else 'reduzindo' if n_resol>n_hoje else 'neutro'}
      </div>
      <div style="color:#1f2937;font-size:8px;margin-left:auto">🔄 atualiza a cada 30min automaticamente</div>
    </div></div>
</div>

<div style="text-align:center;color:#1a1a2a;font-size:8px;padding:10px;border-top:1px solid #0a0a1a;margin-top:8px">
  Logus Sul BI · {today_str} · {tot} chamados · {len(clientes)} clientes · {tot_cust} customizações
</div>
</body></html>'''
