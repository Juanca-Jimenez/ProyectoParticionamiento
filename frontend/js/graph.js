// Paleta de colores para las particiones
const partitionColors = [
  "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
  "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B88B", "#52C0A1"
];

function drawGraphCanvas(matrix, container, assignment = null) {
  const n = matrix.length;
  const canvas = document.createElement('canvas');
  canvas.width = 600;
  canvas.height = 400;
  container.appendChild(canvas);
  
  const ctx = canvas.getContext('2d');
  const radius = 30;
  const center_x = canvas.width / 2;
  const center_y = canvas.height / 2;
  const nodeRadius = Math.min(canvas.width, canvas.height) / 2.5;
  
  // Calcular posiciones de los nodos en círculo
  const positions = [];
  for (let i = 0; i < n; i++) {
    const angle = (i / n) * 2 * Math.PI;
    positions.push({
      x: center_x + Math.cos(angle) * nodeRadius,
      y: center_y + Math.sin(angle) * nodeRadius
    });
  }
  
  // Dibujar aristas
  ctx.strokeStyle = '#999';
  ctx.lineWidth = 2;
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      if (matrix[i][j] > 0 || matrix[j][i] > 0) {
        const weight = Math.max(matrix[i][j], matrix[j][i]);
        
        // Determinar si es una arista cortada
        let isCut = false;
        if (assignment && assignment[i] !== assignment[j]) {
          isCut = true;
        }
        
        ctx.strokeStyle = isCut ? '#FF0000' : '#999';
        ctx.lineWidth = isCut ? 3 : 1;
        ctx.setLineDash(isCut ? [5, 5] : []);
        
        ctx.beginPath();
        ctx.moveTo(positions[i].x, positions[i].y);
        ctx.lineTo(positions[j].x, positions[j].y);
        ctx.stroke();
        
        // Dibujar etiqueta de peso
        const mx = (positions[i].x + positions[j].x) / 2;
        const my = (positions[i].y + positions[j].y) / 2;
        ctx.fillStyle = '#000';
        ctx.font = '12px Arial';
        ctx.fillText(weight, mx, my - 5);
      }
    }
  }
  
  ctx.setLineDash([]);
  
  // Dibujar nodos
  for (let i = 0; i < n; i++) {
    let color = '#87CEEB';
    if (assignment) {
      color = partitionColors[assignment[i] % partitionColors.length];
    }
    
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(positions[i].x, positions[i].y, radius, 0, 2 * Math.PI);
    ctx.fill();
    
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Etiqueta del nodo
    ctx.fillStyle = '#000';
    ctx.font = 'bold 14px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`C${i}`, positions[i].x, positions[i].y);
  }
}

function renderInitialGraph(matrix) {
  console.log("renderInitialGraph called with matrix:", matrix);
  const container = document.getElementById("graph-initial");
  console.log("Container found:", container);
  if (!container) {
    console.error("Container #graph-initial not found");
    return;
  }
  
  container.innerHTML = '';
  drawGraphCanvas(matrix, container);
  document.getElementById("graph-initial-card").style.display = "block";
}

function renderPartitionedGraph(matrix, assignment, k) {
  console.log("renderPartitionedGraph called");
  const container = document.getElementById("graph-partitioned");
  if (!container) {
    console.error("Container #graph-partitioned not found");
    return;
  }
  
  container.innerHTML = '';
  drawGraphCanvas(matrix, container, assignment);
  document.getElementById("graph-partitioned-card").style.display = "block";
}
