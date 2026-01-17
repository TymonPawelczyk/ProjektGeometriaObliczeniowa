const canvas = document.getElementById('geometryCanvas');
const ctx = canvas.getContext('2d');
const statusInfo = document.getElementById('statusInfo');
const descInfo = document.getElementById('descInfo');
const coordsContainer = document.getElementById('coordsContainer');
const coordsInfo = document.getElementById('coordsInfo');
const inputsContainer = document.getElementById('inputsContainer');

let points = [];
let cachedHullResult = null; 
const MAX_POINTS = 4;

// --- STAN WIDOKU (KAMERA) ---
const View = {
    scale: 3.0,       
    offsetX: canvas.width / 2, 
    offsetY: canvas.height / 2, 
    isDragging: false,
    lastMouseX: 0,
    lastMouseY: 0,
    dragDistance: 0
};

// --- KONWERSJA WSPÓŁRZĘDNYCH ---

function pixelToMath(px, py) {
    return {
        x: (px - View.offsetX) / View.scale,
        y: (View.offsetY - py) / View.scale
    };
}

function mathToPixel(mx, my) {
    return {
        x: View.offsetX + (mx * View.scale),
        y: View.offsetY - (my * View.scale)
    };
}

// --- OBSŁUGA INTERAKCJI ---

canvas.addEventListener('wheel', (event) => {
    event.preventDefault();
    const zoomIntensity = 0.1;
    const direction = event.deltaY < 0 ? 1 : -1;
    const factor = 1 + (zoomIntensity * direction);
    const mousePos = getMousePos(canvas, event);
    const mouseMathBefore = pixelToMath(mousePos.x, mousePos.y);

    View.scale *= factor;
    View.scale = Math.max(0.1, Math.min(View.scale, 500));

    View.offsetX = mousePos.x - (mouseMathBefore.x * View.scale);
    View.offsetY = mousePos.y + (mouseMathBefore.y * View.scale);

    redrawAll();
});

canvas.addEventListener('mousedown', (event) => {
    View.isDragging = true;
    const pos = getMousePos(canvas, event);
    View.lastMouseX = pos.x;
    View.lastMouseY = pos.y;
    View.dragDistance = 0;
});

canvas.addEventListener('mousemove', (event) => {
    if (!View.isDragging) return;
    const pos = getMousePos(canvas, event);
    const dx = pos.x - View.lastMouseX;
    const dy = pos.y - View.lastMouseY;
    View.offsetX += dx;
    View.offsetY += dy;
    View.lastMouseX = pos.x;
    View.lastMouseY = pos.y;
    View.dragDistance += Math.abs(dx) + Math.abs(dy);
    redrawAll();
});

canvas.addEventListener('mouseup', (event) => {
    View.isDragging = false;
    if (View.dragDistance < 5) {
        handleCanvasClick(event);
    }
});

canvas.addEventListener('mouseleave', () => { View.isDragging = false; });

// --- LOGIKA ---

function handleCanvasClick(evt) {
    if (points.length >= MAX_POINTS) return;
    const pos = getMousePos(canvas, evt);
    let mathPos = pixelToMath(pos.x, pos.y);
    mathPos.x = Math.round(mathPos.x * 100) / 100;
    mathPos.y = Math.round(mathPos.y * 100) / 100;
    points.push(mathPos);
    cachedHullResult = null;
    updateInputsFromPoints();
    redrawAll();
    if (points.length === MAX_POINTS) updateHull();
}

function createInputs() {
    inputsContainer.innerHTML = '';
    for (let i = 0; i < MAX_POINTS; i++) {
        const div = document.createElement('div');
        div.className = 'point-input-group';
        div.innerHTML = `
            <label>Punkt ${i+1}</label>
            <div class="inputs-row">
                <input type="number" id="p${i}_x" placeholder="X" step="0.1">
                <input type="number" id="p${i}_y" placeholder="Y" step="0.1">
            </div>
        `;
        inputsContainer.appendChild(div);
    }
}

function updateInputsFromPoints() {
    for (let i = 0; i < MAX_POINTS; i++) {
        const inputX = document.getElementById(`p${i}_x`);
        const inputY = document.getElementById(`p${i}_y`);
        if (i < points.length) {
            inputX.value = points[i].x.toFixed(1);
            inputY.value = points[i].y.toFixed(1);
        } else {
            inputX.value = '';
            inputY.value = '';
        }
    }
}

function calculateFromInputs() {
    const newPoints = [];
    for (let i = 0; i < MAX_POINTS; i++) {
        const valX = document.getElementById(`p${i}_x`).value;
        const valY = document.getElementById(`p${i}_y`).value;
        if (valX !== '' && valY !== '') {
            newPoints.push({ x: parseFloat(valX), y: parseFloat(valY) });
        }
    }
    if (newPoints.length < 1) return;
    points = newPoints;
    cachedHullResult = null;
    centerViewOnPoints(points);
    redrawAll();
    if (points.length >= 3) updateHull();
}

function centerViewOnPoints(pts) {
    if (pts.length === 0) return;
    let minX = pts[0].x, maxX = pts[0].x, minY = pts[0].y, maxY = pts[0].y;
    pts.forEach(p => {
        if (p.x < minX) minX = p.x; if (p.x > maxX) maxX = p.x;
        if (p.y < minY) minY = p.y; if (p.y > maxY) maxY = p.y;
    });
    View.offsetX = canvas.width / 2 - ((minX + maxX) / 2 * View.scale);
    View.offsetY = canvas.height / 2 + ((minY + maxY) / 2 * View.scale);
}

