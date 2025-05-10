import { getDocument } from 'pdfjs-dist';

export function ThumbnailSidebar({
  pdfId,
  currentPage,
  onPageSelect,
  onClose
}: {
  pdfId: string,
  currentPage: number,
  onPageSelect: (page: number) => void,
  onClose: () => void
}): HTMLElement {
  const sidebar = document.createElement('div');
  sidebar.className = 'thumbnail-sidebar';

  // Close button
  const closeBtn = document.createElement('button');
  closeBtn.className = 'thumbnail-sidebar-close';
  closeBtn.innerHTML = '&times;';
  closeBtn.onclick = () => onClose();
  sidebar.appendChild(closeBtn);

  // Thumbnails container
  const thumbsContainer = document.createElement('div');
  thumbsContainer.className = 'thumbnail-list';
  sidebar.appendChild(thumbsContainer);

  // Load PDF and render thumbnails
  function getPdfDataById(id: string): string | null {
    const uploads = JSON.parse(localStorage.getItem('libraryUploads') || '[]');
    const found = uploads.find((u: any) => String(u.uploadedAt) === String(id));
    return found ? found.pdfData : null;
  }
  const pdfData = getPdfDataById(pdfId);
  if (!pdfData) {
    thumbsContainer.textContent = 'PDF not found.';
    return sidebar;
  }
  const base64 = pdfData.split(',')[1];
  const uint8 = Uint8Array.from(atob(base64), c => c.charCodeAt(0));

  getDocument({ data: uint8 }).promise.then(async (pdf: any) => {
    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const viewport = page.getViewport({ scale: 0.18 });
      const canvas = document.createElement('canvas');
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      const ctx = canvas.getContext('2d');
      await page.render({ canvasContext: ctx, viewport }).promise;
      canvas.className = 'thumbnail-canvas';
      if (pageNum === currentPage) {
        canvas.classList.add('active');
      }
      canvas.onclick = () => onPageSelect(pageNum);
      thumbsContainer.appendChild(canvas);
    }
  });

  return sidebar;
}
