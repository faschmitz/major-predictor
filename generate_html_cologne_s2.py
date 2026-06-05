#!/usr/bin/env python3
"""
Generate HTML page for IEM Cologne Major 2026 Stage 2 predictions
Format matches index.html (Budapest Major Stage 2) style
"""

from prediction_algorithm_cologne_s2 import CologneS2Predictor
from team_data_cologne_s2 import TEAMS_DATA_COLOGNE_S2, ROUND_1_MATCHUPS_COLOGNE_S2, INITIAL_SEEDING_COLOGNE_S2


def prob_class(value):
    if value >= 15:
        return "prob-high"
    elif value >= 5:
        return "prob-medium"
    return "prob-low"


def generate_html():
    predictor = CologneS2Predictor()
    results = predictor.simulate_swiss_stage(simulations=10000, first_round_matchups=ROUND_1_MATCHUPS_COLOGNE_S2)
    predictions = predictor.get_top_predictions(results)
    rankings = predictor.get_strength_rankings()

    advancement_probs = []
    for team in results:
        total_advance = results[team]['3-0'] + results[team]['3-1'] + results[team]['3-2']
        total_elim = results[team]['2-3'] + results[team]['1-3'] + results[team]['0-3']
        advancement_probs.append((team, total_advance, total_elim, results[team]))
    advancement_probs.sort(key=lambda x: x[1], reverse=True)

    top_team = advancement_probs[0]
    top_3_0 = predictions['3-0'][:2]
    top_0_3 = predictions['0-3'][:2]

    top_3_0_teams = {top_3_0[0][0], top_3_0[1][0]}
    advancing_filtered = [(t, a, e, r) for t, a, e, r in advancement_probs if t not in top_3_0_teams][:6]

    top8 = advancement_probs[:8]

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IEM Cologne Major 2026 - Stage 2 Predictions | Data-Driven Analysis</title>
    <meta name="description" content="Analise cientifica e predicoes baseadas em dados para o Stage 2 do IEM Cologne Major 2026 usando 10.000 simulacoes Monte Carlo">

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
            --primary: #FF4655;
            --secondary: #FFA726;
            --dark: #0A0E27;
            --dark-lighter: #1A1F3A;
            --accent: #00D9FF;
            --success: #00E676;
            --warning: #FFC107;
            --danger: #FF1744;
            --text: #E8E8E8;
            --text-muted: #9E9E9E;
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
    </style>
