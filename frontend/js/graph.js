// Paleta de colores para las particiones
const partitionColors = [
  "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
  "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B88B", "#52C0A1"
];

// Variable global para mantener la instancia del grafo
let initialNetwork = null;
let partitionedNetwork = null;

function renderInitialGraph(matrix) {
  console.log("renderInitialGraph called with matrix:", matrix);
  const container = document.getElementById("graph-initial");
  if (!container) {
    console.error("Container #graph-initial not found");
    return;
  }
  
  container.innerHTML = '';
  const n = matrix.length;
  const isLarge = n > 20;
  const isHuge = n > 35;
  
  // Configuración adaptativa según tamaño
  const nodeSize = isHuge ? 10 : (isLarge ? 15 : 25);
  const fontSize = isHuge ? 10 : (isLarge ? 12 : 16);
  const showLabels = !isHuge;
  
  // Calcular posiciones iniciales en círculo
  const center = { x: 0, y: 0 };
  const radius = Math.min(350, Math.max(180, n * 7));
  const positions = [];
  
  for (let i = 0; i < n; i++) {
    const angle = (i / n) * 2 * Math.PI;
    positions.push({
      x: center.x + Math.cos(angle) * radius,
      y: center.y + Math.sin(angle) * radius
    });
  }
  
  // Crear nodos con posiciones iniciales (NO fixed, para que sean movibles)
  const nodes = [];
  for (let i = 0; i < n; i++) {
    nodes.push({
      id: i,
      label: showLabels ? `${i}` : '',
      title: `Componente ${i}`,
      size: nodeSize,
      font: { size: fontSize },
      x: positions[i].x,
      y: positions[i].y,
      fixed: false,        
      physics: false       
    });
  }
  
  // Crear aristas (solo donde hay dependencia)
  let edgeCount = 0;
  const edges = [];
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const weight = matrix[i][j];
      if (weight > 0) {
        edgeCount++;
        edges.push({
          from: i,
          to: j,
          label: isHuge ? '' : weight.toString(),
          title: `Dependencia: ${weight}`,
          width: Math.min(4, Math.max(1, Math.floor(weight / 3))),
          font: { size: fontSize - 2, background: 'rgba(255,255,255,0.9)' },
          color: '#95a5a6',
          smooth: { enabled: false }  // Aristas rectas
        });
      }
    }
  }
  
  console.log(`Grafo: ${n} nodos, ${edgeCount} aristas`);
  
  const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
  
  const options = {
    nodes: {
      shape: 'circle',
      size: nodeSize,
      font: { size: fontSize, face: 'arial' },
      borderWidth: 2,
      color: {
        background: '#87CEEB',
        border: '#2c3e50',
        highlight: {
          background: '#FFA07A',
          border: '#e74c3c'
        }
      },
      fixed: false,       
      physics: false    
    },
    edges: {
      arrows: { to: { enabled: false } },
      smooth: { enabled: false },  // Aristas rectas
      font: { size: fontSize - 2, align: 'middle', background: 'white' },
      color: '#95a5a6',
      width: 1.5
    },
    physics: {
      enabled: false      
    },
    interaction: {
      zoomView: true,
      dragView: true,
      dragNodes: true,    
      tooltipDelay: 100,
      navigationButtons: true
    },
    manipulation: {
      enabled: false
    }
  };
  
  // Destruir instancia anterior si existe
  if (initialNetwork) {
    initialNetwork.destroy();
  }
  
  initialNetwork = new vis.Network(container, data, options);
  
  // Ajustar vista inicial
  setTimeout(() => {
    if (initialNetwork) {
      initialNetwork.fit({ animation: true, padding: 40 });
    }
  }, 100);
  
  // Mostrar el card y añadir información
  const card = document.getElementById("graph-initial-card");
  if (card) {
    card.style.display = "block";
    
    let infoBar = document.getElementById("graph-initial-info");
    if (!infoBar) {
      infoBar = document.createElement("div");
      infoBar.id = "graph-initial-info";
      infoBar.style.cssText = "margin-top: 10px; padding: 8px; background: #f0f0f0; border-radius: 4px; font-size: 12px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center;";
      card.appendChild(infoBar);
    }
    
    infoBar.innerHTML = `
      <span><strong>${n}</strong> componentes</span>
      <span><strong>${edgeCount}</strong> dependencias</span>
      <span>Densidad: ${((2 * edgeCount) / (n * (n - 1)) * 100).toFixed(1)}%</span>
      <span><strong>Nodos movibles</strong> - Arrastra cualquier nodo</span>
      <span>Rueda para zoom | Click + arrastre para mover canvas</span>
      <button id="reset-view-btn" style="margin-left: auto; padding: 4px 12px; cursor: pointer; border-radius: 4px; border: 1px solid #ccc;">Centrar todo</button>
      <button id="reset-layout-btn" style="padding: 4px 12px; cursor: pointer; border-radius: 4px; border: 1px solid #ccc;"> Reiniciar posiciones</button>
    `;
    
    // Botón para centrar la vista
    const resetViewBtn = document.getElementById("reset-view-btn");
    if (resetViewBtn) {
      resetViewBtn.onclick = () => {
        if (initialNetwork) {
          initialNetwork.fit({ animation: true, padding: 40 });
        }
      };
    }
    
    // Botón para resetear posiciones al círculo original
    const resetLayoutBtn = document.getElementById("reset-layout-btn");
    if (resetLayoutBtn) {
      resetLayoutBtn.onclick = () => {
        if (initialNetwork) {
          const newRadius = Math.min(350, Math.max(180, n * 7));
          for (let i = 0; i < n; i++) {
            const angle = (i / n) * 2 * Math.PI;
            const newX = center.x + Math.cos(angle) * newRadius;
            const newY = center.y + Math.sin(angle) * newRadius;
            initialNetwork.body.data.nodes.update({ id: i, x: newX, y: newY });
          }
          initialNetwork.fit({ animation: true, padding: 40 });
        }
      };
    }
  }
}

function renderPartitionedGraph(matrix, assignment, k) {
  console.log("renderPartitionedGraph called");
  const container = document.getElementById("graph-partitioned");
  if (!container) {
    console.error("Container #graph-partitioned not found");
    return;
  }
  
  container.innerHTML = '';
  const n = matrix.length;
  const isLarge = n > 20;
  const isHuge = n > 35;
  
  // Configuración adaptativa
  const nodeSize = isHuge ? 10 : (isLarge ? 15 : 25);
  const fontSize = isHuge ? 10 : (isLarge ? 12 : 16);
  const showLabels = !isHuge;
  
  // Calcular posiciones iniciales en círculo
  const center = { x: 0, y: 0 };
  const radius = Math.min(350, Math.max(180, n * 7));
  const positions = [];
  
  for (let i = 0; i < n; i++) {
    const angle = (i / n) * 2 * Math.PI;
    positions.push({
      x: center.x + Math.cos(angle) * radius,
      y: center.y + Math.sin(angle) * radius
    });
  }
  
  // Crear nodos con colores según partición
  const nodes = [];
  for (let i = 0; i < n; i++) {
    const partitionId = assignment[i] || 0;
    const color = partitionColors[partitionId % partitionColors.length];
    
    nodes.push({
      id: i,
      label: showLabels ? `${i}` : '',
      title: `Componente ${i} - Partición ${partitionId}`,
      size: nodeSize,
      font: { size: fontSize },
      x: positions[i].x,
      y: positions[i].y,
      fixed: false,       
      physics: false,     
      color: {
        background: color,
        border: '#2c3e50',
        highlight: {
          background: color,
          border: '#e74c3c'
        }
      }
    });
  }
  
  // Crear aristas (diferenciando aristas internas y cortadas)
  let edgeCount = 0;
  let cutEdges = 0;
  const edges = [];
  
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const weight = matrix[i][j];
      if (weight > 0) {
        edgeCount++;
        const isCut = assignment[i] !== assignment[j];
        if (isCut) cutEdges++;
        
        edges.push({
          from: i,
          to: j,
          label: isHuge ? '' : weight.toString(),
          title: `Dependencia: ${weight} ${isCut ? ' [ENTRE PARTES]' : ''}`,
          width: isCut ? 3 : 1.5,
          color: isCut ? '#e74c3c' : '#95a5a6',
          dashes: isCut,
          font: { size: fontSize - 2, align: 'middle', background: 'white' },
          smooth: { enabled: false }
        });
      }
    }
  }
  
  console.log(`Grafo particionado: ${n} nodos, ${edgeCount} aristas, ${cutEdges} aristas entre partes`);
  
  const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
  
  const options = {
    nodes: {
      shape: 'circle',
      size: nodeSize,
      font: { size: fontSize, face: 'arial' },
      borderWidth: 2,
      fixed: false,       
      physics: false      
    },
    edges: {
      arrows: { to: { enabled: false } },
      smooth: { enabled: false },
      font: { size: fontSize - 2, align: 'middle', background: 'white' }
    },
    physics: {
      enabled: false      
    },
    interaction: {
      zoomView: true,
      dragView: true,
      dragNodes: true,  
      tooltipDelay: 100,
      navigationButtons: true
    }
  };
  
  if (partitionedNetwork) {
    partitionedNetwork.destroy();
  }
  
  partitionedNetwork = new vis.Network(container, data, options);
  
  setTimeout(() => {
    if (partitionedNetwork) {
      partitionedNetwork.fit({ animation: true, padding: 40 });
    }
  }, 100);
  
  // Mostrar el card y añadir info
  const card = document.getElementById("graph-partitioned-card");
  if (card) {
    card.style.display = "block";
    
    let infoBar = document.getElementById("graph-partitioned-info");
    if (!infoBar) {
      infoBar = document.createElement("div");
      infoBar.id = "graph-partitioned-info";
      infoBar.style.cssText = "margin-top: 10px; padding: 8px; background: #f0f0f0; border-radius: 4px; font-size: 12px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center;";
      card.appendChild(infoBar);
    }
    
    infoBar.innerHTML = `
      <span><strong>${n}</strong> componentes</span>
      <span><strong>${edgeCount}</strong> dependencias</span>
      <span><strong style="color: #e74c3c;">${cutEdges}</strong> dependencias entre partes</span>
      <span><strong>${k}</strong> particiones</span>
      <span>Rojo = dependencia entre distintas particiones</span>
      <span><strong>Nodos movibles</strong></span>
      <button id="reset-partition-view-btn" style="margin-left: auto; padding: 4px 12px; cursor: pointer; border-radius: 4px; border: 1px solid #ccc;">Centrar</button>
      <button id="reset-partition-layout-btn" style="padding: 4px 12px; cursor: pointer; border-radius: 4px; border: 1px solid #ccc;">Reiniciar posiciones</button>
    `;
    
    // Botón para centrar la vista
    const resetViewBtn = document.getElementById("reset-partition-view-btn");
    if (resetViewBtn) {
      resetViewBtn.onclick = () => {
        if (partitionedNetwork) {
          partitionedNetwork.fit({ animation: true, padding: 40 });
        }
      };
    }
    
    // Botón para resetear posiciones al círculo original
    const resetLayoutBtn = document.getElementById("reset-partition-layout-btn");
    if (resetLayoutBtn) {
      resetLayoutBtn.onclick = () => {
        if (partitionedNetwork) {
          const newRadius = Math.min(350, Math.max(180, n * 7));
          for (let i = 0; i < n; i++) {
            const angle = (i / n) * 2 * Math.PI;
            const newX = center.x + Math.cos(angle) * newRadius;
            const newY = center.y + Math.sin(angle) * newRadius;
            partitionedNetwork.body.data.nodes.update({ id: i, x: newX, y: newY });
          }
          partitionedNetwork.fit({ animation: true, padding: 40 });
        }
      };
    }
  }
}