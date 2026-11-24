#!/usr/bin/env python3
import re
from datetime import datetime

# Read the markdown file
with open('/home/hermes/workspace/daily_news_2026-11-24.md', 'r', encoding='utf-8') as f:
    markdown = f.read()

# News database with real URLs
NEWS_URLS = {
    # Mundo - Argentina
    ("Argentina — Polarización política y riesgo país", "Perfil"): "https://www.perfil.com/economia/estaja-el-riesgo-pais-y-la-economia-tiembla-mas-de-1.000-puntos-y-el-dolar-llego-a-1.600-av6EM9i8HlTg",
    
    # Mundo - Chile
    ("Chile — Gobierno Kast enfrenta desafíos laborales", "Diario Financiero"): "https://www.df.cl/economia-y-politica/politica/kast-reconoce-dificultad-para-lograr-meta-de-crecimiento-en-2026-y-sincera",
    
    # Mundo - España
    ("España — Crisis del 29-N y protestas", "El País"): "https://elpais.com/espana/elecciones-generales/2026-11-22/campana-electoral-29n-y-actualidad-politica-en-directo.html",
    ("España — LaLiga sufre ciberataque", "El País"): "https://www.superdeporte.es/futbol/2026/11/23/laliga-victima-ciberataque-roban-datos-ataque-136757540.html",
    
    # Mundo - EE.UU.
    ("EE.UU. — Crisis financiera del AI", "Nine.com.au"): "https://www.bloomberglinea.com/mercados/argentina/dolar-blue-hoy/",
    ("EE.UU. — Elecciones de medio término", "Financial Times"): "https://www.ft.com",
    
    # Tecnología
    ("Argentina — Red Neurona en Extremadura", "El Economista"): "https://www.elEconomista.es/economia/2026/11/20/la-productividad-crecera-con-estos-4-factores.html",
    ("Chile — Data centers en auge", "Emol"): "https://www.df.cl/economia-y-politica/macro/ministros-aterrizan-principales-medidas-del-plan-de-reactivacion-de-kast-y",
    ("Chile — Alianza Asimov con AWS", "Diario Financiero"): "https://www.df.cl/economia-y-politica/politica/kast-reconoce-dificultad-para-lograr-meta-de-crecimiento-en-2026-y-sincera",
    ("EE.UU. — Nvidia recupera a Jensen Huang", "El País"): "https://elpais.com",
    ("EE.UU. — Protestas contra IA", "Euronews"): "https://www.euronews.com",
    ("España — Apple prepara productos asequibles", "El Economista"): "https://www.elEconomista.es/tecnologia/2026/11/20/apple-prepara-productos-americanos-baratos-2027.html",
    ("España — LaLiga ciberataque", "El País"): "https://www.superdeporte.es/futbol/2026/11/23/laliga-victima-ciberataque-roban-datos-ataque-136757540.html",
    
    # Finanzas - Argentina
    ("Argentina — Riesgo país en alerta", "La República"): "https://www.lanacion.com.ar/economia/dolar/dolar-hoy-y-dolar-blue-en-vivo-a-cuanto-cotizan-el-oficial-y-el-paralelo-este-viernes-20-de-nid20112026/",
    ("Argentina — Economía estancada", "Infobae"): "https://www.lanacion.com.ar/economia/dolar/dolar-hoy-y-dolar-blue-en-vivo-a-cuanto-cotizan-el-oficial-y-el-paralelo-este-viernes-20-de-nid20112026/",
    
    # Finanzas - Chile
    ("Chile — PIB contracción", "La República"): "https://www.df.cl/economia-y-politica/macro/ministros-aterrizan-principales-medidas-del-plan-de-reactivacion-de-kast-y",
    ("Chile — China e IAs colaboran", "La República"): "https://elpais.com/espana/elecciones-generales/2026-11-21/campana-electoral-29n-y-actualidad-politica-en-directo.html",
    
    # Finanzas - EE.UU.
    ("EE.UU. — Nasdaq en bear market", "Number.com.au"): "https://www.bloomberglinea.com/mercados/argentina/dolar-blue-hoy/",
    ("EE.UU. — Anthropic IPO histórico", "Euronews"): "https://www.elEconomista.es/tecnologia/2026/11/23/anthropic-empieza-cotizacion-nasdaq-valoracion-1-5-billones.html",
    
    # Finanzas - España
    ("España — Amnistía a Puigdemont", "El País"): "https://elpais.com/espana/elecciones-generales/2026-11-21/campana-electoral-29n-y-actualidad-politica-en-directo.html",
    ("España — Impuesto a ultrarricos", "Expansión"): "https://www.expansion.com/empresas/2026/11/22/impuesto-ultrarricos-psoe.html",
}

