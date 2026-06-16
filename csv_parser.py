import csv, io
from datetime import date, datetime

def _parse_date(s):
    if not s:
        return '', 0
    s = s.strip().split(' ')[0]
    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y'):
        try:
            d = datetime.strptime(s, fmt).date()
            return d.strftime('%d/%m/%Y'), (date.today() - d).days
        except ValueError:
            continue
    return s, 0

def _detect_dialect(text):
    sample = text[:8192]
    try:
        return csv.Sniffer().sniff(sample, delimiters=',;\t|')
    except csv.Error:
        # fallback: conta qual delimitador aparece mais na primeira linha
        first = sample.split('\n')[0]
        if first.count(';') > first.count(','):
            return csv.excel_tab.__class__  # não usar — vai por abaixo
        return csv.excel

def parse_csv(content_bytes):
    for enc in ('utf-8-sig', 'latin-1', 'cp1252'):
        try:
            text = content_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = content_bytes.decode('utf-8', errors='replace')

    # detecta delimitador pela primeira linha
    first_line = text.split('\n')[0]
    delimiter = ';' if first_line.count(';') >= first_line.count(',') else ','

    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    hdr = {}
    tickets = []
    for r in reader:
        if not r:
            continue
        if not hdr:
            hdr = {v.strip(): i for i, v in enumerate(r)}
            continue
        g = lambda col, fb: r[hdr[col]].strip() if col in hdr and hdr[col] < len(r) else (r[fb].strip() if len(r) > fb else '')
        dt, dias = _parse_date(g('Data e hora de abertura', 12))
        res_raw  = g('Data e hora da resolução', 16)
        res_dt, _= _parse_date(res_raw.split(' ')[0]) if res_raw else ('', 0)
        tickets.append({
            'code':     r[0].strip(),
            'produto':  g('Produto', 1),
            'status':   g('Status', 2),
            'tipo':     g('Tipo', 3) if 'Tipo' in hdr else '',
            'empresa':  g('Empresa', 7) or 'SEM EMPRESA',
            'grupo':    g('Grupo', 8),
            'atrib':    g('Atribuído', 9) or '— Sem Responsável —',
            'assunto':  g('Assunto', 11),
            'data':     dt,
            'dias':     max(dias, 0),
            'ordem':    g('Ordem - Logus Sul', 22) if 'Ordem - Logus Sul' in hdr else g('Ordem - Logus Sul', 23),
            'resolucao': res_dt,
        })
    return [t for t in tickets if t['code'].isdigit()]

def parse_csv_baixados(content_bytes):
    tickets = parse_csv(content_bytes)
    today_str = date.today().strftime('%d/%m/%Y')
    return [t for t in tickets if t['resolucao'] == today_str]
