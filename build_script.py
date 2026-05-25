import sys

html = """<!DOCTYPE html>
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
                <div class="sub-tab active">Control</div><div class="sub-tab">Results</div>
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
"""

css = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
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
"""

js = """const PALETTE = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#E69F00', '#56B4E9', '#F0E442', '#000000'];
let datasets = []; 
let activeDsId = null;
let annotations = [];
let mode = 'pointer'; 
let mainRange = { from: 10, to: 80 };
let currentZoom = null; 

let layoutMode = 'stacked'; // stacked, split, left, right
let settings = {
    whiteBg: true, showGrid: true, logY: false, smoothPts: 1,
    lineWidth: 1.2, xOffset: 0.0, yOffset: 0.0, yScale: 1.0,
};

function parseXY(text) {
    const pts = [];
    for (const l of text.split('\\n')) {
        const raw = l.trim();
        if (!raw || /^[#!;a-zA-Z]/.test(raw)) continue;
        const parts = raw.split(/[\\s,]+/);
        if (parts.length >= 2) pts.push({ x: +parts[0], y: +parts[1] });
    }
    return pts;
}

function smoothData(pts, windowSize) {
    if (windowSize <= 1) return pts;
    let smoothed = [];
    let half = Math.floor(windowSize / 2);
    for (let i = 0; i < pts.length; i++) {
        let sum = 0, count = 0;
        for (let j = Math.max(0, i - half); j < Math.min(pts.length, i + half + 1); j++) {
            sum += pts[j].y; count++;
        }
        smoothed.push({ x: pts[i].x, y: sum / count });
    }
    return smoothed;
}

function normalize(pts) {
    let maxY = d3.max(pts, d => d.y) || 1;
    let minY = d3.min(pts, d => d.y) || 0;
    return pts.map(d => ({ 
        x: d.x, 
        y: settings.logY ? Math.log10(Math.max(d.y, 1e-5)) - Math.log10(Math.max(minY, 1e-5)) : (d.y - minY) / (maxY - minY)
    }));
}

function findPeak(ds, targetX, window=2.0) {
    let data = ds.processedData;
    if(!data) return targetX;
    let candidates = data.filter(d => Math.abs(d.x - targetX) < window);
    if (!candidates.length) return targetX;
    let maxPt = candidates[0];
    for (let pt of candidates) {
        if (pt.y > maxPt.y) maxPt = pt;
    }
    return maxPt.x;
}

function processAllData() {
    datasets.forEach(ds => {
        let smoothed = smoothData(ds.rawData, settings.smoothPts);
        ds.processedData = normalize(smoothed);
    });
}

function scheduleRedraw() {
    processAllData();
    renderSidebar();
    drawPlot();
}

function renderSidebar() {
    const list = document.getElementById('dataset-list');
    if (!list) return;
    list.innerHTML = '';
    datasets.forEach(ds => {
        const div = document.createElement('div');
        div.className = `dataset-item ${ds.id === activeDsId ? 'active-ds' : ''}`;
        div.onclick = () => { activeDsId = ds.id; renderSidebar(); scheduleRedraw(); };
        
        const cb = document.createElement('input'); 
        cb.type = 'checkbox'; cb.checked = ds.visible;
        cb.onclick = (e) => { e.stopPropagation(); ds.visible = cb.checked; scheduleRedraw(); };
        
        const name = document.createElement('input');
        name.type = 'text'; name.className = 'ds-name'; name.value = ds.label;
        name.onchange = (e) => { ds.label = e.target.value; scheduleRedraw(); };
        name.onclick = e => e.stopPropagation();
        
        div.append(cb, name);
        list.appendChild(div);
    });
}

function drawPlot() {
    const svg = d3.select('#main-svg');
    if(svg.empty()) return;
    svg.selectAll('*').remove();
    
    const container = document.getElementById('plot-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    svg.attr('width', width).attr('height', height);
    if (settings.whiteBg) {
        svg.append('rect').attr('width', width).attr('height', height).attr('fill', '#fff');
    }
    
    const margin = { top: 20, right: 30, bottom: 40, left: 30 };
    const w = width - margin.left - margin.right;
    const h = height - margin.top - margin.bottom;
    
    const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`);
    
    let xDomain = currentZoom ? [currentZoom.from, currentZoom.to] : [mainRange.from, mainRange.to];
    const xScale = d3.scaleLinear().domain(xDomain).range([0, w]);
    
    if (settings.showGrid) {
        const xticks = xScale.ticks(10);
        xticks.forEach(tk => {
            g.append('line').attr('x1', xScale(tk)).attr('x2', xScale(tk)).attr('y1', 0).attr('y2', h)
             .attr('class', 'grid-line');
        });
        const yticks = d3.scaleLinear().domain([0,1]).range([h,0]).ticks(10);
        yticks.forEach(tk => {
            g.append('line').attr('x1', 0).attr('x2', w).attr('y1', tk).attr('y2', tk)
             .attr('class', 'grid-line');
        });
    }

    const vis = datasets.filter(d => d.visible);
    const n = Math.max(1, vis.length);
    
    let getYScale = (index) => {
        let base = d3.scaleLinear().domain([0, 1]).range([h, 0]);
        if (layoutMode === 'split') {
            let ch = h / n;
            return d3.scaleLinear().domain([0, 1]).range([h - index * ch, h - (index + 1) * ch + 10]);
        }
        return base;
    };

    const xAxisTop = d3.axisTop(xScale).tickSize(-6).tickFormat(''); 
    const xAxisBottom = d3.axisBottom(xScale).tickSize(6); 
    
    g.append('g').attr('class', 'axis').call(xAxisTop);
    g.append('g').attr('class', 'axis').attr('transform', `translate(0,${h})`).call(xAxisBottom);
    
    vis.forEach((ds, i) => {
        const yScale = getYScale(i);
        let offsetX = ds.id === activeDsId ? settings.xOffset : 0;
        let offsetY = ds.id === activeDsId ? settings.yOffset : 0;
        
        if (layoutMode === 'stacked') { offsetY += i * 0.5 * settings.yScale; offsetX += i * 0.5; }
        
        const line = d3.line()
            .x(d => xScale(d.x + offsetX))
            .y(d => yScale(d.y * settings.yScale + offsetY));
            
        g.append('path')
            .datum(ds.processedData)
            .attr('fill', 'none')
            .attr('stroke', ds.color)
            .attr('stroke-width', settings.lineWidth)
            .attr('d', line)
            .style('clip-path', 'url(#clip)');
            
        svg.append('clipPath').attr('id', 'clip').append('rect').attr('width', w).attr('height', h);
        
        // Render annotations specific to this dataset
        let dsAnns = annotations.filter(a => a.dsId === ds.id);
        dsAnns.forEach(ann => {
            let px = xScale(ann.x + offsetX);
            let pt = ds.processedData.find(d => Math.abs(d.x - ann.x) < 0.05);
            if (!pt) pt = {y: 0};
            let py = yScale(pt.y * settings.yScale + offsetY);
            
            if (px >= 0 && px <= w) {
                g.append('line')
                    .attr('x1', px).attr('x2', px)
                    .attr('y1', py).attr('y2', h)
                    .attr('stroke', 'black')
                    .attr('stroke-width', settings.lineWidth * 0.5)
                    .attr('stroke-dasharray', '2.2');
                
                g.append('text')
                    .attr('x', px).attr('y', py - 10)
                    .attr('text-anchor', 'middle')
                    .attr('font-size', '10px')
                    .text(ann.text || ann.x.toFixed(1));
            }
        });
    });

    let rect = g.append('rect')
        .attr('width', w).attr('height', h)
        .attr('fill', 'transparent')
        .style('cursor', mode === 'zoom' ? 'crosshair' : 'default');
        
    let isDragging = false;
    let startX = 0;
    
    rect.on('mousedown', (e) => {
        if (mode === 'pan' || mode === 'zoom') {
            isDragging = true;
            startX = d3.pointer(e)[0];
        } else if (mode === 'ann' || mode === 'hkl') {
             if(!activeDsId) return alert("Select a dataset in the Patterns List first.");
             let ds = datasets.find(d=>d.id === activeDsId);
             let mx = xScale.invert(d3.pointer(e)[0]);
             let peakX = findPeak(ds, mx);
             
             if(mode === 'ann') {
                 annotations.push({ dsId: activeDsId, x: peakX, text: peakX.toFixed(2) });
                 scheduleRedraw();
             } else {
                 const pop = document.getElementById('annotation-popover');
                 pop.style.display = 'block';
                 pop.style.left = e.pageX + 'px'; pop.style.top = e.pageY + 'px';
                 pop.dataset.targetX = peakX;
                 document.getElementById('ann-custom-text').focus();
             }
        }
    });

    rect.on('mousemove', (e) => {
        if(isDragging && mode === 'pan') {
           let dx = xScale.invert(startX) - xScale.invert(d3.pointer(e)[0]);
           if(currentZoom) { currentZoom.from += dx; currentZoom.to += dx; }
           else { mainRange.from += dx; mainRange.to += dx; }
           startX = d3.pointer(e)[0];
           drawPlot();
        }
    });

    rect.on('mouseup', (e) => {
        if (isDragging && mode === 'zoom') {
            let endX = d3.pointer(e)[0];
            let from = Math.min(xScale.invert(startX), xScale.invert(endX));
            let to = Math.max(xScale.invert(startX), xScale.invert(endX));
            if(Math.abs(from-to) > 0.1) {
                currentZoom = {from, to};
            }
            scheduleRedraw();
        }
        isDragging = false;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const modes = ['pointer','zoom','pan','ann','hkl'];
    modes.forEach(m => {
        let btn = document.getElementById(m + '-mode') || document.getElementById(m + '-mode-btn');
        if(btn) {
            btn.onclick = () => {
                mode = m;
                modes.forEach(x => { let b = document.getElementById(x+'-mode') || document.getElementById(x+'-mode-btn'); if(b) b.classList.remove('active'); });
                btn.classList.add('active');
            }
        }
    });

    const fi = document.getElementById('file-input');
    if (fi) {
      fi.addEventListener('change', async (e) => {
        for (let file of e.target.files) {
            let text = await file.text();
            let pts = parseXY(text);
            if (pts.length) {
                let id = Date.now() + Math.random();
                activeDsId = id;
                datasets.push({
                    id, label: file.name.replace(/\\.[^.]+$/, ''),
                    rawData: pts, visible: true,
                    color: PALETTE[datasets.length % PALETTE.length]
                });
            }
        }
        scheduleRedraw();
      });
    }

    const bindVal = (id, key, type='float') => {
        let el = document.getElementById(id);
        if(!el) return;
        el.oninput = (e) => {
            if(type==='float') settings[key] = parseFloat(e.target.value);
            else if(type==='int') settings[key] = parseInt(e.target.value);
            else settings[key] = e.target.checked;
            scheduleRedraw();
        };
    };
    bindVal('white-bg', 'whiteBg', 'bool');
    bindVal('show-grid', 'showGrid', 'bool');
    bindVal('log-y', 'logY', 'bool');
    bindVal('smooth-pts', 'smoothPts', 'int');
    bindVal('line-width', 'lineWidth', 'float');
    bindVal('x-offset', 'xOffset', 'float');
    bindVal('y-offset', 'yOffset', 'float');
    bindVal('y-scale', 'yScale', 'float');
    
    ['lbl-stacked','lbl-split','lbl-left','lbl-right'].forEach(id => {
       let el = document.getElementById(id);
       if(el) el.onclick = () => { layoutMode = id.split('-')[1]; scheduleRedraw(); };
    });
    
    if (document.getElementById('clear-ann')) document.getElementById('clear-ann').onclick = () => { annotations = []; scheduleRedraw(); };
    if (document.getElementById('ann-save-btn')) document.getElementById('ann-save-btn').onclick = () => {
             const pop = document.getElementById('annotation-popover');
             let txt = document.getElementById('ann-custom-text').value;
             annotations.push({ dsId: activeDsId, x: parseFloat(pop.dataset.targetX), text: txt });
             pop.style.display = 'none';
             scheduleRedraw();
    };
    if (document.getElementById('redraw-btn')) document.getElementById('redraw-btn').onclick = () => { currentZoom = null; scheduleRedraw(); };
    if (document.getElementById('peak-detect-btn')) document.getElementById('peak-detect-btn').onclick = () => {
         if(!activeDsId) return alert("Select a dataset first.");
         let ds = datasets.find(d=>d.id === activeDsId);
         if(ds && ds.processedData) {
              ds.processedData.forEach(d => {
                   if(d.y > 0.8) { 
                      let exists = annotations.find(a => a.dsId === ds.id && Math.abs(a.x - d.x) < 2.0);
                      if(!exists) annotations.push({dsId: ds.id, x: d.x, text: d.x.toFixed(1)});
                   }
              });
              scheduleRedraw();
         }
    };

    window.addEventListener('resize', scheduleRedraw);
    scheduleRedraw();
});
"""

with open("XRD.html", "w") as f: f.write(html)
with open("style.css", "w") as f: f.write(css)
with open("app.js", "w") as f: f.write(js)