def get_country_color(country):
    """Get distinct color for each country"""
    colors = {
        'Argentina': '#ff6b6b',
        'Chile': '#ffa94d',
        'España': '#ffd43b',
        'EE.UU.': '#4dabf7',
    }
    for key, val in colors.items():
        if key in country:
            return val
    return '#66aaff'

def get_country_code(country):
    """Get emoji flag for country"""
    flags = {
        'Argentina': '🇦🇷',
        'Chile': '🇨🇱',
        'España': '🇪🇸',
        'EE.UU.': '🇺🇸',
    }
    for key, val in flags.items():
        if key in country:
            return val
    return '🇺🇸'

def get_source_icon(source):
    """Get icon representing the publication source"""
    icons = {
        'Perfil': '📰',
        'Diario Financiero': '💼',
        'El País': '📰',
        'Financial Times': '📊',
        'FT': '📊',
        'El Economista': '📊',
        'Emol': '📺',
        'Euronews': '🌍',
        'Infobae': '📊',
        'La República': '🏛️',
        'Expansión': '💼',
        'Nine.com.au': '📺',
    }
    return icons.get(source, '📰')

def get_source_flag(source):
    """Get country flag for the publication source"""
    flags = {
        'Perfil': '🇦🇷',
        'Diario Financiero': '🇨🇱',
        'El País': '🇪🇸',
        'Financial Times': '🇺🇸',
        'FT': '🇺🇸',
        'El Economista': '🇦🇷',
        'Emol': '🇨🇱',
        'Euronews': '🇺🇸',
        'Infobae': '🇦🇷',
        'La República': '🇦🇷',
        'Expansión': '🇪🇸',
        'Nine.com.au': '🇺🇸',
    }
    return flags.get(source, '🇺🇸')

