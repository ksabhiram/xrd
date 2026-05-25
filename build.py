with open("XRD.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>XRD Plot Tool</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
    <link rel="stylesheet" href="style.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="layout">
        <div class="sidebar patterns-sidebar">
            <div class="mac-dots">
                <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
            </div>
            <div class="patterns-title">PATTERNS LIST</div>
            <div class="dataset-list" id="dataset-list"></div>
            <label class="upload-zone" id="drop-zone">
                <input type="file" id="file-input" multiple accept=".csv,.txt,.xy,.dat,.xye,.x_y">
                + Add Data
            </label>
        </div>

        <div class="main">
            <div class="top-toolbar">
                <div class="doc-title">
                    <strong id="doc-title-text">Untitled</strong><br>
                    <span style="font-size:10px;color:gray">Constant-Wavelength X-Rays</span>
                </div>
                <div class="tools-group">
                    <button class="btn icon-btn" id="pointer-mode" title="Pointer"><i class="fas fa-hand-pointer"></i></button>
                    <button class="btn icon-btn" id="zoom-mode-btn" title="Zoom"><i class="fas fa-search"></i></button>
                    <button class="btn icon-btn" id="pan-mode-btn" title="Pan"><i class="fas fa-arrows-alt"></i></button>
                    <div class="divider"></div>
                    <button class="btn icon-btn" id="ann-mode-btn" title="Add Annotation"><i class="fas fa-tags"></i></button>
                    <button class="btn icon-btn" id="hkl-mode-btn" title="HKL"><i class="fas fa-cube"></i></button>
                </div>
                <div class="tools-group right-tools">
                   <button class="btn" id="redraw-btn">↺ Redraw</button>
                </div>
            </div>
            <div class="plot-container" id="plot-container">
                <svg id="main-svg"></svg>
            </div>
        </div>

        <div class="sidebar right-sidebar">
            <div class="sidebar-tabs">
                <div class="tab active">Display</div><div class="tab">Simulate</div><div class="tab">Refine</div>
            </div>
            <div class="sub-tabs">
                <div class="sub-tab active">Control</div><div class=\"sub-tab\">Results</div>
            </div>
            
            <div class="accordion">
                <details open><summary><i class="fas fa-chart-line"></i> Plot Settings</summary>
                    <div class="content">
                        <div class="ctrl-row"><label>White Background</label><input type="checkbox" id="white-bg" checked></div>
                        <div class="ctrl-row"><label>Grid Lines</label><input type="checkbox" id="show-grid" checked></div>
                        <div class="ctrl-row"><label>Log Scale Y</label><input type="checkbox" id="log-y"></div>
                        <div class="ctrl-row"><label>Smoothing (pts)</label><input type="number" id="smooth-pts" value="1" min="1" max="100" class="numinput"></div>
                        <div class="ctrl-row"><label>Line width</label><input type="range" id="line-width" min="0.1" max="5" step="0.1" value="1.2"></div>
                    </div>
                </details>
                
                <details open><summary><i class="fas fa-crosshairs"></i> Position &amp; Scale</summary>
                    <div class="content">
                        <div class="labeled-buttons" style="display:flex;gap:5px;margin-bottom:10px;">
                            <span>Label:</span>
                            <button id="lbl-left" class="btn small">Left</button>
                            <button id="lbl-right" class="btn small">Right</button>
                            <button id="lbl-stacked" class="btn small">☰ Stacked</button>
                            <button id="lbl-split" class="btn small">⫷⫸ Split</button>
                        </div>
                        <div class="ctrl-row"><label>X Offset:</label><input type="number" class="numinput" id="x-offset" step="0.1" value="0.0"></div>
                        <div class="ctrl-row"><label>Y Offset:</label><input type="number" class="numinput" id="y-offset" step="0.1" value="0.0"></div>
                        <div class="ctrl-row"><label>Y Scale:</label><input type="range" id="y-scale" min="0.1" max="10" step="0.1" value="1.0"></div>
                    </div>
                </details>

                <details open><summary><i class="fas fa-mountain"></i> Annotations</summary>
                    <div class="content">
                        <button class="btn" id="peak-detect-btn" style="width:100%;margin-bottom:5px;">Auto Detect Peaks</button>
                        <button class="btn" id="clear-ann" style="width:100%;color:#c44;">Clear All</button>
                    </div>
                </details>
            </div>
        </div>
    </div>
    
    <div id="annotation-popover" class="annotation-popover" style="display:none;position:absolute;z-index:9999;background:white;padding:10px;border:1px solid #ccc;">
        <input type="text" id="ann-custom-text" placeholder="Custom text (hkl)">
        <button id="ann-save-btn" class="btn">Save</button>
    </div>

    <script src="app.js"></script>
</body>
</html>
""")

with open("style.css", "w") as f:
    f.write("""@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
:root { --bg: #f2f2f2; --panel: #ffffff; --border: #d0d0d0; --text: #333; --accent: #0055ff; }
body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); height: 100vh; margin: 0; display: flex; flex-direction: column; overflow: hidden; }
.top-toolbar { display: flex; align-items: center; padding: 10px 15px; background: white; border-bottom: 1px solid var(--border); }
.doc-title { margin-right: 20px; line-height: 1.2; }
.tools-group { display: flex; gap: 5px; align-items: center; }
.right-tools { margin-left: auto; }
.icon-btn { background: transparent; border: none; font-size: 16px; width: 32px; height: 32px; cursor: pointer; color: #555; border-radius: 4px; }
.icon-btn:hover { background: #eee; }
.icon-btn.active { background: #e0ebff; color: var(--accent); }
.divider { width: 1px; height: 20px; background: var(--border); margin: 0 5px; }

.layout { display: flex; flex: 1; overflow: hidden; }
.sidebar { background: var(--panel); display: flex; flex-direction: column; }
.patterns-sidebar { width: 220px; min-width: 220px; border-right: 1px solid var(--border); padding: 10px; background: #e8e8e8; overflow-y:auto; }
.right-sidebar { width: 300px; min-width: 300px; border-left: 1px solid var(--border); overflow-y: auto; background:#f9f9f9; }
.main { flex: 1; display: flex; flex-direction: column; background: #fff; position: relative; overflow:hidden;}
.plot-container { flex: 1; display: block; overflow: hidden; position: relative; background: #fff; margin: 10px; border:1px solid #ccc; box-shadow:0 0 5px rgba(0,0,0,0.1); }
svg { outline: none; }

.mac-dots { display: flex; gap: 6px; margin-bottom: 20px; }
.dot { width: 12px; height: 12px; border-radius: 50%; }
.dot.red { background: #ff5f56; }
.dot.yellow { background: #ffbd2e; }
.dot.green { background: #27c93f; }
.patterns-title { font-size: 11px; font-weight: 600; color: #777; margin-bottom: 10px; }

.sidebar-tabs { display: flex; background: #fafafa; border-bottom: 1px solid var(--border); }
.tab { flex: 1; text-align: center; padding: 8px 0; font-size: 12px; cursor: pointer; color: #666; border-right: 1px solid var(--border); }
.tab.active { background: white; font-weight: 600; color: var(--accent); border-bottom: 2px solid var(--accent); margin-bottom: -1px; }
.sub-tabs { display: flex; justify-content: center; gap: 10px; padding: 10px; background: white; border-bottom: 1px solid var(--border); }
.sub-tab { font-size: 11px; padding: 3px 15px; border-radius: 12px; background: #eee; cursor: pointer; }
.sub-tab.active { background: var(--accent); color: white; }

details {  }
summary { padding: 10px; font-size: 13px; font-weight: 600; cursor: pointer; user-select: none; outline: none; display: flex; align-items: center; gap: 8px; border-top:1px solid #eee;}
.content { padding: 10px; background: #fff; font-size:12px;}

.upload-zone { display: block; text-align: center; padding: 15px; background: #ddd; border: 1px dashed #aaa; border-radius: 5px; cursor: pointer; color: #555; text-decoration: none; margin-top: auto; font-size:12px; }
.upload-zone input { display:none; }
.dataset-item { background: white; padding: 6px 10px; border-radius: 6px; margin-bottom: 5px; display: flex; align-items: center; font-size: 12px; cursor: pointer; border: 1px solid transparent; gap:5px;}
.dataset-item.active-ds { background:#eef5ff; border-color: var(--accent); }
.ds-name { flex:1; margin-left: 5px; outline:none; border:none; background:transparent; font-size:12px; width:100%;}
.btn { padding: 5px 10px; border: 1px solid var(--border); border-radius: 4px; background: white; cursor: pointer; font-size: 11px; font-family: inherit; }
.btn:hover { background: #f0f0f0; }
.btn.small { padding: 2px 6px; font-size: 10px; }
.ctrl-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 12px; }
.ctrl-row label { color: #555; }
.numinput { width: 60px; padding: 2px 4px; border: 1px solid var(--border); border-radius: 3px; font-family:inherit;}
input[type=range] { flex: 1; margin: 0 10px; }

.grid-line { stroke: #e0e8f0; stroke-width: 1; }
.axis text { font-family: 'Inter', sans-serif; font-size:12px; }
""")
