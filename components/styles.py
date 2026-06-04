# components/styles.py
def get_custom_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        .stApp { background: linear-gradient(135deg, #09090e 0%, #111124 50%, #07070f 100%) !important; color: #f8fafc !important; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #07070f 0%, #0d0d1e 100%) !important; border-right: 1px solid rgba(255, 255, 255, 0.05) !important; }
        .glass-panel { background: rgba(18, 18, 37, 0.45) !important; backdrop-filter: blur(12px) !important; border: 1px solid rgba(255, 255, 255, 0.06) !important; border-radius: 16px !important; padding: 24px !important; margin: 12px 0px !important; }
        .gradient-text { background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #f472b6 100%); -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; background-clip: text !important; font-weight: 800 !important; }
        .insight-box { background: linear-gradient(135deg, rgba(56, 189, 248, 0.08) 0%, rgba(129, 140, 248, 0.04) 100%); border-left: 4px solid #38bdf8; border-radius: 0 12px 12px 0; padding: 16px; margin: 16px 0; color: #cbd5e1; }
        .warning-box { background: linear-gradient(135deg, rgba(244, 114, 182, 0.08) 0%, rgba(129, 140, 248, 0.04) 100%); border-left: 4px solid #f472b6; border-radius: 0 12px 12px 0; padding: 16px; margin: 16px 0; color: #cbd5e1; }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """
