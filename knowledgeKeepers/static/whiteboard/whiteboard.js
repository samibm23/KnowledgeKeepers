const canvas = document.getElementById('whiteboard');
const context = canvas.getContext('2d');
const formData = new FormData();



let isDrawing = false;
let lastX = 0;
let lastY = 0;
let lineWidth = 20; // default line width

function startDrawing(e) {
  isDrawing = true;
  lastX = e.offsetX;
  lastY = e.offsetY;
}

function draw(e) {
  if (!isDrawing) return;
  context.beginPath();
  context.moveTo(lastX, lastY);
  context.lineTo(e.offsetX, e.offsetY);
  context.lineWidth = lineWidth;
  context.lineCap = 'round';
  context.stroke();
  lastX = e.offsetX;
  lastY = e.offsetY;
}

function stopDrawing() {
  isDrawing = false;
}


canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);
