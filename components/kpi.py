# components/kpi.py
def render_kpi_card(label, value, delta="", status="neutral", icon=""):
    status_colors = {
        "positive": "#38bdf8",
        "negative": "#f472b6",
        "gold": "#fbbf24",
        "neutral": "#818cf8"
    }
    glow_color = status_colors.get(status, "#818cf8")
    return f"""
    <div style="
        background: rgba(18, 18, 37, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    ">
        <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 600;">
            <span>{icon}</span> {label}
        </div>
        <div style="font-size: 2.1rem; font-weight: 800; color: {glow_color}; margin: 8px 0;">
            {value}
        </div>
        <div style="font-size: 0.85rem; font-weight: 500; color: {glow_color if status != 'neutral' else '#94a3b8'};">
            {delta}
        </div>
    </div>
    """
