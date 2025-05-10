// Add a style element to the container to enable text selection
const style = document.createElement('style');
style.textContent = `
  .pdf-page canvas {
    pointer-events: none;
  }
`;
document.head.appendChild(style); 