function redrawAll() {
    drawGrid();
    points.forEach((p, idx) => {
        const pix = mathToPixel(p.x, p.y);
        drawPoint(pix.x, pix.y, `P${idx+1} (${p.x.toFixed(1)}, ${p.y.toFixed(1)})`);
    });
    if (cachedHullResult) {
        drawHull(cachedHullResult.hull);
        statusInfo.innerText = `Wynik: ${cachedHullResult.shape_type}`;
        statusInfo.style.color = "#007bff";
    } else {
        statusInfo.innerText = points.length === MAX_POINTS ? "Analiza..." : `Punkty: ${points.length}/${MAX_POINTS}`;
        statusInfo.style.color = "#555";
    }
}

function getMousePos(canvas, evt) {
    const rect = canvas.getBoundingClientRect();
    return { x: evt.clientX - rect.left, y: evt.clientY - rect.top };
}

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 1;
    ctx.font = '10px Arial';
    ctx.fillStyle = '#888';

    let targetPixelStep = 80;
    let rawStep = targetPixelStep / View.scale;
    let magnitude = Math.pow(10, Math.floor(Math.log10(rawStep)));
    let residual = rawStep / magnitude;
    let step = residual > 5 ? 10 * magnitude : (residual > 2 ? 5 * magnitude : (residual > 1 ? 2 * magnitude : magnitude));

    const topLeft = pixelToMath(0, 0);
    const bottomRight = pixelToMath(canvas.width, canvas.height);
    const startX = Math.floor(topLeft.x / step) * step;
    const endX = Math.ceil(bottomRight.x / step) * step;
    const startY = Math.floor(bottomRight.y / step) * step;
    const endY = Math.ceil(topLeft.y / step) * step;

    for(let x = startX; x <= endX; x += step) {
        x = Math.round(x * 1000) / 1000;
        const p = mathToPixel(x, 0);
        if (x !== 0) {
            ctx.beginPath(); ctx.moveTo(p.x, 0); ctx.lineTo(p.x, canvas.height); ctx.stroke();
            let labelY = Math.min(Math.max(mathToPixel(0, 0).y + 12, 12), canvas.height - 5);
            ctx.fillText(x, p.x + 2, labelY);
        }
    }
    for(let y = startY; y <= endY; y += step) {
        y = Math.round(y * 1000) / 1000;
        const p = mathToPixel(0, y);
        if (y !== 0) {
            ctx.beginPath(); ctx.moveTo(0, p.y); ctx.lineTo(canvas.width, p.y); ctx.stroke();
            let labelX = Math.min(Math.max(mathToPixel(0, 0).x + 4, 4), canvas.width - 20);
            ctx.fillText(y, labelX, p.y - 2);
        }
    }
    const center = mathToPixel(0, 0);
    ctx.strokeStyle = '#444'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(0, center.y); ctx.lineTo(canvas.width, center.y); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(center.x, 0); ctx.lineTo(center.x, canvas.height); ctx.stroke();
    ctx.fillStyle = '#000'; ctx.fillText("0", center.x + 4, center.y + 12);
}

function drawPoint(px, py, label) {
    ctx.fillStyle = '#ff4444';
    ctx.beginPath(); ctx.arc(px, py, 5, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#000'; ctx.font = 'bold 11px Arial';
    ctx.fillText(label, px + 8, py - 8);
}

function drawHull(hullPoints) {
    if (hullPoints.length < 2) return;
    ctx.strokeStyle = '#007bff'; ctx.lineWidth = 3;
    ctx.beginPath();
    const first = mathToPixel(hullPoints[0][0], hullPoints[0][1]);
    ctx.moveTo(first.x, first.y);
    for (let i = 1; i < hullPoints.length; i++) {
        const p = mathToPixel(hullPoints[i][0], hullPoints[i][1]);
        ctx.lineTo(p.x, p.y);
    }
    ctx.closePath(); ctx.stroke();
    ctx.fillStyle = 'rgba(0, 123, 255, 0.1)'; ctx.fill();
}

async function updateHull() {
    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ points: points.map(p => [p.x, p.y]) })
        });
        const data = await response.json();
        if (data.hull) {
            cachedHullResult = data;
            redrawAll();
            descInfo.innerText = data.description;
            const hullWithLabels = data.hull.map(hVal => {
                const originalIdx = points.findIndex(p => Math.abs(p.x - hVal[0]) < 0.001 && Math.abs(p.y - hVal[1]) < 0.001);
                const label = originalIdx !== -1 ? `[P${originalIdx + 1}]` : '';
                return { val: hVal, label: label };
            });
            coordsInfo.innerHTML = hullWithLabels.map((item, i) => `W${i+1} <b style="color:#d63384">${item.label}</b>: [ ${item.val[0].toFixed(2)}, ${item.val[1].toFixed(2)} ]`).join('<br>');
            coordsContainer.style.display = 'block';
        }
    } catch (error) { console.error(error); }
}

function resetCanvas() {
    points = []; cachedHullResult = null;
    View.scale = 3.0; View.offsetX = canvas.width / 2; View.offsetY = canvas.height / 2;
    drawGrid();
    statusInfo.innerText = "Wprowadź punkty (0/4)";
    statusInfo.style.color = "#555";
    descInfo.innerText = "";
    coordsContainer.style.display = 'none';
    updateInputsFromPoints();
}

document.addEventListener('keydown', (e) => { if (e.key === 'r') resetCanvas(); });
createInputs(); drawGrid();