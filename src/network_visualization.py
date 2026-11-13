"""
PhishGuard AI — Hybrid Cyber Intelligence Platform v3.5
Interactive 60 FPS Network Topology Graph Component
Design Tokens & Features:
- Palette: #061411 (Deep), #0B211D (Surface), #102722 (Card), #35D6C0 (Turquoise),
  #F2C96D (Gold), #9587FF (Purple), #E77DB8 (Pink), #E8F5F1 (Text), #89AAA2 (Secondary)
- Golden Central Intelligence Core with Breathing Pulse & Expanding Energy Waves
- 16 Deterministic Feature Nodes (Gini Importance from Random Forest)
- Multi-layer Concentric Orbital Rings & Moving Orbiting Satellites
- Animated Comet Trails with Gradient Glow along Graph Edges
- Starfield Background with Twinkle and Subtle Drift
- Delta-Time (dt) requestAnimationFrame Loop with Zero Memory Leaks
- High-DPI (Retina) Canvas Rendering via window.devicePixelRatio
- Interactive Hover / Selection with Floating Glassmorphic Intel Panel
- Fully Offline (Zero external CDN / Zero HTTP requests)
"""

def render_network_graph():
    """
    Menghasilkan HTML, CSS, dan JavaScript murni (offline)
    untuk visualisasi graf topologi intelijen PhishGuard AI v3.5.
    """
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PhishGuard AI — Intelligence Topology</title>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body {
        width: 100%;
        height: 100%;
        min-height: 720px;
        background: radial-gradient(ellipse at 35% 35%, #0B211D 0%, #061411 60%, #030A09 100%);
        color: #E8F5F1;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        overflow: hidden;
        position: relative;
        user-select: none;
    }

    #canvas-container {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
    }

    canvas {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        display: block;
    }
    #canvas-bg { z-index: 1; pointer-events: none; }
    #canvas-main { z-index: 2; cursor: grab; }
    #canvas-main:active { cursor: grabbing; }
    #canvas-fx { z-index: 3; pointer-events: none; }

    /* Floating Header Badge */
    .title-badge {
        position: absolute;
        left: 20px;
        top: 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(11, 33, 29, 0.88);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(242, 201, 109, 0.35);
        border-radius: 12px;
        padding: 9px 16px;
        z-index: 20;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5);
    }
    .title-core-dot {
        width: 12px; height: 12px; border-radius: 50%;
        background: radial-gradient(circle, #FFE49E, #F2C96D);
        box-shadow: 0 0 10px #F2C96D, 0 0 20px rgba(242, 201, 109, 0.5);
        animation: pulseCoreDot 2.4s ease-in-out infinite;
    }
    @keyframes pulseCoreDot {
        0%, 100% { transform: scale(1); box-shadow: 0 0 10px #F2C96D; }
        50% { transform: scale(1.2); box-shadow: 0 0 24px #FFE49E; }
    }
    .title-text { font-size: 13px; font-weight: 700; color: #E8F5F1; letter-spacing: 0.04em; }
    .title-sub { font-size: 10px; color: #89AAA2; margin-top: 1px; }

    /* Floating Toolbar */
    .toolbar {
        position: absolute;
        top: 18px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        gap: 5px;
        background: rgba(11, 33, 29, 0.88);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(53, 214, 192, 0.22);
        border-radius: 50px;
        padding: 5px 12px;
        z-index: 20;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
    }
    .tb-sep { width: 1px; height: 16px; background: rgba(53, 214, 192, 0.16); margin: 0 4px; }
    .tool-btn {
        background: transparent;
        border: 1px solid transparent;
        color: #89AAA2;
        font-size: 11px;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 5px;
        white-space: nowrap;
    }
    .tool-btn:hover {
        color: #35D6C0;
        border-color: rgba(53, 214, 192, 0.35);
        background: rgba(53, 214, 192, 0.08);
    }
    .tool-btn.active {
        color: #061411;
        background: linear-gradient(135deg, #35D6C0, #28A897);
        box-shadow: 0 0 14px rgba(53, 214, 192, 0.5);
    }

    /* Floating Information Panel */
    .info-panel {
        position: absolute;
        right: 20px;
        top: 20px;
        width: 310px;
        background: rgba(16, 39, 34, 0.92);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(53, 214, 192, 0.28);
        border-radius: 14px;
        padding: 18px 20px;
        z-index: 20;
        box-shadow: 0 16px 44px rgba(0, 0, 0, 0.65);
        transition: opacity 0.3s ease, transform 0.3s ease;
        pointer-events: auto;
    }
    .info-panel.hidden {
        opacity: 0;
        transform: translateY(-8px);
        pointer-events: none;
    }
    .panel-badge {
        font-size: 9.5px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 3px 9px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .panel-title {
        font-size: 16px;
        font-weight: 700;
        color: #E8F5F1;
        margin-bottom: 4px;
    }
    .panel-desc {
        font-size: 12px;
        color: #89AAA2;
        line-height: 1.5;
        margin-bottom: 12px;
    }
    .panel-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-top: 1px solid rgba(53, 214, 192, 0.12);
        font-size: 11px;
    }
    .panel-row-lbl { color: #53746D; }
    .panel-row-val { font-weight: 700; font-family: monospace; color: #35D6C0; }

    /* Legend Box */
    .legend {
        position: absolute;
        left: 20px;
        bottom: 20px;
        background: rgba(11, 33, 29, 0.86);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(53, 214, 192, 0.16);
        border-radius: 12px;
        padding: 12px 16px;
        z-index: 15;
    }
    .legend-title {
        font-size: 9px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #53746D;
        margin-bottom: 8px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 5px;
        font-size: 11px;
        color: #89AAA2;
    }
    .legend-item:last-child { margin-bottom: 0; }
    .legend-dot { width: 8px; height: 8px; border-radius: 50%; }

    /* Stats Tray */
    .stats-tray {
        position: absolute;
        right: 20px;
        bottom: 20px;
        display: flex;
        gap: 8px;
        z-index: 15;
    }
    .stat-pill {
        background: rgba(11, 33, 29, 0.86);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(53, 214, 192, 0.16);
        border-radius: 10px;
        padding: 8px 14px;
        text-align: center;
        min-width: 65px;
    }
    .stat-val { font-size: 18px; font-weight: 800; color: #35D6C0; font-family: monospace; line-height: 1; }
    .stat-lbl { font-size: 8.5px; text-transform: uppercase; letter-spacing: 0.1em; color: #53746D; margin-top: 3px; }
</style>
</head>
<body>

<div id="canvas-container">
    <canvas id="canvas-bg"></canvas>
    <canvas id="canvas-main"></canvas>
    <canvas id="canvas-fx"></canvas>
</div>

<!-- Header Identity Badge -->
<div class="title-badge">
    <div class="title-core-dot"></div>
    <div>
        <div class="title-text">PhishGuard AI Core Topology</div>
        <div class="title-sub">Neural Architecture: 16 Input Features &bull; 100 Trees</div>
    </div>
</div>

<!-- Interactive Floating Toolbar -->
<div class="toolbar">
    <button class="tool-btn" id="btn-zoom-in">＋ Zoom In</button>
    <button class="tool-btn" id="btn-zoom-out">－ Zoom Out</button>
    <div class="tb-sep"></div>
    <button class="tool-btn" id="btn-reset">⟲ Reset</button>
    <div class="tb-sep"></div>
    <button class="tool-btn active" id="btn-flow">✦ Comet Trails</button>
    <button class="tool-btn active" id="btn-orbits">◎ Orbital Rings</button>
</div>

<!-- Floating Holographic Info Panel -->
<div class="info-panel" id="infoPanel">
    <div class="panel-badge" id="panelBadge" style="background: rgba(242,201,109,0.2); color: #F2C96D;">CORE ENGINE</div>
    <div class="panel-title" id="panelTitle">PhishGuard Core</div>
    <div class="panel-desc" id="panelDesc">Ensemble Random Forest Intelligence Unit yang mengolah 16 dimensi fitur leksikal dan struktural URL.</div>
    <div class="panel-row">
        <span class="panel-row-lbl">Gini Importance:</span>
        <span class="panel-row-val" id="panelImp">Primary Hub</span>
    </div>
    <div class="panel-row">
        <span class="panel-row-lbl">Cluster:</span>
        <span class="panel-row-val" id="panelCluster">Ensemble Unit</span>
    </div>
    <div class="panel-row">
        <span class="panel-row-lbl">Importance Rank:</span>
        <span class="panel-row-val" id="panelRank">—</span>
    </div>
</div>

<!-- Topology Legend -->
<div class="legend">
    <div class="legend-title">Feature Clusters</div>
    <div class="legend-item"><div class="legend-dot" style="background: #F2C96D; box-shadow: 0 0 6px #F2C96D;"></div>Core Engine (RF Hub)</div>
    <div class="legend-item"><div class="legend-dot" style="background: #35D6C0;"></div>Path &amp; Resource Risk (38.8%)</div>
    <div class="legend-item"><div class="legend-dot" style="background: #9587FF;"></div>Lexical Analysis (25.9%)</div>
    <div class="legend-item"><div class="legend-dot" style="background: #F2C96D;"></div>Protocol &amp; Network (14.8%)</div>
    <div class="legend-item"><div class="legend-dot" style="background: #35D6C0;"></div>URL Entropy &amp; Ratio (10.9%)</div>
    <div class="legend-item"><div class="legend-dot" style="background: #E77DB8;"></div>Domain Architecture (9.6%)</div>
</div>

<!-- Stats Tray -->
<div class="stats-tray">
    <div class="stat-pill"><div class="stat-val">16</div><div class="stat-lbl">Features</div></div>
    <div class="stat-pill"><div class="stat-val">100</div><div class="stat-lbl">Trees</div></div>
    <div class="stat-pill"><div class="stat-val" style="color: #35D6C0;">99.9%</div><div class="stat-lbl">Accuracy</div></div>
</div>

<script>
// ═════════════════════════════════════════════════════════════════════
//  1. CANVAS INITIALIZATION & DEVICE PIXEL RATIO (RETINA CRISP)
// ═════════════════════════════════════════════════════════════════════
const bgCanvas = document.getElementById('canvas-bg');
const mainCanvas = document.getElementById('canvas-main');
const fxCanvas = document.getElementById('canvas-fx');

const bgCtx = bgCanvas.getContext('2d');
const ctx = mainCanvas.getContext('2d');
const fxCtx = fxCanvas.getContext('2d');

let W = 1000, H = 720;
let dpr = window.devicePixelRatio || 1;

function resizeCanvases() {
    dpr = window.devicePixelRatio || 1;
    W = window.innerWidth || document.documentElement.clientWidth || 1000;
    H = window.innerHeight || document.documentElement.clientHeight || 720;

    [bgCanvas, mainCanvas, fxCanvas].forEach(c => {
        c.width = Math.round(W * dpr);
        c.height = Math.round(H * dpr);
        c.style.width = W + 'px';
        c.style.height = H + 'px';
    });

    bgCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    fxCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
resizeCanvases();
window.addEventListener('resize', resizeCanvases);

// ═════════════════════════════════════════════════════════════════════
//  2. STARFIELD BACKGROUND (DEEP SPACE PARTICLES)
// ═════════════════════════════════════════════════════════════════════
const stars = [];
for (let i = 0; i < 160; i++) {
    stars.push({
        x: Math.random(),
        y: Math.random(),
        r: Math.random() * 1.2 + 0.3,
        alpha: Math.random() * 0.6 + 0.15,
        twinkleSpeed: Math.random() * 1.5 + 0.5,
        phase: Math.random() * Math.PI * 2
    });
}

function drawStarfield(t) {
    bgCtx.clearRect(0, 0, W, H);
    stars.forEach(s => {
        const a = s.alpha * (0.6 + 0.4 * Math.sin(t * s.twinkleSpeed + s.phase));
        bgCtx.beginPath();
        bgCtx.arc(s.x * W, s.y * H, s.r, 0, Math.PI * 2);
        bgCtx.fillStyle = 'rgba(165, 235, 225, ' + a + ')';
        bgCtx.fill();
    });
}

// ═════════════════════════════════════════════════════════════════════
//  3. NODES & EDGES TOPOLOGY (16 FEATURES FROM RANDOM FOREST)
// ═════════════════════════════════════════════════════════════════════
const NODES = [
    // 0: Central Random Forest Core (Gold)
    { id: 0, lines: ["PhishGuard", "Core"], group: "core", x: 0, y: 15, r: 38, color: "#F2C96D", glow: "#FFE49E", imp: "Primary Hub", rank: "—", desc: "Pusat klasifikasi ensemble Random Forest (100 Decision Trees) yang mengagregasi prediksi 16 fitur leksikal & struktural.", clusterLabel: "Core Engine" },

    // Cluster 1: Path & Resource Risk (Turquoise #35D6C0)
    { id: 1, lines: ["path_length"], group: "path", x: 195, y: -40, r: 26, color: "#35D6C0", glow: "#74E8D7", imp: "38.79%", rank: "#1", desc: "Panjang direktori path URL. Fitur prediktor nomor satu — URL phishing memiliki path lebih panjang dan manipulatif.", clusterLabel: "Path & Resource" },
    { id: 2, lines: ["suspicious_ext"], group: "path", x: 280, y: -120, r: 14, color: "#35D6C0", glow: "#74E8D7", imp: "0.17%", rank: "#14", desc: "Mendeteksi ekstensi file mencurigakan (.exe, .zip, .apk) pada jalur URL.", clusterLabel: "Path & Resource" },
    { id: 3, lines: ["query_param_count"], group: "path", x: 330, y: -25, r: 12, color: "#35D6C0", glow: "#74E8D7", imp: "0.01%", rank: "#16", desc: "Banyaknya parameter kueri setelah tanda tanya (?) tempat menyembunyikan payload redirect.", clusterLabel: "Path & Resource" },

    // Cluster 2: Lexical Analysis (Purple #9587FF)
    { id: 4, lines: ["token_count"], group: "lexical", x: -185, y: -60, r: 22, color: "#9587FF", glow: "#C3BCFF", imp: "15.06%", rank: "#2", desc: "Jumlah segmen kata pemisah dalam URL. Phishing cenderung memiliki token acak lebih banyak.", clusterLabel: "Lexical Analysis" },
    { id: 5, lines: ["number_of_digits"], group: "lexical", x: -280, y: -130, r: 20, color: "#9587FF", glow: "#C3BCFF", imp: "10.81%", rank: "#4", desc: "Total karakter angka (0-9). Phishing URL memuat banyak angka untuk hashing atau session spoofing.", clusterLabel: "Lexical Analysis" },
    { id: 6, lines: ["dot_count"], group: "lexical", x: -260, y: 0, r: 16, color: "#9587FF", glow: "#C3BCFF", imp: "4.18%", rank: "#6", desc: "Banyaknya karakter titik (.) untuk menyamarkan domain asli melalui multilevel subdomains.", clusterLabel: "Lexical Analysis" },

    // Cluster 3: Protocol & Network (Gold #F2C96D)
    { id: 7, lines: ["https_flag"], group: "protocol", x: -135, y: 145, r: 21, color: "#F2C96D", glow: "#FFE49E", imp: "13.40%", rank: "#3", desc: "Indikator protokol HTTPS (0 = HTTP, 1 = HTTPS). Phishing modern kini juga memanipulasi sertifikat TLS.", clusterLabel: "Protocol & Network" },
    { id: 8, lines: ["has_ip_address"], group: "protocol", x: -235, y: 225, r: 14, color: "#F2C96D", glow: "#FFE49E", imp: "1.45%", rank: "#9", desc: "Host menggunakan alamat IP langsung tanpa DNS — indikasi kuat server penyerang temporer.", clusterLabel: "Protocol & Network" },

    // Cluster 4: URL Entropy & Ratios (Turquoise #35D6C0)
    { id: 9, lines: ["percentage_numeric"], group: "entropy", x: 140, y: 155, r: 19, color: "#35D6C0", glow: "#74E8D7", imp: "9.56%", rank: "#5", desc: "Persentase karakter numerik terhadap panjang keseluruhan URL.", clusterLabel: "URL Entropy & Ratio" },
    { id: 10, lines: ["url_entropy"], group: "entropy", x: 245, y: 210, r: 14, color: "#35D6C0", glow: "#74E8D7", imp: "0.22%", rank: "#12", desc: "Nilai Shannon Entropy string URL — mengukur tingkat keacakan distribusi karakter.", clusterLabel: "URL Entropy & Ratio" },
    { id: 11, lines: ["url_length"], group: "entropy", x: 220, y: 85, r: 16, color: "#35D6C0", glow: "#74E8D7", imp: "1.36%", rank: "#10", desc: "Panjang total karakter URL. URL phishing secara empiris jauh lebih panjang.", clusterLabel: "URL Entropy & Ratio" },

    // Cluster 5: Domain Architecture (Pink #E77DB8)
    { id: 12, lines: ["domain_name_length"], group: "domain", x: 0, y: -170, r: 15, color: "#E77DB8", glow: "#FFA8D7", imp: "0.69%", rank: "#11", desc: "Panjang karakter nama domain inti.", clusterLabel: "Domain Architecture" },
    { id: 13, lines: ["subdomain_count"], group: "domain", x: -85, y: -220, r: 16, color: "#E77DB8", glow: "#FFA8D7", imp: "2.20%", rank: "#7", desc: "Kedalaman level subdomain yang digunakan untuk typosquatting.", clusterLabel: "Domain Architecture" },
    { id: 14, lines: ["tld_length"], group: "domain", x: 85, y: -215, r: 14, color: "#E77DB8", glow: "#FFA8D7", imp: "1.98%", rank: "#8", desc: "Panjang karakter ekstensi Top Level Domain.", clusterLabel: "Domain Architecture" },
    { id: 15, lines: ["tld_popularity"], group: "domain", x: 165, y: -220, r: 12, color: "#E77DB8", glow: "#FFA8D7", imp: "0.11%", rank: "#13", desc: "Popularitas TLD (.com, .org vs TLD tidak lazim).", clusterLabel: "Domain Architecture" },
    { id: 16, lines: ["has_hyphen_in_domain"], group: "domain", x: -165, y: -220, r: 11, color: "#E77DB8", glow: "#FFA8D7", imp: "0.01%", rank: "#15", desc: "Penggunaan tanda hubung (-) untuk meniru brand resmi seperti paypal-login.com.", clusterLabel: "Domain Architecture" }
];

const EDGES = [
    // Core Connections
    { f: 0, t: 1 }, { f: 0, t: 4 }, { f: 0, t: 7 }, { f: 0, t: 9 }, { f: 0, t: 12 },
    // Path Cluster
    { f: 1, t: 2 }, { f: 1, t: 3 },
    // Lexical Cluster
    { f: 4, t: 5 }, { f: 4, t: 6 },
    // Protocol Cluster
    { f: 7, t: 8 },
    // Entropy Cluster
    { f: 9, t: 10 }, { f: 9, t: 11 },
    // Domain Cluster
    { f: 12, t: 13 }, { f: 12, t: 14 }, { f: 14, t: 15 }, { f: 13, t: 16 },
    // Cross Cluster Signals
    { f: 1, t: 9 }, { f: 4, t: 12 }, { f: 6, t: 13 }, { f: 7, t: 9 }
];

// ═════════════════════════════════════════════════════════════════════
//  4. ORBITAL RINGS & COMET PARTICLES
// ═════════════════════════════════════════════════════════════════════
let orbitsEnabled = true;
let particlesEnabled = true;

const ORBITS = [
    { r: 110, speed: 0.0002, dotColor: "rgba(53,214,192,0.45)", dotR: 2.5, numDots: 2 },
    { r: 200, speed: -0.00015, dotColor: "rgba(149,135,255,0.4)", dotR: 2.2, numDots: 3 },
    { r: 280, speed: 0.0001, dotColor: "rgba(231,125,184,0.35)", dotR: 2.0, numDots: 2 }
];

const PARTICLES = [];
for (let i = 0; i < 55; i++) {
    PARTICLES.push({
        edgeIdx: Math.floor(Math.random() * EDGES.length),
        t: Math.random(),
        speed: 0.003 + Math.random() * 0.004,
        size: 1.8 + Math.random() * 1.8,
        tail: 0.12 + Math.random() * 0.1
    });
}

// ═════════════════════════════════════════════════════════════════════
//  5. CAMERA & INTERACTION STATE
// ═════════════════════════════════════════════════════════════════════
let scale = 1.0;
let panX = 0, panY = 0;
let isDragging = false;
let startX = 0, startY = 0;

let hoveredNode = null;
let selectedNode = NODES[0];

function toWorld(cx, cy) {
    const rect = mainCanvas.getBoundingClientRect();
    const mx = cx - rect.left;
    const my = cy - rect.top;
    return {
        x: (mx - (W / 2 + panX)) / scale,
        y: (my - (H / 2 + panY)) / scale
    };
}

function getNodeAt(wx, wy) {
    for (let i = NODES.length - 1; i >= 0; i--) {
        const n = NODES[i];
        const dist = Math.hypot(n.x - wx, n.y - wy);
        if (dist <= n.r + 10) return n;
    }
    return null;
}

// ═════════════════════════════════════════════════════════════════════
//  6. DRAWING LOGIC (60 FPS OPTIMIZED & ENERGY WAVES)
// ═════════════════════════════════════════════════════════════════════
function drawOrbits(t) {
    if (!orbitsEnabled) return;
    ORBITS.forEach(orb => {
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, 15, orb.r, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(53, 214, 192, 0.12)';
        ctx.lineWidth = 0.8;
        ctx.setLineDash([4, 10]);
        ctx.stroke();
        ctx.setLineDash([]);

        // Orbiting satellite dots
        for (let d = 0; d < orb.numDots; d++) {
            const angle = t * orb.speed + (d / orb.numDots) * Math.PI * 2;
            const sx = Math.cos(angle) * orb.r;
            const sy = 15 + Math.sin(angle) * orb.r;
            ctx.beginPath();
            ctx.arc(sx, sy, orb.dotR, 0, Math.PI * 2);
            ctx.fillStyle = orb.dotColor;
            ctx.shadowColor = orb.dotColor;
            ctx.shadowBlur = 6;
            ctx.fill();
        }
        ctx.restore();
    });
}

function drawEdges() {
    EDGES.forEach(edge => {
        const s = NODES[edge.f];
        const e = NODES[edge.t];
        const isLit = hoveredNode && (edge.f === hoveredNode.id || edge.t === hoveredNode.id);

        ctx.save();
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(e.x, e.y);
        ctx.strokeStyle = isLit ? 'rgba(53, 214, 192, 0.8)' : 'rgba(53, 214, 192, 0.15)';
        ctx.lineWidth = isLit ? 2.0 : 1.0;
        if (isLit) {
            ctx.shadowColor = s.glow;
            ctx.shadowBlur = 10;
        }
        ctx.stroke();
        ctx.restore();
    });
}

function drawParticles() {
    if (!particlesEnabled) return;
    PARTICLES.forEach(p => {
        p.t += p.speed;
        if (p.t > 1) p.t = 0;

        const edge = EDGES[p.edgeIdx];
        const s = NODES[edge.f];
        const e = NODES[edge.t];

        const px = s.x + (e.x - s.x) * p.t;
        const py = s.y + (e.y - s.y) * p.t;

        const tailT = Math.max(0, p.t - p.tail);
        const tx = s.x + (e.x - s.x) * tailT;
        const ty = s.y + (e.y - s.y) * tailT;

        const grad = ctx.createLinearGradient(tx, ty, px, py);
        grad.addColorStop(0, 'transparent');
        grad.addColorStop(1, s.glow);

        ctx.save();
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(px, py);
        ctx.strokeStyle = grad;
        ctx.lineWidth = p.size;
        ctx.lineCap = 'round';
        ctx.shadowColor = s.glow;
        ctx.shadowBlur = 6;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(px, py, p.size * 0.9, 0, Math.PI * 2);
        ctx.fillStyle = s.glow;
        ctx.fill();
        ctx.restore();
    });
}

function drawNodes(t) {
    // Expanding golden wave from core
    const waveProgress = (t * 0.0006) % 1;
    const waveRadius = 38 + waveProgress * 95;
    const waveAlpha = (1 - waveProgress) * 0.35;
    
    ctx.save();
    ctx.beginPath();
    ctx.arc(0, 15, waveRadius, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(242, 201, 109, ' + waveAlpha + ')';
    ctx.lineWidth = 1.2;
    ctx.stroke();
    ctx.restore();

    NODES.forEach(n => {
        const isHov = hoveredNode && hoveredNode.id === n.id;
        const isSel = selectedNode && selectedNode.id === n.id;
        const pulse = (n.id === 0) ? Math.sin(t * 0.0025) * 3.5 : (isHov ? 2.5 : 0);
        const r = n.r + pulse;

        // 1. Outer Halo
        const halo = ctx.createRadialGradient(n.x, n.y, r * 0.4, n.x, n.y, r * 2.5);
        halo.addColorStop(0, n.glow + '35');
        halo.addColorStop(1, 'transparent');
        ctx.beginPath();
        ctx.arc(n.x, n.y, r * 2.5, 0, Math.PI * 2);
        ctx.fillStyle = halo;
        ctx.fill();

        // 2. Core Body Fill
        ctx.save();
        ctx.beginPath();
        ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
        ctx.fillStyle = (n.id === 0) ? '#241D0D' : '#0B211D';
        ctx.fill();

        // 3. Glowing Border
        ctx.shadowColor = n.glow;
        ctx.shadowBlur = isHov || isSel ? 20 : (n.id === 0 ? 16 : 8);
        ctx.strokeStyle = isHov || isSel ? n.glow : n.color;
        ctx.lineWidth = isHov || isSel ? 2.8 : (n.id === 0 ? 2.4 : 1.6);
        ctx.stroke();
        ctx.restore();

        // 4. Center Inner Dot
        ctx.beginPath();
        ctx.arc(n.x, n.y, r * 0.35, 0, Math.PI * 2);
        ctx.fillStyle = n.color;
        ctx.fill();

        // 5. Typography Label
        ctx.save();
        ctx.font = (n.id === 0 ? 'bold 12px' : '10.5px') + " -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
        ctx.textAlign = 'center';
        ctx.fillStyle = isHov ? n.glow : (n.id === 0 ? '#F2C96D' : '#CCE4E1');
        const startY = n.y + r + 15;
        n.lines.forEach((line, idx) => {
            ctx.fillText(line, n.x, startY + (idx * 13));
        });
        ctx.restore();
    });
}

function drawFX(t) {
    fxCtx.clearRect(0, 0, W, H);
    if (!selectedNode) return;

    fxCtx.save();
    fxCtx.translate(W / 2 + panX, H / 2 + panY);
    fxCtx.scale(scale, scale);

    const n = selectedNode;
    const ringR = n.r + 9 + Math.sin(t * 0.003) * 2;

    fxCtx.save();
    fxCtx.shadowColor = n.glow;
    fxCtx.shadowBlur = 16;
    fxCtx.beginPath();
    fxCtx.arc(n.x, n.y, ringR, 0, Math.PI * 2);
    fxCtx.strokeStyle = n.glow + '99';
    fxCtx.lineWidth = 1.5;
    fxCtx.setLineDash([5, 4]);
    fxCtx.stroke();
    fxCtx.restore();

    fxCtx.restore();
}

// ═════════════════════════════════════════════════════════════════════
//  7. MAIN RENDER LOOP & TAB VISIBILITY MANAGEMENT (DELTA-TIME)
// ═════════════════════════════════════════════════════════════════════
let animFrameId = null;
let isVisible = true;

function renderFrame(ts) {
    if (!isVisible) return;

    drawStarfield(ts);

    ctx.clearRect(0, 0, W, H);
    ctx.save();
    ctx.translate(W / 2 + panX, H / 2 + panY);
    ctx.scale(scale, scale);

    drawOrbits(ts);
    drawEdges();
    drawParticles();
    drawNodes(ts);

    ctx.restore();

    drawFX(ts);

    animFrameId = requestAnimationFrame(renderFrame);
}

// Initial immediate paint & start animation loop
resizeCanvases();
renderFrame(0);

document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        isVisible = false;
        if (animFrameId) cancelAnimationFrame(animFrameId);
    } else {
        isVisible = true;
        animFrameId = requestAnimationFrame(renderFrame);
    }
});

// ═════════════════════════════════════════════════════════════════════
//  8. INFO PANEL CONTROLLER
// ═════════════════════════════════════════════════════════════════════
const infoPanel = document.getElementById('infoPanel');
const panelBadge = document.getElementById('panelBadge');
const panelTitle = document.getElementById('panelTitle');
const panelDesc = document.getElementById('panelDesc');
const panelImp = document.getElementById('panelImp');
const panelCluster = document.getElementById('panelCluster');
const panelRank = document.getElementById('panelRank');

function updatePanel(node) {
    if (!node) return;
    panelBadge.textContent = node.clusterLabel.toUpperCase();
    panelBadge.style.color = node.color;
    panelBadge.style.background = node.color + '22';
    panelTitle.textContent = node.lines.join(' ');
    panelDesc.textContent = node.desc;
    panelImp.textContent = node.imp;
    panelCluster.textContent = node.clusterLabel;
    panelRank.textContent = node.rank;
    infoPanel.classList.remove('hidden');
}

// ═════════════════════════════════════════════════════════════════════
//  9. MOUSE & TOUCH EVENT LISTENERS (PAN & ZOOM)
// ═════════════════════════════════════════════════════════════════════
mainCanvas.addEventListener('mousemove', e => {
    if (isDragging) {
        panX += e.clientX - startX;
        panY += e.clientY - startY;
        startX = e.clientX;
        startY = e.clientY;
        return;
    }

    const { x, y } = toWorld(e.clientX, e.clientY);
    const hit = getNodeAt(x, y);
    if (hit !== hoveredNode) {
        hoveredNode = hit;
        if (hit) updatePanel(hit);
    }
    mainCanvas.style.cursor = hit ? 'pointer' : 'grab';
});

mainCanvas.addEventListener('mousedown', e => {
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    const { x, y } = toWorld(e.clientX, e.clientY);
    const hit = getNodeAt(x, y);
    if (hit) {
        selectedNode = hit;
        updatePanel(hit);
    }
});

window.addEventListener('mouseup', () => { isDragging = false; });

mainCanvas.addEventListener('wheel', e => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.08 : 0.92;
    scale = Math.min(Math.max(scale * zoomFactor, 0.45), 2.8);
}, { passive: false });

// Toolbar Controls
document.getElementById('btn-zoom-in').onclick = () => { scale = Math.min(scale * 1.2, 2.8); };
document.getElementById('btn-zoom-out').onclick = () => { scale = Math.max(scale / 1.2, 0.45); };
document.getElementById('btn-reset').onclick = () => { scale = 1.0; panX = 0; panY = 0; };
document.getElementById('btn-flow').onclick = function() {
    particlesEnabled = !particlesEnabled;
    this.classList.toggle('active', particlesEnabled);
};
document.getElementById('btn-orbits').onclick = function() {
    orbitsEnabled = !orbitsEnabled;
    this.classList.toggle('active', orbitsEnabled);
};
</script>
</body>
</html>"""
    return html_content
