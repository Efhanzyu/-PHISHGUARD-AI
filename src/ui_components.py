"""
PhishGuard AI — Reusable UI Components v3.5
Hybrid Cyber Intelligence Platform: Tokens, Badges, and Metric Cards.
"""

import streamlit as st

def render_top_header():
    """Header platform berdesain Cyber Intelligence Command Center."""
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0 18px 0; border-bottom: 1px solid rgba(53, 214, 192, 0.16); margin-bottom: 22px;">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 40px; height: 40px; border-radius: 10px; background: rgba(53, 214, 192, 0.14); border: 1px solid #35D6C0; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 18px rgba(53, 214, 192, 0.35);">
                <span style="font-size: 20px;">🛡️</span>
            </div>
            <div>
                <div style="font-size: 20px; font-weight: 700; letter-spacing: 0.04em; color: #E8F5F1;">PHISHGUARD <span style="color: #35D6C0;">AI</span></div>
                <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.12em; color: #89AAA2;">Hybrid Cyber Intelligence Platform</div>
            </div>
        </div>
        <div style="display: flex; gap: 14px; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px; background: rgba(16, 39, 34, 0.75); border: 1px solid rgba(53, 214, 192, 0.2); border-radius: 20px; padding: 6px 14px; font-size: 11.5px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #35D6C0; box-shadow: 0 0 8px #35D6C0;"></span>
                <span style="color: #89AAA2; font-weight: 600;">ENGINE:</span>
                <span style="color: #35D6C0; font-weight: 700;">RANDOM FOREST (100 TREES)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; background: rgba(16, 39, 34, 0.75); border: 1px solid rgba(242, 201, 109, 0.25); border-radius: 20px; padding: 6px 14px; font-size: 11.5px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #F2C96D; box-shadow: 0 0 8px #F2C96D;"></span>
                <span style="color: #89AAA2; font-weight: 600;">PRECISION:</span>
                <span style="color: #F2C96D; font-weight: 700; font-family: monospace;">99.99%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, sub: str, variant: str = "turquoise"):
    """Render kartu metrik bergaya glassmorphism dengan aksen glow."""
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
    <div style="background: rgba(16, 39, 34, 0.78); backdrop-filter: blur(16px); border: 1px solid rgba(53, 214, 192, 0.16); border-radius: 13px; padding: 18px 20px; position: relative; overflow: hidden; box-shadow: 0 8px 30px rgba(0,0,0,0.4); margin-bottom: 14px;">
        <div style="position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: {color}; box-shadow: 0 0 12px {color};"></div>
        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #89AAA2; font-weight: 600;">{title}</div>
        <div style="font-size: 28px; font-weight: 700; color: #E8F5F1; margin: 4px 0; font-family: 'JetBrains Mono', monospace;">{value}</div>
        <div style="font-size: 12px; color: {color}; font-weight: 500;">{sub}</div>
    </div>
    """, unsafe_allow_html=True)