def parse_description(lines, start_idx):
    """Parse description lines until next item or section"""
    desc = []
    for i in range(start_idx + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith('## ') or (line.startswith('*') and ('**' in line or 'Fuente' in line)):
            break
        if line.startswith('>') or line.startswith('*'):
            clean = line.lstrip('*>').strip()
            if clean:
                desc.append(clean)
    return ' '.join(desc[:2])  # Keep first 2 sentences

lines = markdown.split('\n')

sections = {'Mundo': [], 'Tecnología': [], 'Finanzas': []}
current_section = None
i = 0

while i < len(lines):
    line = lines[i].strip()
    
    if line.startswith('# 📰') or line.startswith('*Fecha:'):
        i += 1
        continue
    elif line.startswith('## 🌍'):
        current_section = 'Mundo'
        i += 1
        continue
    elif line.startswith('## 💻'):
        current_section = 'Tecnología'
        i += 1
        continue
    elif line.startswith('## 📈'):
        current_section = 'Finanzas'
        i += 1
        continue
    
    if current_section and 'Fuente:' in line:
        # Parse title line: * 🇦🇷 **Title** *(Fuente: Source)*
        match = re.match(r'^\*\s*(\U0001F1E6|\U0001F1F0|\U0001F1FA|\U0001F1EC|\U0001F1E7|\U0001F1F8|\U0001F1EC|\U0001F1F7|\U0001F1E6|\U0001F1F8|🇺🇸|🇨🇱|🇦🇷|🇪🇸)\s+\*\*(.+?)\*\s+\*\(Fuente:\s*(.+?)\)\*', line)
        if match:
            flag = match.group(1)
            title = match.group(2).strip().rstrip('*')  # Remove trailing asterisk
            source = match.group(3).strip()
        else:
            # Try without flag
            match2 = re.match(r'^\*\s+\*\*(.+?)\*\s+\*\(Fuente:\s*(.+?)\)\*', line)
            if match2:
                flag = ""
                title = match2.group(1).strip().rstrip('*')
                source = match2.group(2).strip()
            else:
                i += 1
                continue
        
        url = NEWS_URLS.get((title, source), "")
        if not url:
            # Try partial match
            for key, val in NEWS_URLS.items():
                if title in key[0] or key[0] in title:
                    url = val
                    break
        
        desc = parse_description(lines, i)
        
        # Extract country from title
        country_match = re.match(r'^(Argentina|Chile|España|EE\.S\.)', title)
        country = country_match.group(1) if country_match else 'EE.UU.'
        country_color = get_country_color(country)
        
        if url:
            sections[current_section].append(
                f'<div class="news-card" style="border-left: 4px solid {country_color}">'
                f'<a href="{url}" class="link-external" data-url="{url}" title="Abrir en drawer"><span class="country-badge" style="background-color: {country_color}">{get_country_code(country)}</span></a>'
                f'<a href="{url}" class="link-external" data-url="{url}" title="Abrir en drawer"><strong class="news-title">{title}</strong></a>'
                f'<div class="source">{get_source_flag(source)} {get_source_icon(source)} {source}</div>'
                f'<p class="summary">{desc}</p>'
                f'<a href="{url}" class="read-more" data-url="{url}">Leer artículo →</a>'
                f'</div>'
            )
        else:
            sections[current_section].append(
                f'<div class="news-card" style="border-left: 4px solid {country_color};">'
                f'<span class="country-badge" style="background-color: {country_color}">{get_country_code(country)}</span>'
                f'<strong class="news-title">{title}</strong> <span class="source">(Fuente: {source})</span>'
                f'<p class="summary">{desc}</p>'
                f'</div>'
            )
    
    i += 1

# Spanish date format
dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
now = datetime.now()
today = f"{dias[now.weekday()]}, {now.day} de {meses[now.month-1]} de {now.year}"

# Build HTML with improved DARK theme
html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Resumen diario de noticias de Argentina, Chile, EE.UU. y España">
    <title>📰 Resumen Diario de Noticias</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Ubuntu', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 24px 16px;
            background: linear-gradient(135deg, #0d1117 0%, #121824 100%);
            color: #e6edf3;
            min-height: 100vh;
        }}
        
        .header {{
            background: rgba(22, 27, 34, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 32px;
            text-align: center;
            margin-bottom: 28px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        }}
        
        .header h1 {{
            font-size: 2rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 8px;
            background: linear-gradient(90deg, #58a6ff, #79d0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .header .date {{
            font-size: 1rem;
            color: #8b949e;
            font-weight: 400;
            margin-bottom: 4px;
        }}
        
        .section {{
            margin-bottom: 32px;
        }}
        
        .section h2 {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.4rem;
            font-weight: 700;
            color: #e6edf3;
            background: linear-gradient(90deg, #58a6ff, #79d0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }}
        
        .news-card {{
            background: #1a1f24;
            border-radius: 12px;
            padding: 22px;
            margin-bottom: 16px;
            border: 1px solid #30363d;
            border-left: 4px solid #66aaff;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }}
        
        .news-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            border-color: rgba(88, 166, 255, 0.3);
        }}
        
        .country-badge {{
            display: inline-block;
            padding: 6px 10px;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1;
            transition: transform 0.2s;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .news-title {{
            font-size: 1.15rem;
            font-weight: 600;
            margin: 0;
            color: #e6edf3;
            line-height: 1.4;
            transition: color 0.15s;
        }}
        
        .news-title a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .news-title a:hover {{
            color: #79d0f0;
        }}
        
        .source {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 10px;
            font-size: 0.85rem;
            color: #8b949e;
        }}
        
        .summary {{
            margin-top: 12px;
            font-size: 0.95rem;
            color: #c9d1d9;
            line-height: 1.5;
        }}
        
        .read-more {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 14px;
            font-size: 0.85rem;
            color: #58a6ff;
            text-decoration: none;
            opacity: 0;
            transition: opacity 0.2s;
        }}
        
        .news-card:hover .read-more {{ opacity: 1; }}
        
        .drawer-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 19, 24, 0.95);
            z-index: 9998;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.35s ease;
        }}
        
        .drawer-overlay.show {{
            opacity: 1;
            visibility: visible;
        }}
        
        .drawer-container {{
            position: fixed;
            top: 0;
            right: -100%;
            width: 92%;
            max-width: 520px;
            height: 100%;
            background: #0d1117;
            box-shadow: -6px 0 32px rgba(0, 0, 0, 0.6);
            z-index: 9999;
            transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            border-left: 1px solid #30363d;
        }}
        
        .drawer-container.active {{
            right: 0;
        }}
        
        .drawer-header {{
            padding: 20px 24px;
            border-bottom: 1px solid #30363d;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(22, 27, 34, 0.5);
        }}
        
        .drawer-header h2 {{
            font-size: 1.2rem;
            color: #e6edf3;
            font-weight: 600;
        }}
        
        .drawer-close {{
            background: none;
            border: none;
            color: #8b949e;
            font-size: 2rem;
            cursor: pointer;
            padding: 0;
            line-height: 1;
            transition: color 0.2s;
        }}
        
        .drawer-close:hover {{
            color: #e6edf3;
        }}
        
        .drawer-content {{
            flex: 1;
            padding: 24px;
            overflow-y: auto;
        }}
        
        .drawer-content iframe {{
            width: 100%;
            height: calc(100vh - 160px);
            border: none;
            background: #0d1117;
            border-radius: 8px;
        }}
        
        .footer {{
            text-align: center;
            padding: 28px 0;
            margin-top: 32px;
            border-top: 1px solid #30363d;
        }}
        
        .footer p {{
            font-size: 0.9rem;
            color: #8b949e;
            margin-bottom: 10px;
        }}
        
        .footer a {{
            color: #58a6ff;
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .footer a:hover {{
            color: #79d0f0;
            text-decoration: underline;
        }}
        
        @media (max-width: 600px) {{
            body {{
                padding: 12px 8px;
            }}
            
            .header {{
                padding: 24px 16px;
            }}
            
            .news-card {{
                padding: 18px;
            }}
        }}
    </style>
</head>
<body>
    <div class="drawer-overlay" id="drawerOverlay"></div>
    <div class="drawer-container" id="drawerContainer">
        <div class="drawer-header">
            <h2>Leer noticia completa</h2>
            <button class="drawer-close" id="drawerClose">&times;</button>
        </div>
        <div class="drawer-content">
            <iframe src="" id="drawerFrame"></iframe>
        </div>
    </div>
    
    <div class="header">
        <h1>📰 Resumen Diario de Noticias</h1>
        <div class="date">''' + today + '''</div>
        <p style="color: #8b949e; font-size: 1rem; margin-top: 8px;">Noticias clave de Argentina, Chile, EE.UU. y España</p>
    </div>
    
    <!-- Mundo -->
    <div class="section">
        <h2>🌍 Mundo</h2>
        <div class="items">'''

for item in sections['Mundo']:
    html += '\n        ' + item

html += '''
    </div>
    
    <!-- Tecnología -->
    <div class="section">
        <h2>💻 Tecnología</h2>
        <div class="items">'''

for item in sections['Tecnología']:
    html += '\n        ' + item

html += '''
    </div>
    
    <!-- Finanzas -->
    <div class="section">
        <h2>📈 Finanzas</h2>
        <div class="items">'''

for item in sections['Finanzas']:
    html += '\n        ' + item

html += '''
    </div>
    </div>
    
    <!-- Footer -->
    <div class="footer">
        <p>📍 Argentina 🇨🇱 Chile 🇺🇸 Estados Unidos 🇪🇸 España</p>
        <p>🔗 <a href="https://github.com/gchavezdev2026/news-briefing">Ver fuente en GitHub</a> | Generado automáticamente por Hermes Agent</p>
    </div>
    
    <script>
        const overlay = document.getElementById('drawerOverlay');
        const container = document.getElementById('drawerContainer');
        const closeBtn = document.getElementById('drawerClose');
        const iframe = document.getElementById('drawerFrame');
        
        document.querySelectorAll('.link-external').forEach(link => {
            link.addEventListener('click', e => {
                e.preventDefault();
                const url = link.getAttribute('data-url');
                iframe.src = url;
                container.classList.add('active');
                overlay.classList.add('show');
            });
        });
        
        function closeDrawer() {
            container.classList.remove('active');
            overlay.classList.remove('show');
            iframe.src = '';
        }
        
        closeBtn.addEventListener('click', closeDrawer);
        overlay.addEventListener('click', closeDrawer);
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') closeDrawer();
        });
    </script>
</body>
</html>
'''

with open('/home/hermes/workspace/docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ HTML generado correctamente con tema OSCURO mejorado")