</head>
<body>
    <div class="scroll-progress" id="scrollProgress"></div>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <div class="hero-badge">Analise Cientifica</div>
            <h1>IEM Cologne Major 2026<br>Stage 2 Predictions</h1>
            <p class="hero-subtitle">Predicoes baseadas em dados usando 10.000 simulacoes Monte Carlo do sistema Swiss</p>

            <div class="hero-stats">
                <div class="hero-stat">
                    <span class="hero-stat-value">10,000</span>
                    <span class="hero-stat-label">Simulacoes</span>
                </div>
                <div class="hero-stat">
                    <span class="hero-stat-value">16</span>
                    <span class="hero-stat-label">Times</span>
                </div>
                <div class="hero-stat">
                    <span class="hero-stat-value">4</span>
                    <span class="hero-stat-label">Fatores</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Methodology Section -->
    <section class="section">
        <div class="container">
            <div class="section-header">
                <div class="section-number">01</div>
                <h2 class="section-title">Metodologia</h2>
                <p class="section-description">
                    Sistema de predicao multi-fatorial com analise estatistica avancada
                </p>
            </div>

            <div class="methodology-grid">
                <div class="method-card">
                    <div class="method-icon">📊</div>
                    <h3 class="method-title">HLTV Ranking</h3>
                    <span class="method-weight">30% do peso</span>
                    <p class="method-description">
                        Rankings oficiais HLTV dos times, considerando performance historica e resultados recentes em torneios tier 1 e tier 2.
                    </p>
                </div>

                <div class="method-card">
                    <div class="method-icon">🔥</div>
                    <h3 class="method-title">Forma Recente</h3>
                    <span class="method-weight">30% do peso</span>
                    <p class="method-description">
                        Momentum e performance nas ultimas semanas, incluindo vitorias em torneios recentes e nivel de jogo demonstrado.
                    </p>
                </div>

                <div class="method-card">
                    <div class="method-icon">🎯</div>
                    <h3 class="method-title">Performance no Stage 1</h3>
                    <span class="method-weight">25% do peso</span>
                    <p class="method-description">
                        Record no Stage 1 (3-0 vale mais que 3-1, que vale mais que 3-2). Para os convidados diretos, o momentum recente e usado como substituto.
                    </p>
                </div>

                <div class="method-card">
                    <div class="method-icon">📈</div>
                    <h3 class="method-title">Consistencia</h3>
                    <span class="method-weight">15% do peso</span>
                    <p class="method-description">
                        Historico de estabilidade e confiabilidade do time, medindo variancia de performance ao longo do tempo.
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
                    Por que a chance de avancar e maior que a chance de fazer 3-0?
                </p>
            </div>

            <div class="prob-explainer">
                <div class="prob-formula">
                    <p style="color: var(--text-muted); margin-bottom: 15px; font-size: 1.1rem;">Formula da Probabilidade de Avancar:</p>
                    <div class="prob-formula-text">
                        P(Avancar) = P(3-0) + P(3-1) + P(3-2)
                    </div>
                </div>

                <div class="prob-comparison">
                    <div class="prob-card">
                        <div class="prob-card-header">
                            <div class="prob-card-icon">🎯</div>
                            <h3 class="prob-card-title">3-0 Especifico</h3>
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
                            <h3 class="prob-card-title">Avancar (Qualquer)</h3>
                            <p class="prob-card-subtitle">Tres formas de vencer</p>
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
                            O time so precisa conseguir 3 vitorias
                        </p>
                    </div>
                </div>

                <div class="insight-box">
                    <h4 class="insight-box-title">
                        <span>💡</span> Por que isso acontece?
                    </h4>
                    <div class="insight-box-content">
                        <p style="margin-bottom: 15px;">
                            Quando voce escolhe um time para <strong style="color: var(--primary);">3-0</strong>, esta apostando que ele fara um desempenho <strong>perfeito</strong>.
                            Qualquer derrota elimina a possibilidade.
                        </p>
                        <p style="margin-bottom: 15px;">
                            Quando voce escolhe um time para <strong style="color: var(--success);">avancar</strong>, esta apostando que ele conseguira
                            <strong>3 vitorias antes de 3 derrotas</strong>. Nao importa o caminho: 3-0, 3-1 ou 3-2 - todas contam!
                        </p>
                        <p style="color: var(--accent); font-weight: 600;">
                            Por isso {top_team[0]} tem {top_team[3]['3-0']:.2f}% de fazer 3-0, mas {top_team[1]:.2f}% de avancar (somando 3-0 + 3-1 + 3-2).
                        </p>
                    </div>
                </div>

                <div class="insight-box" style="background: linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(0, 230, 118, 0.1)); border-left-color: var(--accent);">
                    <h4 class="insight-box-title" style="color: var(--accent);">
                        <span>🎲</span> Estrategia para Pick'ems
                    </h4>
                    <div class="insight-grid">
                        <div class="insight-item">
                            <div class="insight-item-title">Pick 3-0</div>
                            <div class="insight-item-desc">
                                Escolha times top tier com matchups favoraveis pelo seeding. E arriscado mas vale mais pontos!
                            </div>
                        </div>
                        <div class="insight-item">
                            <div class="insight-item-title">Pick 0-3</div>
                            <div class="insight-item-desc">
                                Escolha os times mais fracos. Mais facil acertar que 3-0, pois times ruins tendem a perder consistentemente.
                            </div>
                        </div>
                        <div class="insight-item">
                            <div class="insight-item-title">Picks de Avancar</div>
                            <div class="insight-item-desc">
                                Escolha times com >70% de chance. Sao picks "seguros" onde voce maximiza a probabilidade de acerto.
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
                    Entenda como funciona o formato de competicao utilizado no Major
                </p>
            </div>

            <div class="swiss-explainer">
                <h3 class="swiss-title">Como Funciona o Swiss System</h3>
                <div class="swiss-steps">
                    <div class="swiss-step">
                        <div class="swiss-step-number">1</div>
                        <div class="swiss-step-content">
                            <h4>Seeding Inicial</h4>
                            <p>Convidados diretos (seeds 1-8) pelo Valve Global Standing; classificados do Stage 1 (seeds 9-16) por record Swiss + Buchholz</p>
                        </div>
                    </div>
                    <div class="swiss-step">
                        <div class="swiss-step-number">2</div>
                        <div class="swiss-step-content">
                            <h4>Confrontos por Record</h4>
                            <p>Times com mesmo numero de vitorias e derrotas jogam entre si (1-0 vs 1-0, 0-1 vs 0-1)</p>
                        </div>
                    </div>
                    <div class="swiss-step">
                        <div class="swiss-step-number">3</div>
                        <div class="swiss-step-content">
                            <h4>Emparelhamento por Buchholz</h4>
                            <p>Dentro de cada grupo de record, o sistema Buchholz determina os confrontos baseado na forca dos oponentes anteriores</p>
                        </div>
                    </div>
                    <div class="swiss-step">
                        <div class="swiss-step-number">4</div>
                        <div class="swiss-step-content">
                            <h4>Classificacao e Eliminacao</h4>
                            <p>Times com 3 vitorias avancam para o Stage 3 (Legends Stage), times com 3 derrotas sao eliminados. BO1 normal, BO3 em jogos de avanco/eliminacao.</p>
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
                <h2 class="section-title">Simulacoes Monte Carlo</h2>
                <p class="section-description">
                    Como geramos probabilidades confiaveis atraves de milhares de simulacoes
                </p>
            </div>

            <div class="swiss-explainer" style="border-color: rgba(0, 217, 255, 0.3);">
                <div style="text-align: center; margin-bottom: 40px;">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🎲</div>
                    <h3 class="swiss-title" style="color: var(--accent);">O que e Monte Carlo?</h3>
                    <p style="color: var(--text); font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
                        Monte Carlo e um metodo estatistico que usa <strong style="color: var(--accent);">aleatoriedade repetida</strong>
                        para calcular probabilidades de eventos complexos. Em vez de tentar calcular matematicamente todas as possibilidades,
                        nos <strong>simulamos o torneio milhares de vezes</strong> e contamos os resultados.
                    </p>
                </div>

                <div class="insight-box" style="background: rgba(0, 217, 255, 0.05); border-left-color: var(--accent);">
                    <h4 class="insight-box-title" style="color: var(--accent);">
                        <span>💡</span> Como Funciona na Pratica
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
                                    <strong style="color: var(--text);">Repetir 10.000 vezes:</strong> Cada simulacao pode ter resultados diferentes devido a aleatoriedade (upsets acontecem!). Depois de 10.000 simulacoes, temos um retrato estatistico muito preciso.
                                </div>
                            </div>
                            <div style="display: flex; gap: 15px; align-items: start;">
                                <div style="background: var(--accent); color: var(--dark); width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;">3</div>
                                <div>
                                    <strong style="color: var(--text);">Calcular probabilidades:</strong> Se {top_team[0]} fez 3-0 em {int(top_team[3]['3-0'] * 100)} das 10.000 simulacoes, sua probabilidade de 3-0 e {top_team[3]['3-0']:.2f}%. Simples assim!
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
                            Quanto mais simulacoes, mais precisas as probabilidades. 10.000 e o ponto ideal entre precisao e tempo de processamento.
                        </p>
                    </div>

                    <div style="background: rgba(0, 230, 118, 0.05); border: 1px solid var(--success); border-radius: 12px; padding: 25px;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">🎯</div>
                        <h4 style="color: var(--success); margin-bottom: 10px; font-size: 1.2rem;">Considera Upsets</h4>
                        <p style="color: var(--text-muted); font-size: 0.95rem;">
                            Times fracos podem vencer times fortes (com menor probabilidade). O Monte Carlo captura essa variancia naturalmente.
                        </p>
                    </div>

                    <div style="background: rgba(0, 217, 255, 0.05); border: 1px solid var(--accent); border-radius: 12px; padding: 25px;">
                        <div style="font-size: 2.5rem; margin-bottom: 15px;">🔬</div>
                        <h4 style="color: var(--accent); margin-bottom: 10px; font-size: 1.2rem;">Metodo Cientifico</h4>
                        <p style="color: var(--text-muted); font-size: 0.95rem;">
                            Usado em fisica, financas, meteorologia e esports. E uma tecnica comprovada para modelar sistemas complexos.
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
                    Seeds 1-8: convidados diretos (Valve Global Standing) | Seeds 9-16: classificados do Stage 1 (Swiss + Buchholz)
                </p>
            </div>

            <div class="seeding-grid">
