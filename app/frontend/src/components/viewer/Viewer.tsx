import { ViewerHeader } from './header/ViewerHeader';
import { PdfViewer } from './content/PdfViewer';
import { ThumbnailSidebar } from './content/ThumbnailSidebar';
import { GeneratedContentsSidebar } from './sidebars/GeneratedContentsSidebar';
import './header/ViewerHeader.css';
import './Viewer.css';
import './content/ThumbnailSidebar.css';

export function Viewer(id: string): HTMLElement {
  const container = document.createElement('div');
  container.className = 'viewer-root';

  // State for sidebar open/closed and current page
  let sidebarOpen = true;
  let rightSidebarOpen = false;
  let currentPage = 1;

  // Header with toggle logic for right sidebar
  const header = ViewerHeader({
    onToggleSidebar: () => {
      sidebarOpen = !sidebarOpen;
      updateSidebar();
    },
    onToggleRightSidebar: () => {
      rightSidebarOpen = !rightSidebarOpen;
      updateRightSidebar();
    }
  });
  container.appendChild(header);

  // Main content area
  const main = document.createElement('div');
  main.className = 'viewer-main';

  // Left sidebar (thumbnails)
  let leftSidebar: HTMLElement | null = null;
  let openSidebarBtn: HTMLElement | null = null;

  // PDF viewer
  const pdfViewer = PdfViewer(id, {
    onPageChange: (page: number) => {
      currentPage = page;
      setActiveThumbnail(page);
    },
    scrollToPage: (page: number) => {
      // Scroll to the selected page's canvas
      const canvases = pdfViewer.querySelectorAll('canvas');
      if (canvases[page - 1]) {
        canvases[page - 1].scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  });
  main.appendChild(pdfViewer);

  // Right sidebar (generated contents)
  const rightSidebar = GeneratedContentsSidebar();
  rightSidebar.classList.add('generated-contents-sidebar');
  main.appendChild(rightSidebar);

  // Track which sidebars have listeners
  const sidebarListeners = new WeakSet<HTMLElement>();
  const rightSidebarListeners = new WeakSet<HTMLElement>();

  function setActiveThumbnail(pageNum: number) {
    if (leftSidebar) {
      const thumbs = leftSidebar.querySelectorAll('.thumbnail-canvas');
      thumbs.forEach((thumb, idx) => {
        thumb.classList.toggle('active', idx === pageNum - 1);
      });
    }
  }

  function updateSidebar() {
    // Only create the sidebar once
    if (!leftSidebar) {
      leftSidebar = ThumbnailSidebar({
        pdfId: id,
        currentPage,
        onPageSelect: (page: number) => {
          currentPage = page;
          setActiveThumbnail(page);
          // Scroll to the selected page
          const canvases = pdfViewer.querySelectorAll('canvas');
          if (canvases[page - 1]) {
            canvases[page - 1].scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        },
        onClose: () => {
          sidebarOpen = false;
          updateSidebar();
        }
      });
      main.insertBefore(leftSidebar, pdfViewer);
      setTimeout(() => setActiveThumbnail(currentPage), 0);
    }
    // Add transitionend listener only once
    if (leftSidebar && !sidebarListeners.has(leftSidebar)) {
      leftSidebar.addEventListener('transitionend', (e: TransitionEvent) => {
        if (e.propertyName === 'transform') {
          if (leftSidebar && leftSidebar.classList.contains('closed')) {
            leftSidebar.style.width = '0';
            leftSidebar.style.minWidth = '0';
          } else if (leftSidebar) {
            leftSidebar.style.width = '';
            leftSidebar.style.minWidth = '';
          }
        }
      });
      sidebarListeners.add(leftSidebar);
    }
    // Show/hide with animation
    if (sidebarOpen) {
      if (leftSidebar) {
        leftSidebar.style.width = '';
        leftSidebar.style.minWidth = '';
        leftSidebar.classList.remove('closed');
      }
      if (openSidebarBtn) {
        openSidebarBtn.remove();
        openSidebarBtn = null;
      }
    } else {
      if (leftSidebar) leftSidebar.classList.add('closed');
      if (openSidebarBtn) openSidebarBtn.remove();
      openSidebarBtn = document.createElement('button');
      openSidebarBtn.className = 'thumbnail-sidebar-open-btn';
      openSidebarBtn.innerHTML = '<svg width="24" height="24" fill="none" stroke="#a259ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M4 12h16M4 12l6-6M4 12l6 6"/></svg>';
      openSidebarBtn.onclick = () => {
        sidebarOpen = true;
        updateSidebar();
      };
      main.insertBefore(openSidebarBtn, pdfViewer);
    }
  }

  function updateRightSidebar() {
    // Add transitionend listener only once
    if (rightSidebar && !rightSidebarListeners.has(rightSidebar)) {
      rightSidebar.addEventListener('transitionend', (e: TransitionEvent) => {
        if (e.propertyName === 'transform') {
          if (rightSidebar.classList.contains('closed')) {
            rightSidebar.style.width = '0';
            rightSidebar.style.minWidth = '0';
          } else {
            rightSidebar.style.width = '';
            rightSidebar.style.minWidth = '';
          }
        }
      });
      rightSidebarListeners.add(rightSidebar);
    }
    // Fix: On initial render, if closed, set width to 0
    if (!rightSidebarOpen) {
      rightSidebar.style.width = '0';
      rightSidebar.style.minWidth = '0';
    }
    if (rightSidebarOpen) {
      rightSidebar.style.width = '';
      rightSidebar.style.minWidth = '';
      rightSidebar.classList.remove('closed');
    } else {
      rightSidebar.classList.add('closed');
      // width will be set to 0 after transition
    }
  }

  // Initial render
  updateSidebar();
  updateRightSidebar();

  container.appendChild(main);
  return container;
}
