#!/usr/bin/env python3
"""
Generate HTML page for PGL Major Singapore 2026 Stage 2 predictions
Format matches index.html (Budapest Major Stage 3) style.
Uses the seeded simulation, so numbers match predict_singapore_s2.py exactly.
"""

import os

from prediction_algorithm_singapore_s2 import SingaporeS2Predictor
from team_data_singapore_s2 import TEAMS_DATA_SINGAPORE_S2, ROUND_1_MATCHUPS_SINGAPORE_S2, INITIAL_SEEDING_SINGAPORE_S2


def prob_class(value):
    if value >= 15:
        return "prob-high"
    elif value >= 5:
        return "prob-medium"
    return "prob-low"


def heat(value, kind):
    """Inline style for a heat-map cell: jade for advancing records, red for eliminations."""
    rgb = "53, 224, 200" if kind == "adv" else "239, 51, 64"
    alpha = min(0.62, value / 100 * 1.15)
    color = "var(--text)" if value >= 5 else "var(--text-muted)"
    return f"background: rgba({rgb}, {alpha:.3f}); color: {color};"


def hero_logo_html():
    """Optional official logo: drop a file at assets/singapore_major_logo.png to show it."""
    path = "assets/singapore_major_logo.png"
    if os.path.exists(path):
        return f'<img class="hero-logo" src="{path}" alt="PGL Major Singapore 2026">'
    return SG_EMBLEM_SVG


SG_EMBLEM_SVG = """<svg class="hero-emblem" viewBox="0 0 100 80" aria-hidden="true">
                <defs>
                    <mask id="crescent"><rect width="100" height="80" fill="black"/><circle cx="34" cy="40" r="28" fill="white"/><circle cx="45" cy="40" r="25" fill="black"/></mask>
                    <polygon id="sgstar" points="0,-10 2.9,-3.1 9.5,-3.1 3.8,1.2 5.9,8.1 0,4 -5.9,8.1 -3.8,1.2 -9.5,-3.1 -2.9,-3.1"/>
                </defs>
                <rect width="100" height="80" fill="white" mask="url(#crescent)"/>
                <g fill="white">
                    <use href="#sgstar" transform="translate(60,23) scale(0.6)"/>
                    <use href="#sgstar" transform="translate(76,35) scale(0.6)"/>
                    <use href="#sgstar" transform="translate(70,53) scale(0.6)"/>
                    <use href="#sgstar" transform="translate(50,53) scale(0.6)"/>
                    <use href="#sgstar" transform="translate(44,35) scale(0.6)"/>
                </g>
            </svg>"""

SKYLINE_SVG = """<svg class="hero-skyline" viewBox="0 0 1440 240" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
            <!-- back layer: CBD towers -->
            <g fill="#3B0D1C" opacity="0.9">
                <rect x="0" y="150" width="70" height="90"/><rect x="60" y="110" width="46" height="130"/><rect x="112" y="135" width="60" height="105"/>
                <rect x="180" y="95" width="40" height="145"/><rect x="226" y="125" width="54" height="115"/>
                <rect x="470" y="140" width="50" height="100"/><rect x="820" y="130" width="44" height="110"/>
                <rect x="1085" y="70" width="44" height="170"/><rect x="1135" y="100" width="52" height="140"/><rect x="1192" y="55" width="40" height="185"/>
                <rect x="1238" y="90" width="56" height="150"/><rect x="1300" y="120" width="48" height="120"/><rect x="1352" y="80" width="42" height="160"/><rect x="1398" y="130" width="42" height="110"/>
                <polygon points="1192,55 1212,25 1232,55"/><polygon points="180,95 200,70 220,95"/>
            </g>
            <!-- front layer -->
            <g fill="#0B0A12">
                <!-- Supertrees -->
                <path d="M300 240 L308 150 Q270 138 262 112 Q312 128 316 128 Q320 128 370 112 Q362 138 324 150 L332 240 Z"/>
                <path d="M372 240 L378 178 Q350 170 344 150 Q380 162 384 162 Q388 162 424 150 Q418 170 390 178 L396 240 Z"/>
                <path d="M222 240 L228 186 Q204 178 198 162 Q230 172 234 172 Q238 172 270 162 Q264 178 240 186 L246 240 Z"/>
                <!-- ArtScience lotus -->
                <path d="M470 240 Q462 200 446 186 Q474 190 484 214 Q482 180 472 162 Q502 176 506 212 Q512 176 530 160 Q534 188 524 216 Q538 194 562 188 Q550 206 546 240 Z"/>
                <!-- Marina Bay Sands -->
                <path d="M598 240 L610 92 L654 92 L650 240 Z"/>
                <path d="M686 240 L690 92 L734 92 L738 240 Z"/>
                <path d="M774 240 L770 92 L814 92 L826 240 Z"/>
                <path d="M574 92 Q590 74 620 72 L820 72 Q856 74 880 60 Q868 88 836 92 Z"/>
                <!-- Singapore Flyer -->
                <rect x="1006" y="150" width="8" height="90"/>
                <path d="M960 240 L1008 150 L1012 150 L1060 240 L1050 240 L1010 166 L970 240 Z"/>
                <!-- low buildings + waterfront -->
                <rect x="0" y="196" width="210" height="44"/><rect x="408" y="206" width="60" height="34"/>
                <rect x="860" y="200" width="90" height="40"/><rect x="1068" y="186" width="372" height="54"/>
                <rect x="0" y="226" width="1440" height="14"/>
            </g>
            <g fill="none" stroke="#0B0A12">
                <circle cx="1010" cy="112" r="62" stroke-width="7"/>
                <g stroke-width="1.6">
                    <line x1="948" y1="112" x2="1072" y2="112"/><line x1="1010" y1="50" x2="1010" y2="174"/>
                    <line x1="966" y1="68" x2="1054" y2="156"/><line x1="966" y1="156" x2="1054" y2="68"/>
                    <line x1="953" y1="88" x2="1067" y2="136"/><line x1="953" y1="136" x2="1067" y2="88"/>
                    <line x1="986" y1="55" x2="1034" y2="169"/><line x1="986" y1="169" x2="1034" y2="55"/>
                </g>
            </g>
            <!-- lights -->
            <g fill="#FFB84D" opacity="0.85">
                <circle cx="316" cy="126" r="2.2"/><circle cx="384" cy="160" r="1.8"/><circle cx="234" cy="170" r="1.8"/>
                <rect x="620" y="110" width="3" height="5"/><rect x="634" y="140" width="3" height="5"/><rect x="702" y="120" width="3" height="5"/>
                <rect x="716" y="160" width="3" height="5"/><rect x="786" y="112" width="3" height="5"/><rect x="798" y="150" width="3" height="5"/>
                <rect x="626" y="180" width="3" height="5"/><rect x="706" y="196" width="3" height="5"/><rect x="792" y="190" width="3" height="5"/>
            </g>
            <g fill="#E056A0" opacity="0.9">
                <circle cx="268" cy="114" r="2"/><circle cx="364" cy="114" r="2"/><circle cx="348" cy="152" r="1.6"/><circle cx="420" cy="152" r="1.6"/>
                <circle cx="202" cy="164" r="1.6"/><circle cx="266" cy="164" r="1.6"/>
            </g>
        </svg>"""