"""

    for i, team in enumerate(INITIAL_SEEDING_COLOGNE_S2, 1):
        origin = "Convidado" if i <= 8 else f"Stage 1 ({TEAMS_DATA_COLOGNE_S2[team]['stage1_record']})"
        html += f"""                <div class="seed-card">
                    <div class="seed-number">Seed #{i} &middot; {origin}</div>
                    <div class="seed-team">{team}</div>
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
                <h2 class="section-title">Resultados das Simulacoes</h2>
                <p class="section-description">
                    10.000 simulacoes Monte Carlo com confrontos R1 reais e Swiss System correto
                </p>
            </div>

            <!-- Chart -->
            <div class="chart-container">
                <h3 class="chart-title">Distribuicao de Probabilidades - Top 8 Times</h3>
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
                            <th>HLTV</th>
                            <th>Stage 1</th>
                            <th class="prob-cell">3-0</th>
                            <th class="prob-cell">3-1</th>
                            <th class="prob-cell">3-2</th>
                            <th class="prob-cell total-advance">✅ Avancar</th>
                            <th class="prob-cell">2-3</th>
                            <th class="prob-cell">1-3</th>
                            <th class="prob-cell">0-3</th>
                            <th class="prob-cell total-eliminated">❌ Eliminar</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    for team, adv, elim, probs in advancement_probs:
        data = TEAMS_DATA_COLOGNE_S2[team]
        html += f"""                        <tr>
                            <td class="team-name">{team}</td>
                            <td>#{data['hltv_rank']}</td>
                            <td>{data['stage1_record']}</td>
                            <td class="prob-cell {prob_class(probs['3-0'])}">{probs['3-0']:.2f}%</td>
                            <td class="prob-cell {prob_class(probs['3-1'])}">{probs['3-1']:.2f}%</td>
                            <td class="prob-cell {prob_class(probs['3-2'])}">{probs['3-2']:.2f}%</td>
                            <td class="prob-cell total-advance">{adv:.2f}%</td>
                            <td class="prob-cell {prob_class(probs['2-3'])}">{probs['2-3']:.2f}%</td>
                            <td class="prob-cell {prob_class(probs['1-3'])}">{probs['1-3']:.2f}%</td>
                            <td class="prob-cell {prob_class(probs['0-3'])}">{probs['0-3']:.2f}%</td>
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
                <h2 class="final-picks-title">🎯 Recomendacoes Finais para Pick'ems</h2>
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
                            <span>✅</span> Avancam (Escolha 6)
                        </h3>
                        <ul class="pick-list" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 10px;">
"""

    for team, adv, elim, probs in advancing_filtered:
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
                <strong>⚠️ Aviso Importante:</strong> Estas predicoes sao baseadas em analise estatistica e 10.000 simulacoes Monte Carlo. CS2 tem alta variancia e upsets sao comuns no formato Swiss. Considere tambem noticias recentes, mudancas de roster e sua propria analise antes de fazer seus Pick'ems.
            </div>
            <p><strong>Stage 2:</strong> 6 a 9 de Junho, 2026 | Top 8 avancam para o Stage 3 (Legends Stage)</p>
            <p><strong>Formato:</strong> Swiss System (BO1 normal, BO3 em jogos de avanco/eliminacao)</p>
            <p style="margin-top: 20px;">📊 Analise gerada com Python | Simulacoes Monte Carlo | Dados: HLTV & Liquipedia</p>
            <p style="font-size: 0.85rem; margin-top: 15px;">© 2026 IEM Cologne Major Predictions | Boa sorte com seus Pick'ems! 🎮</p>
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
                        backgroundColor: 'rgba(255, 70, 85, 0.8)',
                        borderColor: 'rgba(255, 70, 85, 1)',
                        borderWidth: 1
                    }},
                    {{
                        label: '3-1',
                        data: {[round(v, 2) for v in chart_3_1]},
                        backgroundColor: 'rgba(255, 167, 38, 0.8)',
                        borderColor: 'rgba(255, 167, 38, 1)',
                        borderWidth: 1
                    }},
                    {{
                        label: '3-2',
                        data: {[round(v, 2) for v in chart_3_2]},
                        backgroundColor: 'rgba(0, 217, 255, 0.8)',
                        borderColor: 'rgba(0, 217, 255, 1)',
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
    print("Generating HTML for IEM Cologne Major 2026 Stage 2...")
    html_content = generate_html()

    with open("cologne_s2.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("HTML generated successfully: cologne_s2.html")
