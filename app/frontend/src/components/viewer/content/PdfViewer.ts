import { getDocument, GlobalWorkerOptions } from 'pdfjs-dist';
GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

function base64ToUint8Array(base64: string) {
  return Uint8Array.from(atob(base64), c => c.charCodeAt(0));
}

export function PdfViewer(
  id: string,
  opts?: {
    onPageChange?: (page: number) => void;
    scrollToPage?: (page: number) => void;
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

  // Debug logs
  // console.log('pdfData:', pdfData.slice(0, 100));
  // console.log('base64:', base64.slice(0, 100));
  // console.log('uint8 length:', uint8.length);

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
      container.appendChild(canvas);
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