def generate_html():
    predictor = SingaporeS2Predictor()
    results = predictor.simulate_swiss_stage(simulations=10000, first_round_matchups=ROUND_1_MATCHUPS_SINGAPORE_S2)
    predictions = predictor.get_top_predictions(results)
    rankings = predictor.get_strength_rankings()

    advancement_probs = []
    for team in results:
        total_advance = results[team]['3-0'] + results[team]['3-1'] + results[team]['3-2']
        total_elim = results[team]['2-3'] + results[team]['1-3'] + results[team]['0-3']
        advancement_probs.append((team, total_advance, total_elim, results[team]))
    advancement_probs.sort(key=lambda x: x[1], reverse=True)

    top_team = advancement_probs[0]
    picks = predictor.get_optimal_picks(results)
    top_3_0 = picks['3-0']
    top_0_3 = picks['0-3']
    advancing_picks = picks['advance']

    top8 = advancement_probs[:8]

    def chips(items):
        return "".join(
            f'<span class="hp-chip"><span class="hp-team">{t}</span><span class="hp-pct">{v:.0f}%</span></span>'
            for t, v in items)

    hero_picks_html = f"""<div class="hero-picks">
                <div class="hp-col hp-30">
                    <div class="hp-label">3-0</div>
                    <div class="hp-chips">{chips(top_3_0)}</div>
                </div>
                <div class="hp-col hp-adv">
                    <div class="hp-label">Avançam (3-1 / 3-2)</div>
                    <div class="hp-chips">{chips(advancing_picks)}</div>
                </div>
                <div class="hp-col hp-03">
                    <div class="hp-label">0-3</div>
                    <div class="hp-chips">{chips(top_0_3)}</div>
                </div>
            </div>"""
    hero_logo = hero_logo_html()

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PGL Major Singapore 2026 - Stage 2 Predictions | Data-Driven Analysis</title>
    <meta name="description" content="Análise científica e predições baseadas em dados para o Stage 2 do PGL Major Singapore 2026 usando 10.000 simulações Monte Carlo">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            /* Singapore palette: flag red + white, gold, Gardens-by-the-Bay jade, orchid */
            --primary: #EF3340;
            --secondary: #FFB84D;
            --dark: #0B0A12;
            --dark-lighter: #17151F;
            --accent: #35E0C8;
            --orchid: #E056A0;
            --success: #3DDC97;
            --warning: #FFB84D;
            --danger: #FF5468;
            --text: #F1EEF0;
            --text-muted: #A39FAB;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background: var(--dark);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }}

        h1, h2, h3 {{
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}

        .hero {{
            background: linear-gradient(135deg, #0A0E27 0%, #1A1F3A 50%, #2A1F3A 100%);
            padding: 80px 20px 60px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(circle at 20% 50%, rgba(255, 70, 85, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(0, 217, 255, 0.1) 0%, transparent 50%);
            pointer-events: none;
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .hero-badge {{
            display: inline-block;
            background: rgba(255, 70, 85, 0.1);
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .hero h1 {{
            font-size: clamp(2.5rem, 5vw, 4rem);
            margin-bottom: 20px;
            background: linear-gradient(135deg, #FF4655 0%, #FFA726 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .hero-subtitle {{
            font-size: clamp(1.1rem, 2vw, 1.4rem);
            color: var(--text-muted);
            margin-bottom: 40px;
        }}

        .hero-stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 40px;
        }}

        .hero-stat {{ text-align: center; }}

        .hero-stat-value {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--accent);
            display: block;
        }}

        .hero-stat-label {{
            font-size: 0.9rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        .section {{
            padding: 80px 20px;
            position: relative;
        }}

        .section-header {{
            text-align: center;
            margin-bottom: 60px;
        }}

        .section-number {{
            display: inline-block;
            width: 40px; height: 40px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 50%;
            line-height: 40px;
            text-align: center;
            font-weight: 700;
            margin-bottom: 15px;
        }}

        .section-title {{
            font-size: clamp(2rem, 4vw, 3rem);
            margin-bottom: 15px;
        }}

        .section-description {{
            font-size: 1.1rem;
            color: var(--text-muted);
            max-width: 700px;
            margin: 0 auto;
        }}

        .methodology-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }}

        .method-card {{
            background: var(--dark-lighter);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 30px;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .method-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(255, 70, 85, 0.2);
        }}

        .method-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }}

        .method-icon {{ font-size: 2.5rem; margin-bottom: 20px; }}

        .method-title {{
            font-size: 1.4rem;
            margin-bottom: 15px;
            color: var(--accent);
        }}

        .method-weight {{
            display: inline-block;
            background: rgba(255, 70, 85, 0.1);
            color: var(--primary);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 15px;
        }}

        .method-description {{ color: var(--text-muted); line-height: 1.7; }}

        .swiss-explainer {{
            background: var(--dark-lighter);
            border-radius: 20px;
            padding: 50px;
            margin: 40px 0;
            border: 1px solid rgba(0, 217, 255, 0.2);
        }}

        .swiss-title {{
            font-size: 2rem;
            margin-bottom: 30px;
            color: var(--accent);
            text-align: center;
        }}

        .swiss-steps {{ display: grid; gap: 20px; }}

        .swiss-step {{
            display: flex;
            align-items: start;
            gap: 20px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            border-left: 3px solid var(--accent);
        }}

        .swiss-step-number {{
            flex-shrink: 0;
            width: 35px; height: 35px;
            background: var(--accent);
            color: var(--dark);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
        }}

        .swiss-step-content h4 {{ margin-bottom: 8px; color: var(--text); }}
        .swiss-step-content p {{ color: var(--text-muted); font-size: 0.95rem; }}

        .seeding-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 15px;
            margin: 40px 0;
        }}

        .seed-card {{
            background: var(--dark-lighter);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px 15px;
            text-align: center;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .seed-card:hover {{
            transform: scale(1.05);
            border-color: var(--primary);
        }}

        .seed-number {{ font-size: 0.9rem; color: var(--text-muted); margin-bottom: 10px; }}
        .seed-team {{ font-weight: 700; font-size: 1.1rem; color: var(--text); }}
        .seed-meta {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 4px; }}

        .results-container {{ display: grid; gap: 40px; margin-top: 40px; }}

        .result-category {{
            background: var(--dark-lighter);
            border-radius: 20px;
            padding: 40px;
            border: 2px solid rgba(255, 255, 255, 0.05);
        }}

        .result-category-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 30px;
        }}

        .result-icon {{ font-size: 2.5rem; }}
        .result-category-title {{ font-size: 2rem; flex: 1; }}
        .result-category-subtitle {{ color: var(--text-muted); font-size: 0.95rem; }}

        .predictions-list {{ display: grid; gap: 20px; }}

        .prediction-card {{
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            padding: 25px;
            display: flex;
            align-items: center;
            gap: 25px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}

        .prediction-card:hover {{
            transform: translateX(5px);
            border-color: var(--primary);
        }}

        .prediction-rank {{
            font-size: 2rem;
            font-weight: 800;
            color: var(--text-muted);
            min-width: 50px;
        }}

        .prediction-team-info {{ flex: 1; }}

        .prediction-team-name {{
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .prediction-team-details {{ font-size: 0.9rem; color: var(--text-muted); }}

        .prediction-probability {{ text-align: right; }}

        .prediction-percentage {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            display: block;
        }}

        .prediction-label {{
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .confidence-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 5px;
        }}

        .confidence-high {{
            background: rgba(0, 230, 118, 0.1);
            color: var(--success);
            border: 1px solid var(--success);
        }}

        .confidence-medium {{
            background: rgba(255, 193, 7, 0.1);
            color: var(--warning);
            border: 1px solid var(--warning);
        }}

        .prob-explainer {{
            background: var(--dark-lighter);
            border-radius: 20px;
            padding: 50px;
            margin: 40px 0;
            border: 1px solid rgba(255, 167, 38, 0.2);
        }}

        .prob-comparison {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }}

        .prob-card {{
            background: rgba(255, 255, 255, 0.02);
            border-radius: 16px;
            padding: 30px;
            border: 2px solid rgba(255, 255, 255, 0.05);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }}

        .prob-card:hover {{
            transform: translateY(-5px);
            border-color: var(--secondary);
        }}

        .prob-card-header {{ text-align: center; margin-bottom: 25px; }}
        .prob-card-icon {{ font-size: 3rem; margin-bottom: 15px; }}
        .prob-card-title {{ font-size: 1.5rem; color: var(--secondary); margin-bottom: 10px; }}
        .prob-card-subtitle {{ font-size: 0.9rem; color: var(--text-muted); }}

        .prob-breakdown {{ margin: 20px 0; }}

        .prob-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 3px solid var(--primary);
        }}

        .prob-item-label {{ font-weight: 600; }}

        .prob-item-value {{
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--accent);
        }}

        .prob-total {{
            margin-top: 20px;
            padding: 20px;
            background: linear-gradient(135deg, rgba(255, 70, 85, 0.1), rgba(255, 167, 38, 0.1));
            border-radius: 12px;
            border: 2px solid var(--secondary);
            text-align: center;
        }}

        .prob-total-label {{
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .prob-total-value {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--secondary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .prob-formula {{
            background: rgba(0, 217, 255, 0.05);
            border: 1px dashed var(--accent);
            border-radius: 12px;
            padding: 20px;
            margin: 30px 0;
            text-align: center;
        }}

        .prob-formula-text {{
            font-family: 'Courier New', monospace;
            font-size: 1.2rem;
            color: var(--accent);
            font-weight: 600;
        }}

        .insight-box {{
            background: linear-gradient(135deg, rgba(255, 167, 38, 0.1), rgba(255, 70, 85, 0.1));
            border-left: 4px solid var(--secondary);
            border-radius: 12px;
            padding: 25px;
            margin: 30px 0;
        }}

        .insight-box-title {{
            font-size: 1.3rem;
            color: var(--secondary);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .insight-box-content {{ color: var(--text); line-height: 1.8; }}

        .insight-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .insight-item {{
            background: rgba(255, 255, 255, 0.02);
            border-radius: 8px;
            padding: 15px;
        }}

        .insight-item-title {{ font-weight: 700; color: var(--accent); margin-bottom: 8px; }}
        .insight-item-desc {{ font-size: 0.9rem; color: var(--text-muted); }}

        .prob-summary-table {{
            background: var(--dark-lighter);
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
            overflow-x: auto;
        }}

        .prob-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }}

        .prob-table thead {{ background: rgba(255, 70, 85, 0.1); }}

        .prob-table th {{
            padding: 15px 12px;
            text-align: left;
            font-weight: 700;
            color: var(--accent);
            border-bottom: 2px solid var(--primary);
            white-space: nowrap;
        }}

        .prob-table th:first-child {{ border-top-left-radius: 12px; }}
        .prob-table th:last-child {{ border-top-right-radius: 12px; }}

        .prob-table tbody tr {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            transition: background 0.2s ease;
        }}

        .prob-table tbody tr:hover {{ background: rgba(255, 70, 85, 0.05); }}

        .prob-table td {{ padding: 15px 12px; color: var(--text); }}
        .prob-table .team-name {{ font-weight: 700; color: var(--text); }}
        .prob-table .prob-cell {{ text-align: center; font-weight: 600; }}
        .prob-table .prob-high {{ color: var(--success); }}
        .prob-table .prob-medium {{ color: var(--secondary); }}
        .prob-table .prob-low {{ color: var(--text-muted); }}

        .prob-table .total-advance {{
            background: rgba(0, 230, 118, 0.1);
            border-left: 3px solid var(--success);
            font-weight: 700;
            color: var(--success);
        }}

        .prob-table .total-eliminated {{
            background: rgba(255, 23, 68, 0.1);
            border-left: 3px solid var(--danger);
            font-weight: 700;
            color: var(--danger);
        }}

        .chart-container {{
            background: var(--dark-lighter);
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .chart-title {{
            font-size: 1.5rem;
            margin-bottom: 30px;
            text-align: center;
            color: var(--accent);
        }}

        .chart-wrapper {{ position: relative; height: 400px; }}

        .final-picks {{
            background: linear-gradient(135deg, rgba(255, 70, 85, 0.1) 0%, rgba(255, 167, 38, 0.1) 100%);
            border: 2px solid var(--primary);
            border-radius: 20px;
            padding: 50px;
            margin: 60px 0;
        }}

        .final-picks-title {{
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 40px;
            color: var(--primary);
        }}

        .picks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}

        .pick-category {{
            background: var(--dark-lighter);
            border-radius: 16px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .pick-category-title {{
            font-size: 1.3rem;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .pick-list {{ list-style: none; }}

        .pick-item {{
            padding: 15px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 8px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .pick-team {{ font-weight: 700; font-size: 1.1rem; }}
        .pick-prob {{ color: var(--accent); font-weight: 600; }}

        .footer {{
            background: var(--dark-lighter);
            padding: 40px 20px;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .footer-content {{ max-width: 1200px; margin: 0 auto; }}
        .footer p {{ color: var(--text-muted); margin-bottom: 15px; }}

        .footer-warning {{
            background: rgba(255, 193, 7, 0.1);
            border: 1px solid var(--warning);
            border-radius: 12px;
            padding: 20px;
            margin: 20px auto;
            max-width: 800px;
            color: var(--warning);
            font-size: 0.9rem;
        }}

        .author-section {{
            background: linear-gradient(135deg, rgba(255, 70, 85, 0.05) 0%, rgba(0, 217, 255, 0.05) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 30px;
            margin: 30px auto;
            max-width: 800px;
            text-align: center;
        }}

        .author-title {{ font-size: 1.2rem; color: var(--accent); margin-bottom: 15px; font-weight: 600; }}
        .author-name {{ font-size: 1.5rem; color: var(--primary); font-weight: 700; margin-bottom: 5px; }}
        .author-title-text {{ font-size: 1.1rem; color: var(--text); margin-bottom: 20px; font-style: italic; }}

        .author-links {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 20px;
        }}

        .author-link {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text);
            text-decoration: none;
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .author-link:hover {{
            background: rgba(255, 70, 85, 0.2);
            border-color: var(--primary);
            transform: translateY(-2px);
        }}

        .author-link-icon {{ font-size: 1.2rem; }}

        .scroll-progress {{
            position: fixed;
            top: 0; left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
            z-index: 9999;
            transition: width 0.1s ease;
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .animate-in {{ animation: fadeInUp 0.6s ease-out forwards; }}

        @media (max-width: 768px) {{
            .hero {{ padding: 60px 20px 40px; }}
            .section {{ padding: 60px 20px; }}
            .swiss-explainer, .final-picks {{ padding: 30px 20px; }}
            .result-category {{ padding: 25px 20px; }}
            .prediction-card {{ flex-direction: column; text-align: center; }}
            .prediction-probability {{ text-align: center; }}
            .author-section {{ padding: 20px; }}
            .author-links {{ flex-direction: column; gap: 15px; }}
            .author-link {{ width: 100%; justify-content: center; }}
        }}

        /* ============ Singapore theme ============ */
        body {{
            background:
                radial-gradient(circle at 1px 1px, rgba(255, 255, 255, 0.035) 1px, transparent 0) 0 0 / 28px 28px,
                var(--dark);
        }}

        .flag-band {{
            height: 6px;
            background: linear-gradient(180deg, var(--primary) 0 50%, #FFFFFF 50% 100%);
        }}

        .hero {{
            background: linear-gradient(180deg, #12060D 0%, #2B0A19 38%, #6E1228 70%, #C8283C 92%, #F0623F 100%);
            padding: 56px 20px 270px;
        }}

        .hero::before {{
            background:
                radial-gradient(circle at 50% 100%, rgba(255, 184, 77, 0.35) 0%, transparent 45%),
                radial-gradient(circle at 12% 18%, rgba(224, 86, 160, 0.18) 0%, transparent 40%),
                radial-gradient(circle at 88% 12%, rgba(53, 224, 200, 0.10) 0%, transparent 40%);
        }}

        .hero-skyline {{
            position: absolute;
            left: 0; right: 0; bottom: -1px;
            width: 100%;
            height: 240px;
            display: block;
        }}

        .hero-emblem {{ width: 84px; height: 68px; margin-bottom: 10px; filter: drop-shadow(0 0 18px rgba(255, 255, 255, 0.35)); }}
        .hero-logo {{ max-height: 150px; max-width: 80%; margin-bottom: 16px; }}

        .hero-eyebrow {{
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            letter-spacing: 6px;
            text-transform: uppercase;
            color: var(--secondary);
            font-size: 1rem;
            margin-bottom: 6px;
        }}

        .hero h1 {{
            background: none;
            -webkit-text-fill-color: currentColor;
            color: #FFFFFF;
            margin-bottom: 18px;
            line-height: 1;
        }}

        .h1-city {{
            display: block;
            font-size: clamp(3rem, 9vw, 6.5rem);
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 6px 40px rgba(239, 51, 64, 0.65);
        }}

        .h1-stage {{
            display: block;
            margin-top: 10px;
            font-size: clamp(1.2rem, 2.6vw, 2rem);
            letter-spacing: 3px;
            text-transform: uppercase;
            background: linear-gradient(90deg, var(--secondary), #FFFFFF 50%, var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-subtitle {{ color: rgba(255, 255, 255, 0.78); max-width: 760px; margin: 0 auto 26px; font-size: clamp(1rem, 1.6vw, 1.15rem); }}

        .hero-meta {{ display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 34px; }}
        .hero-meta span {{
            background: rgba(11, 10, 18, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(6px);
            padding: 7px 16px;
            border-radius: 999px;
            font-size: 0.88rem;
            font-weight: 600;
        }}

        .hero-cta {{
            display: inline-block; margin-top: 26px; padding: 12px 26px; border-radius: 999px;
            background: var(--primary); color: #fff; font-weight: 700; text-decoration: none;
            box-shadow: 0 8px 24px rgba(239, 51, 64, 0.35); transition: transform 0.15s;
        }}
        .hero-cta:hover {{ transform: translateY(-2px); }}

        .hero-picks-title {{
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 4px;
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.75);
            margin-bottom: 12px;
        }}

        .hero-picks {{
            display: grid;
            grid-template-columns: 1fr 2.2fr 1fr;
            gap: 14px;
            max-width: 1080px;
            margin: 0 auto;
            text-align: left;
        }}

        .hp-col {{
            background: rgba(11, 10, 18, 0.62);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-top: 3px solid var(--hp-color);
            border-radius: 14px;
            padding: 16px;
            backdrop-filter: blur(10px);
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.35);
        }}

        .hp-30 {{ --hp-color: var(--secondary); }}
        .hp-adv {{ --hp-color: var(--accent); }}
        .hp-03 {{ --hp-color: var(--primary); }}

        .hp-label {{
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: var(--hp-color);
            margin-bottom: 10px;
        }}

        .hp-chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}

        .hp-chip {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 0.92rem;
        }}

        .hp-team {{ font-weight: 700; color: #FFFFFF; }}
        .hp-pct {{ font-weight: 700; font-size: 0.8rem; color: var(--hp-color); }}

        /* sections */
        .section-number {{
            background: linear-gradient(135deg, var(--primary), var(--orchid));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .section-title {{ text-transform: uppercase; letter-spacing: 2px; }}
        .section-header::after {{
            content: '';
            display: block;
            width: 72px;
            height: 4px;
            margin: 18px auto 0;
            border-radius: 2px;
            background: linear-gradient(90deg, var(--primary) 0 50%, #FFFFFF 50% 100%);
        }}

        .method-card, .seed-card, .prob-card, .pick-category, .result-category,
        .swiss-explainer, .prob-explainer, .chart-container, .prob-summary-table {{
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.045), rgba(255, 255, 255, 0.015));
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .method-card {{ border-top: 3px solid var(--primary); }}
        .method-card:nth-child(2) {{ border-top-color: var(--secondary); }}
        .method-card:nth-child(3) {{ border-top-color: var(--orchid); }}
        .method-card:nth-child(4) {{ border-top-color: var(--accent); }}
        .method-card:nth-child(5) {{ border-top-color: #FFFFFF; }}
        .method-weight {{ background: rgba(239, 51, 64, 0.14); color: #FF8A93; }}

        .seeding-grid {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
        @media (max-width: 760px) {{ .seeding-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
        .seed-card {{ text-align: left; border-left: 3px solid var(--primary); padding: 16px 18px; }}
        .seed-card:nth-child(n+9) {{ border-left-color: var(--accent); }}
        .seed-number {{ font-family: 'Rajdhani', sans-serif; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px; }}

        /* table as heat map */
        .prob-table thead {{ background: transparent; }}
        .prob-table th {{ color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; border-bottom: 2px solid var(--primary); }}
        .prob-table td {{ padding: 11px 12px; }}
        .prob-table td.prob-cell {{ border: 2px solid var(--dark-lighter); border-radius: 8px; font-variant-numeric: tabular-nums; }}
        .prob-table .team-name {{ white-space: nowrap; }}
        .prob-table .total-advance, .prob-table .total-eliminated {{ border-left-width: 3px; }}
        .prob-table tbody tr:hover {{ background: rgba(255, 255, 255, 0.04); }}

        /* final picks */
        .final-picks {{
            background: linear-gradient(135deg, rgba(239, 51, 64, 0.16), rgba(224, 86, 160, 0.08) 50%, rgba(53, 224, 200, 0.10));
            border: 1px solid rgba(239, 51, 64, 0.45);
        }}
        .picks-grid {{ grid-template-columns: 1fr 1fr; }}
        .picks-grid .pick-category:nth-child(1) {{ border-top: 3px solid var(--secondary); }}
        .picks-grid .pick-category:nth-child(2) {{ border-top: 3px solid var(--primary); }}
        .picks-grid .pick-category:nth-child(3) {{ border-top: 3px solid var(--accent); }}
        .picks-grid .pick-category:nth-child(1) .pick-prob {{ color: var(--secondary); }}
        .picks-grid .pick-category:nth-child(2) .pick-prob {{ color: #FF8A93; }}

        .scroll-progress {{ background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent)); }}
        .footer {{ border-top: 4px solid var(--primary); }}

        @media (max-width: 768px) {{
            .hero {{ padding: 40px 16px 200px; }}
            .hero-skyline {{ height: 170px; }}
            .hero-picks {{ grid-template-columns: 1fr; }}
            .picks-grid {{ grid-template-columns: 1fr; }}
            .hero-eyebrow {{ letter-spacing: 3px; }}
        }}
    </style>
</head>
<body>
    <div class="scroll-progress" id="scrollProgress"></div>

    <!-- Hero Section -->
    <div class="flag-band"></div>
    <section class="hero">
        <div class="hero-content">
            {hero_logo}
            <div class="hero-eyebrow">PGL Major &middot; Counter-Strike 2</div>
            <h1><span class="h1-city">Singapore 2026</span><span class="h1-stage">Stage 2 &middot; Pick'em Predictions</span></h1>
            <p class="hero-subtitle">Predições baseadas em dados: Valve Global Standing, forma recente (incluindo o Stage 1), preços de mercado e 10.000 simulações Monte Carlo do sistema Swiss</p>

            <div class="hero-meta">
                <span>📍 Singapura</span>
                <span>🗓️ 28 Nov &ndash; 1 Dez 2026</span>
                <span>⚔️ Swiss &middot; 16 times &middot; Top 8 avançam</span>
                <span>🎲 10.000 simulações</span>
            </div>

            <div class="hero-picks-title">Seu Pick'em em um olhar</div>
            {hero_picks_html}
            <a class="hero-cta" href="bolao.html">🏆 Entrar no bolão com os amigos</a>
        </div>
        {SKYLINE_SVG}
    </section>

    <!-- Methodology Section -->
    <section class="section">
        <div class="container">
            <div class="section-header">
                <div class="section-number">01</div>
                <h2 class="section-title">Metodologia</h2>
                <p class="section-description">
                    Sistema de predição multifatorial com análise estatística avançada
                </p>
            </div>

            <div class="methodology-grid">
                <div class="method-card">
                    <div class="method-icon">📊</div>
                    <h3 class="method-title">Valve Global Standing</h3>
                    <span class="method-weight">35% do peso</span>
                    <p class="method-description">
                        Pontos do Valve Global Standing (VGS) de 2/nov/2026 - o ranking oficial usado para convidar e seedar o Major. Escala tipo Elo, mais informativa que a posição. Os resultados do Stage 1 ainda não entraram nele; eles pesam na forma e no momentum.
                    </p>
                </div>

                <div class="method-card">
                    <div class="method-icon">🔥</div>
                    <h3 class="method-title">Forma Recente</h3>
                    <span class="method-weight">30% do peso</span>
                    <p class="method-description">
                        Resultados dos últimos 3 meses ponderados pela qualidade do adversário (séries contra top 50), para não premiar farm regional que já infla o VGS.
                    </p>
                </div>

                <div class="method-card">
                    <div class="method-icon">🎯</div>
                    <h3 class="method-title">Momentum</h3>
                    <span class="method-weight">20% do peso</span>
                    <p class="method-description">
                        Avaliação qualitativa da tendência do time: títulos recentes, sequências de vitórias/derrotas, trocas de lineup, stand-ins e tempo sem jogar.
                    </p>
                </div>

                <div class="method-card">
                    <div class="method-icon">📈</div>
                    <h3 class="method-title">Consistência</h3>
                    <span class="method-weight">15% do peso</span>
                    <p class="method-description">
                        Histórico de estabilidade e confiabilidade do time, medindo variância de performance ao longo do tempo.
                    </p>
                </div>

                <div class="method-card">
                    <div class="method-icon">💰</div>
                    <h3 class="method-title">Mercado (Polymarket)</h3>
                    <span class="method-weight">50% da força final</span>
                    <p class="method-description">
                        Os quatro fatores acima formam o modelo de dados (metade da força final). Para este stage nenhuma casa publicou odds de classificação ao Stage 3, então a outra metade vem dos preços da rodada 1 no Polymarket: em cada confronto, a diferença de força é ajustada para reproduzir a chance que o mercado dá. Os poucos preços de classificação que existem servem de comparação: o modelo final é mais otimista que o mercado com a FUT e menos com NAVI e G2.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Probability Explanation Section -->
    <section class="section" style="background: rgba(255, 255, 255, 0.01);">
        <div class="container">
            <div class="section-header">
                <div class="section-number">02</div>
                <h2 class="section-title">Como Interpretar os Percentuais</h2>
                <p class="section-description">
                    Por que a chance de avançar é maior que a chance de fazer 3-0?
                </p>
            </div>

            <div class="prob-explainer">
                <div class="prob-formula">
                    <p style="color: var(--text-muted); margin-bottom: 15px; font-size: 1.1rem;">Fórmula da Probabilidade de Avançar:</p>
                    <div class="prob-formula-text">
                        P(Avançar) = P(3-0) + P(3-1) + P(3-2)
                    </div>
                </div>

                <div class="prob-comparison">
                    <div class="prob-card">
                        <div class="prob-card-header">
                            <div class="prob-card-icon">🎯</div>
                            <h3 class="prob-card-title">3-0 Específico</h3>
                            <p class="prob-card-subtitle">Uma forma de vencer</p>
                        </div>
                        <div class="prob-breakdown">
                            <div class="prob-item" style="border-left-color: var(--primary);">
                                <span class="prob-item-label">🏆 3-0 (Perfeito)</span>
                                <span class="prob-item-value">{top_team[3]['3-0']:.2f}%</span>
                            </div>
                        </div>
                        <div class="prob-total" style="background: rgba(255, 70, 85, 0.1); border-color: var(--primary);">
                            <div class="prob-total-label">Total</div>
                            <div class="prob-total-value" style="background: linear-gradient(135deg, var(--primary), var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{top_team[3]['3-0']:.2f}%</div>
                        </div>
                        <p style="margin-top: 20px; color: var(--text-muted); text-align: center; font-size: 0.9rem;">
                            <strong>High Risk, High Reward</strong><br>
                            O time precisa vencer EXATAMENTE 3-0
                        </p>
                    </div>

                    <div class="prob-card">
                        <div class="prob-card-header">
                            <div class="prob-card-icon">✅</div>
                            <h3 class="prob-card-title">Avançar (Qualquer)</h3>
                            <p class="prob-card-subtitle">Três formas de vencer</p>
                        </div>
                        <div class="prob-breakdown">
                            <div class="prob-item" style="border-left-color: var(--primary);">
                                <span class="prob-item-label">🏆 3-0</span>
                                <span class="prob-item-value">{top_team[3]['3-0']:.2f}%</span>
                            </div>
                            <div class="prob-item" style="border-left-color: var(--secondary);">
                                <span class="prob-item-label">⚡ 3-1</span>
                                <span class="prob-item-value">{top_team[3]['3-1']:.2f}%</span>
                            </div>
                            <div class="prob-item" style="border-left-color: var(--accent);">
                                <span class="prob-item-label">🎮 3-2</span>
                                <span class="prob-item-value">{top_team[3]['3-2']:.2f}%</span>
                            </div>
                        </div>
                        <div class="prob-total">
                            <div class="prob-total-label">Total</div>
                            <div class="prob-total-value">{top_team[1]:.2f}%</div>
                        </div>
                        <p style="margin-top: 20px; color: var(--text-muted); text-align: center; font-size: 0.9rem;">
                            <strong>Safe Pick</strong><br>
                            O time só precisa conseguir 3 vitórias
                        </p>
                    </div>
                </div>

                <div class="insight-box">
                    <h4 class="insight-box-title">
                        <span>💡</span> Por que isso acontece?
                    </h4>
                    <div class="insight-box-content">
                        <p style="margin-bottom: 15px;">
                            Quando você escolhe um time para <strong style="color: var(--primary);">3-0</strong>, está apostando que ele fará um desempenho <strong>perfeito</strong>.
                            Qualquer derrota elimina a possibilidade.
                        </p>
                        <p style="margin-bottom: 15px;">
                            Quando você escolhe um time para <strong style="color: var(--success);">avançar</strong>, está apostando que ele conseguirá
                            <strong>3 vitórias antes de 3 derrotas</strong>. Não importa o caminho: 3-0, 3-1 ou 3-2 - todas contam!
                        </p>
                        <p style="color: var(--accent); font-weight: 600;">
                            Por isso {top_team[0]} tem {top_team[3]['3-0']:.2f}% de fazer 3-0, mas {top_team[1]:.2f}% de avançar (somando 3-0 + 3-1 + 3-2).
                        </p>
                    </div>
                </div>

                <div class="insight-box" style="background: linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(0, 230, 118, 0.1)); border-left-color: var(--accent);">
                    <h4 class="insight-box-title" style="color: var(--accent);">
                        <span>🎲</span> Estratégia para Pick'ems
                    </h4>
                    <div class="insight-grid">
                        <div class="insight-item">
                            <div class="insight-item-title">Pick 3-0</div>
                            <div class="insight-item-desc">
                                Escolha times top tier com matchups favoráveis pelo seeding. É arriscado, mas vale mais pontos!
                            </div>
                        </div>
                        <div class="insight-item">
                            <div class="insight-item-title">Pick 0-3</div>
                            <div class="insight-item-desc">
                                Escolha os times mais fracos. Mais fácil acertar que 3-0, pois times ruins tendem a perder consistentemente.
                            </div>
                        </div>
                        <div class="insight-item">
                            <div class="insight-item-title">Picks de Avançar</div>
                            <div class="insight-item-desc">
                                Só pontua se o time avançar com 3-1 ou 3-2 (um 3-0 NÃO conta). Por isso ordenamos por P(3-1) + P(3-2), e não pela chance total de avançar.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Swiss System Section -->
    <section class="section">
        <div class="container">
            <div class="section-header">
                <div class="section-number">03</div>
                <h2 class="section-title">Sistema Swiss</h2>
                <p class="section-description">
                    Entenda como funciona o formato de competição utilizado no Major
                </p>
            </div>

            <div class="swiss-explainer">
                <h3 class="swiss-title">Como Funciona o Swiss System</h3>
                <div class="swiss-steps">
                    <div class="swiss-step">
                        <div class="swiss-step-number">1</div>
                        <div class="swiss-step-content">
                            <h4>Seeding Inicial</h4>
                            <p>Seeds 1 a 8: os convidados, pelo Valve Global Standing (VGS) de 2/nov/2026. Seeds 9 a 16: os classificados do Stage 1, pela colocação final. Rodada 1: seed 1 vs 9, 2 vs 10 ... 8 vs 16</p>
                        </div>
                    </div>
                    <div class="swiss-step">
                        <div class="swiss-step-number">2</div>
                        <div class="swiss-step-content">
                            <h4>Confrontos por Record</h4>
                            <p>Times com mesmo número de vitórias e derrotas jogam entre si (1-0 vs 1-0, 0-1 vs 0-1)</p>
                        </div>
                    </div>
                    <div class="swiss-step">
                        <div class="swiss-step-number">3</div>
                        <div class="swiss-step-content">
                            <h4>Emparelhamento por Buchholz</h4>
                            <p>Dentro de cada grupo de record os times são reordenados pelo Buchholz (saldo de vitórias-derrotas dos adversários já enfrentados) e depois pelo seed inicial. Rodadas 2-3: maior seed vs menor seed sem repetir confronto; rodadas 4-5: tabela de prioridade oficial da Valve. O simulador segue exatamente essas regras.</p>
                        </div>
                    </div>
                    <div class="swiss-step">
                        <div class="swiss-step-number">4</div>
                        <div class="swiss-step-content">
                            <h4>Classificação e Eliminação</h4>
                            <p>Times com 3 vitórias avançam para Stage 3, times com 3 derrotas são eliminados. BO1 normal, BO3 em jogos de avanço/eliminação (simulados como série de 3 mapas).</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Monte Carlo Explanation Section -->
    <section class="section" style="background: rgba(255, 255, 255, 0.01);">
        <div class="container">
            <div class="section-header">
                <div class="section-number">04</div>
                <h2 class="section-title">Simulações Monte Carlo</h2>
                <p class="section-description">
                    Como geramos probabilidades confiáveis através de milhares de simulações
                </p>
            </div>

            <div class="swiss-explainer" style="border-color: rgba(0, 217, 255, 0.3);">
                <div style="text-align: center; margin-bottom: 40px;">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🎲</div>
                    <h3 class="swiss-title" style="color: var(--accent);">O que é Monte Carlo?</h3>
                    <p style="color: var(--text); font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
                        Monte Carlo é um método estatístico que usa <strong style="color: var(--accent);">aleatoriedade repetida</strong>
                        para calcular probabilidades de eventos complexos. Em vez de tentar calcular matematicamente todas as possibilidades,
                        nós <strong>simulamos o torneio milhares de vezes</strong> e contamos os resultados.
                    </p>
                </div>

                <div class="insight-box" style="background: rgba(0, 217, 255, 0.05); border-left-color: var(--accent);">
                    <h4 class="insight-box-title" style="color: var(--accent);">
                        <span>💡</span> Como Funciona na Prática
                    </h4>
                    <div class="insight-box-content">
                        <div style="display: grid; gap: 20px;">
                            <div style="display: flex; gap: 15px; align-items: start;">
                                <div style="background: var(--accent); color: var(--dark); width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;">1</div>
                                <div>
                                    <strong style="color: var(--text);">Simular uma vez:</strong> O algoritmo simula TODO o Stage 2, rodada por rodada, usando as probabilidades calculadas para cada confronto.
                                </div>
                            </div>
                            <div style="display: flex; gap: 15px; align-items: start;">
                                <div style="background: var(--accent); color: var(--dark); width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;">2</div>
                                <div>
                                    <strong style="color: var(--text);">Repetir 10.000 vezes:</strong> Cada simulação pode ter resultados diferentes devido à aleatoriedade (upsets acontecem!). Depois de 10.000 simulações, temos um retrato estatístico muito preciso.
                                </div>
                            </div>
                            <div style="display: flex; gap: 15px; align-items: start;">
                                <div style="background: var(--accent); color: var(--dark); width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;">3</div>
                                <div>
                                    <strong style="color: var(--text);">Calcular probabilidades:</strong> Se {top_team[0]} fez 3-0 em {int(top_team[3]['3-0'] * 100)} das 10.000 simulações, sua probabilidade de 3-0 é {top_team[3]['3-0']:.2f}%. Simples assim!
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin-top: 40px;">
                    <div style="background: rgba(255, 167, 38, 0.05); border: 1px solid var(--secondary); border-radius: 12px; padding: 25px;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">⚡</div>
                        <h4 style="color: var(--secondary); margin-bottom: 10px; font-size: 1.2rem;">Por que 10.000?</h4>
                        <p style="color: var(--text-muted); font-size: 0.95rem;">
                            Quanto mais simulações, mais precisas as probabilidades. 10.000 é o ponto ideal entre precisão e tempo de processamento.
                        </p>
                    </div>

                    <div style="background: rgba(0, 230, 118, 0.05); border: 1px solid var(--success); border-radius: 12px; padding: 25px;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">🎯</div>
                        <h4 style="color: var(--success); margin-bottom: 10px; font-size: 1.2rem;">Considera Upsets</h4>
                        <p style="color: var(--text-muted); font-size: 0.95rem;">
                            Times fracos podem vencer times fortes (com menor probabilidade). O Monte Carlo captura essa variância naturalmente.
                        </p>
                    </div>

                    <div style="background: rgba(0, 217, 255, 0.05); border: 1px solid var(--accent); border-radius: 12px; padding: 25px;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">🔬</div>
                        <h4 style="color: var(--accent); margin-bottom: 10px; font-size: 1.2rem;">Método Científico</h4>
                        <p style="color: var(--text-muted); font-size: 0.95rem;">
                            Usado em física, finanças, meteorologia e esports. É uma técnica comprovada para modelar sistemas complexos.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Seeding Section -->
    <section class="section">
        <div class="container">
            <div class="section-header">
                <div class="section-number">05</div>
                <h2 class="section-title">Initial Seeding</h2>
                <p class="section-description">
                    Convidados (seeds 1-8) pelo Valve Global Standing de 2/nov/2026; classificados do Stage 1 (seeds 9-16) pela colocação final
                </p>
            </div>

            <div class="seeding-grid">
"""

    for i, team in enumerate(INITIAL_SEEDING_SINGAPORE_S2, 1):
        html += f"""                <div class="seed-card">
                    <div class="seed-number">Seed #{i}</div>
                    <div class="seed-team">{team}</div>
                    <div class="seed-meta">{("Stage 1: " + TEAMS_DATA_SINGAPORE_S2[team]["s1_record"]) if TEAMS_DATA_SINGAPORE_S2[team]["s1_record"] else ("Convidado · VGS #" + str(TEAMS_DATA_SINGAPORE_S2[team]["vgs_rank"]))}</div>
                </div>
"""

    html += """            </div>
        </div>
    </section>

    <!-- Simulation Results -->
    <section class="section" style="background: rgba(255, 255, 255, 0.01);">
        <div class="container">
            <div class="section-header">
                <div class="section-number">06</div>
                <h2 class="section-title">Resultados das Simulações</h2>
                <p class="section-description">
                    10.000 simulações Monte Carlo com confrontos R1 reais e Swiss System correto
                </p>
            </div>

            <!-- Chart -->
            <div class="chart-container">
                <h3 class="chart-title">Distribuição de Probabilidades - Top 8 Times</h3>
                <div class="chart-wrapper">
                    <canvas id="probabilityChart"></canvas>
                </div>
            </div>

            <!-- Probability Summary Table -->
            <div class="prob-summary-table">
                <h3 class="chart-title">Resumo Completo de Probabilidades - Todos os Times</h3>
                <table class="prob-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>VGS</th>
                            <th class="prob-cell">3-0</th>
                            <th class="prob-cell">3-1</th>
                            <th class="prob-cell">3-2</th>
                            <th class="prob-cell total-advance">✅ Avançar</th>
                            <th class="prob-cell">2-3</th>
                            <th class="prob-cell">1-3</th>
                            <th class="prob-cell">0-3</th>
                            <th class="prob-cell total-eliminated">❌ Eliminar</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    for team, adv, elim, probs in advancement_probs:
        data = TEAMS_DATA_SINGAPORE_S2[team]
        html += f"""                        <tr>
                            <td class="team-name">{team}</td>
                            <td>#{data['vgs_rank']}</td>
                            <td class="prob-cell" style="{heat(probs['3-0'], 'adv')}">{probs['3-0']:.2f}%</td>
                            <td class="prob-cell" style="{heat(probs['3-1'], 'adv')}">{probs['3-1']:.2f}%</td>
                            <td class="prob-cell" style="{heat(probs['3-2'], 'adv')}">{probs['3-2']:.2f}%</td>
                            <td class="prob-cell total-advance">{adv:.2f}%</td>
                            <td class="prob-cell" style="{heat(probs['2-3'], 'elim')}">{probs['2-3']:.2f}%</td>
                            <td class="prob-cell" style="{heat(probs['1-3'], 'elim')}">{probs['1-3']:.2f}%</td>
                            <td class="prob-cell" style="{heat(probs['0-3'], 'elim')}">{probs['0-3']:.2f}%</td>
                            <td class="prob-cell total-eliminated">{elim:.2f}%</td>
                        </tr>
"""

    html += """                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <!-- Final Recommendations -->
    <section class="section">
        <div class="container">
            <div class="final-picks">
                <h2 class="final-picks-title">🎯 Recomendações Finais para Pick'ems</h2>
                <div class="picks-grid">
                    <div class="pick-category">
                        <h3 class="pick-category-title">
                            <span>🏆</span> 3-0 (Escolha 2)
                        </h3>
                        <ul class="pick-list">
"""

    for team, prob in top_3_0:
        html += f"""                            <li class="pick-item">
                                <span class="pick-team">{team}</span>
                                <span class="pick-prob">{prob:.2f}%</span>
                            </li>
"""

    html += """                        </ul>
                    </div>

                    <div class="pick-category">
                        <h3 class="pick-category-title">
                            <span>💀</span> 0-3 (Escolha 2)
                        </h3>
                        <ul class="pick-list">
"""

    for team, prob in top_0_3:
        html += f"""                            <li class="pick-item">
                                <span class="pick-team">{team}</span>
                                <span class="pick-prob">{prob:.2f}%</span>
                            </li>
"""

    html += """                        </ul>
                    </div>

                    <div class="pick-category" style="grid-column: 1 / -1;">
                        <h3 class="pick-category-title">
                            <span>✅</span> Avançam com 3-1 ou 3-2 (Escolha 6)
                        </h3>
                        <ul class="pick-list" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 10px;">
"""

    for team, adv in advancing_picks:
        html += f"""                            <li class="pick-item">
                                <span class="pick-team">{team}</span>
                                <span class="pick-prob">{adv:.2f}%</span>
                            </li>
"""

    html += """                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <div class="author-section">
                <div class="author-title">👨‍💻 Desenvolvido por</div>
                <div class="author-name">Fernando Augusto Schmitz</div>
                <div class="author-title-text">Cientista de Dados</div>
                <div class="author-links">
                    <a href="https://wa.me/5548999125833" target="_blank" class="author-link">
                        <span class="author-link-icon">📱</span>
                        <span>WhatsApp</span>
                    </a>
                    <a href="https://www.linkedin.com/in/feschmitz/" target="_blank" class="author-link">
                        <span class="author-link-icon">💼</span>
                        <span>LinkedIn</span>
                    </a>
                </div>
            </div>

            <div class="footer-warning">
                <strong>⚠️ Aviso Importante:</strong> Estas predições são baseadas em análise estatística e 10.000 simulações Monte Carlo. CS2 tem alta variância e upsets são comuns no formato Swiss. Considere também notícias recentes, mudanças de roster e sua própria análise antes de fazer seus Pick'ems.
            </div>
            <p><strong>Stage 2:</strong> 28 de novembro a 1º de dezembro de 2026 | Top 8 avançam para o Stage 3</p>
            <p><strong>Formato:</strong> Swiss System (BO1 normal, BO3 em jogos de avanço/eliminação)</p>
            <p style="margin-top: 20px;">📊 Análise gerada com Python | Simulações Monte Carlo | Dados: Valve Global Standings (2/nov/2026), resultados do Stage 1 (HLTV/Wikipedia), Polymarket, Strafe, Pley, Insider Gaming, Skin.Club</p>
            <p style="font-size: 0.85rem; margin-top: 15px;">© 2026 PGL Major Singapore Predictions | Boa sorte com seus Pick'ems! 🎮</p>
        </div>
    </footer>

    <script>
        // Scroll Progress Bar
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById('scrollProgress').style.width = scrolled + '%';
        });

        // Chart.js Configuration
        const ctx = document.getElementById('probabilityChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
"""

    chart_labels = [t[0] for t in top8]
    chart_3_0 = [t[3]['3-0'] for t in top8]
    chart_3_1 = [t[3]['3-1'] for t in top8]
    chart_3_2 = [t[3]['3-2'] for t in top8]

    html += f"""                labels: {chart_labels},
                datasets: [
                    {{
                        label: '3-0',
                        data: {[round(v, 2) for v in chart_3_0]},
                        backgroundColor: 'rgba(255, 184, 77, 0.9)',
                        borderColor: 'rgba(255, 184, 77, 1)',
                        borderWidth: 1
                    }},
                    {{
                        label: '3-1',
                        data: {[round(v, 2) for v in chart_3_1]},
                        backgroundColor: 'rgba(53, 224, 200, 0.85)',
                        borderColor: 'rgba(53, 224, 200, 1)',
                        borderWidth: 1
                    }},
                    {{
                        label: '3-2',
                        data: {[round(v, 2) for v in chart_3_2]},
                        backgroundColor: 'rgba(224, 86, 160, 0.85)',
                        borderColor: 'rgba(224, 86, 160, 1)',
                        borderWidth: 1
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'top',
                        labels: {{
                            color: '#E8E8E8',
                            font: {{
                                size: 14,
                                family: "'Inter', sans-serif"
                            }},
                            padding: 15
                        }}
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(26, 31, 58, 0.95)',
                        titleColor: '#E8E8E8',
                        bodyColor: '#E8E8E8',
                        borderColor: 'rgba(255, 70, 85, 0.5)',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true,
                        callbacks: {{
                            label: function(context) {{
                                return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + '%';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        stacked: true,
                        grid: {{ display: false }},
                        ticks: {{
                            color: '#9E9E9E',
                            font: {{ size: 12, family: "'Inter', sans-serif" }}
                        }}
                    }},
                    y: {{
                        stacked: true,
                        beginAtZero: true,
                        max: 100,
                        grid: {{ color: 'rgba(255, 255, 255, 0.05)' }},
                        ticks: {{
                            color: '#9E9E9E',
                            font: {{ size: 12, family: "'Inter', sans-serif" }},
                            callback: function(value) {{ return value + '%'; }}
                        }}
                    }}
                }}
            }}
        }});

        // Animate elements on scroll
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('animate-in');
                }}
            }});
        }}, observerOptions);

        document.querySelectorAll('.method-card, .prediction-card, .swiss-step').forEach(el => {{
            observer.observe(el);
        }});
    </script>
</body>
</html>
"""

    return html


if __name__ == "__main__":
    print("Generating HTML for PGL Major Singapore 2026 Stage 2...")
    html_content = generate_html()

    with open("singapore_s2.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("HTML generated successfully: singapore_s2.html")
