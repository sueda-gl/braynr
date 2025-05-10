import { getDocument, GlobalWorkerOptions } from 'pdfjs-dist';
import { TextLayerBuilder } from 'pdfjs-dist/web/pdf_viewer';
import 'pdfjs-dist/web/pdf_viewer.css';

GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

function base64ToUint8Array(base64: string) {
  return Uint8Array.from(atob(base64), c => c.charCodeAt(0));
}

export function PdfViewer(
  id: string,
  opts?: {
    onPageChange?: (page: number) => void;
    scrollToPage?: (page: number) => void;
    onScreenshot?: (dataUrl: string) => void;
  }
): HTMLElement {
  const container = document.createElement('div');
  container.className = 'pdf-viewer';

  // Show loading message
  const loading = document.createElement('div');
  loading.textContent = 'Loading PDF...';
  container.appendChild(loading);

  // Inline: get PDF data from localStorage by id
  function getPdfDataById(id: string): string | null {
    const uploads = JSON.parse(localStorage.getItem('libraryUploads') || '[]');
    const found = uploads.find((u: any) => String(u.uploadedAt) === String(id));
    return found ? found.pdfData : null;
  }
  const pdfData = getPdfDataById(id);
  if (!pdfData) {
    loading.textContent = 'PDF not found.';
    return container;
  }

  // Convert base64 to Uint8Array
  const base64 = pdfData.split(',')[1];
  const uint8 = base64ToUint8Array(base64);

  // Screenshot selection state
  let selection = null;
  let selectionRect: HTMLDivElement | null = null;
  let startX = 0, startY = 0, endX = 0, endY = 0;
  let screenshotCanvas = null;
  let currentScreenshot = null;

  function clearSelectionRect() {
    if (selectionRect && selectionRect.parentNode) selectionRect.parentNode.removeChild(selectionRect);
    selectionRect = null;
  }

  function setupScreenshotTool(canvas: HTMLCanvasElement, pageContainer: HTMLDivElement) {
    canvas.style.cursor = 'crosshair';
    canvas.addEventListener('mousedown', (e: MouseEvent) => {
      console.log('mousedown');
      if (e.button !== 0) return;
      const rect = canvas.getBoundingClientRect();
      startX = e.clientX - rect.left;
      startY = e.clientY - rect.top;
      endX = startX;
      endY = startY;
      clearSelectionRect();
      selectionRect = document.createElement('div');
      selectionRect.style.position = 'absolute';
      selectionRect.style.border = '2px solid #a259ff';
      selectionRect.style.background = 'rgba(162,89,255,0.1)';
      selectionRect.style.pointerEvents = 'none';
      selectionRect.style.zIndex = '10';
      pageContainer.appendChild(selectionRect);
      function onMouseMove(ev: MouseEvent) {
        console.log('mousemove');
        endX = ev.clientX - rect.left;
        endY = ev.clientY - rect.top;
        const x = Math.min(startX, endX);
        const y = Math.min(startY, endY);
        const w = Math.abs(endX - startX);
        const h = Math.abs(endY - startY);
        if (selectionRect) {
          selectionRect.style.left = x + 'px';
          selectionRect.style.top = y + 'px';
          selectionRect.style.width = w + 'px';
          selectionRect.style.height = h + 'px';
        }
      }
      function onMouseUp(ev: MouseEvent) {
        console.log('mouseup');
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
        endX = ev.clientX - rect.left;
        endY = ev.clientY - rect.top;
        const x = Math.round(Math.min(startX, endX));
        const y = Math.round(Math.min(startY, endY));
        const w = Math.round(Math.abs(endX - startX));
        const h = Math.round(Math.abs(endY - startY));
        if (w > 5 && h > 5) {
          // Capture screenshot
          const tempCanvas = document.createElement('canvas');
          tempCanvas.width = w;
          tempCanvas.height = h;
          const tempCtx = tempCanvas.getContext('2d');
          if (tempCtx) {
            tempCtx.drawImage(canvas, x, y, w, h, 0, 0, w, h);
            const dataUrl = tempCanvas.toDataURL('image/png');
            console.log('Screenshot captured:', dataUrl);
            currentScreenshot = dataUrl;
            if (opts && typeof opts.onScreenshot === 'function') {
              opts.onScreenshot(dataUrl);
            }
          }
        }
        clearSelectionRect();
      }
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    });
  }

  // Render PDF using PDF.js
  getDocument({ data: uint8 }).promise.then(async (pdf: any) => {
    loading.remove();
    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const viewport = page.getViewport({ scale: 1.2 });
      const canvas = document.createElement('canvas');
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      const ctx = canvas.getContext('2d');
      await page.render({ canvasContext: ctx, viewport }).promise;
      const pageContainer = document.createElement('div');
      pageContainer.style.position = 'relative';
      pageContainer.appendChild(canvas);
      setupScreenshotTool(canvas, pageContainer);

      container.appendChild(pageContainer);

      // Optionally, notify onPageChange when a page is rendered (for future use)
      // if (opts?.onPageChange) opts.onPageChange(pageNum);
    }
  }).catch((err: any) => {
    console.error('PDF.js error:', err);
    loading.textContent = 'Failed to load PDF.';
  });

  // Optionally, expose scrollToPage for external navigation (already handled in parent)

  return container;
}
