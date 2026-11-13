"""
PhishGuard AI — Reusable UI Components v3.5
Hybrid Cyber Intelligence Platform: Tokens, Badges, and Metric Cards.
"""

import streamlit as st

def render_top_header():
    """Header platform berdesain Cyber Intelligence Command Center (Responsive Mobile & Desktop)."""
    st.markdown("""
    <div class="cyber-top-header">
        <div class="cyber-header-brand">
            <div style="width: 40px; height: 40px; min-width: 40px; border-radius: 10px; background: rgba(53, 214, 192, 0.14); border: 1px solid #35D6C0; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 18px rgba(53, 214, 192, 0.35);">
                <span style="font-size: 20px;">🛡️</span>
            </div>
            <div>
                <div style="font-size: 20px; font-weight: 700; letter-spacing: 0.04em; color: #E8F5F1; line-height: 1.2;">PHISHGUARD <span style="color: #35D6C0;">AI</span></div>
                <div style="font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.1em; color: #89AAA2;">Hybrid Cyber Intelligence Platform</div>
            </div>
        </div>
        <div class="cyber-header-badges">
            <div class="cyber-header-badge-item" style="display: flex; align-items: center; gap: 8px; background: rgba(16, 39, 34, 0.75); border: 1px solid rgba(53, 214, 192, 0.2); border-radius: 20px; padding: 6px 14px; font-size: 11.5px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #35D6C0; box-shadow: 0 0 8px #35D6C0;"></span>
                <span style="color: #89AAA2; font-weight: 600;">ENGINE:</span>
                <span style="color: #35D6C0; font-weight: 700;">RANDOM FOREST (100 TREES)</span>
            </div>
            <div class="cyber-header-badge-item" style="display: flex; align-items: center; gap: 8px; background: rgba(16, 39, 34, 0.75); border: 1px solid rgba(242, 201, 109, 0.25); border-radius: 20px; padding: 6px 14px; font-size: 11.5px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #F2C96D; box-shadow: 0 0 8px #F2C96D;"></span>
                <span style="color: #89AAA2; font-weight: 600;">PRECISION:</span>
                <span style="color: #F2C96D; font-weight: 700; font-family: monospace;">99.99%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, sub: str, variant: str = "turquoise"):
    """Render kartu metrik bergaya glassmorphism dengan aksen glow (Responsive Mobile & Desktop)."""
    color_map = {
        "turquoise": ("#35D6C0", "rgba(53, 214, 192, 0.35)"),
        "cyan": ("#35D6C0", "rgba(53, 214, 192, 0.35)"),
        "gold": ("#F2C96D", "rgba(242, 201, 109, 0.35)"),
        "purple": ("#9587FF", "rgba(149, 135, 255, 0.35)"),
        "pink": ("#E77DB8", "rgba(231, 125, 184, 0.35)"),
        "phishing": ("#FF5566", "rgba(255, 85, 102, 0.35)"),
        "legit": ("#35D6C0", "rgba(53, 214, 192, 0.35)")
    }
    color, glow = color_map.get(variant, color_map["turquoise"])
    
    st.markdown(f"""
    <div class="metric-tile">
        <div class="metric-tile-bar" style="background: {color}; box-shadow: 0 0 12px {color};"></div>
        <div class="metric-label">{title}</div>
        <div class="metric-number">{value}</div>
        <div class="metric-sub" style="color: {color};">{sub}</div>
    </div>
    """, unsafe_allow_html=True)
