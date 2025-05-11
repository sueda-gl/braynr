import React, { useState, useEffect, useRef } from 'react';
import { ViewerHeader as ViewerHeader_vanilla } from './header/ViewerHeader';
import { PdfViewer as PdfViewer_vanilla } from './content/PdfViewer';
import { ThumbnailSidebar as ThumbnailSidebar_vanilla } from './content/ThumbnailSidebar';
import { GeneratedContentsSidebar } from './sidebars/GeneratedContentsSidebar'; 

import './header/ViewerHeader.css';
import './Viewer.css';
import './content/ThumbnailSidebar.css';

// Props for vanilla components (simplified)
interface VanillaComponentProps {
  onToggleSidebar?: () => void;
  onToggleRightSidebar?: () => void;
  onPageChange?: (page: number) => void;
  onScreenshot?: (img: string) => void;
  pdfId?: string;
  id?: string; // for PdfViewer
  currentPage?: number;
  onPageSelect?: (page: number) => void;
  onClose?: () => void;
  // Add scrollToPage if its signature is known and needed for PdfViewer opts
}

export const Viewer: React.FC<{ id: string }> = ({ id }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [screenshot, setScreenshot] = useState<string | null>(null);

  const headerContainerRef = useRef<HTMLDivElement>(null);
  const pdfViewerContainerRef = useRef<HTMLDivElement>(null);
  const leftSidebarContainerRef = useRef<HTMLDivElement>(null);
  const openSidebarButtonRef = useRef<HTMLButtonElement>(null);

  // Mount ViewerHeader
  useEffect(() => {
    if (headerContainerRef.current) {
      const headerElement = ViewerHeader_vanilla({
        onToggleSidebar: () => setSidebarOpen(prev => !prev),
        onToggleRightSidebar: () => setRightSidebarOpen(prev => !prev)
      });
      headerContainerRef.current.innerHTML = ''; 
      headerContainerRef.current.appendChild(headerElement);
    }
  }, []); 

  // Mount and manage PdfViewer
  useEffect(() => {
    if (pdfViewerContainerRef.current) {
      const pdfViewerElement = PdfViewer_vanilla(id, {
        onPageChange: (page: number) => setCurrentPage(page),
        onScreenshot: (img: string) => setScreenshot(img)
        // scrollToPage: (page: number) => { /* original scroll logic for canvases in pdfViewerElement */ }
      });
      pdfViewerContainerRef.current.innerHTML = '';
      pdfViewerContainerRef.current.appendChild(pdfViewerElement);
    }
  }, [id]); 

  // Mount and manage ThumbnailSidebar (left sidebar)
  useEffect(() => {
    if (leftSidebarContainerRef.current) {
      if (sidebarOpen) {
        const thumbnailSidebarElement = ThumbnailSidebar_vanilla({
          pdfId: id,
          currentPage: currentPage,
          onPageSelect: (page: number) => {
            setCurrentPage(page);
            // TODO: Implement setActiveThumbnail or direct scroll if PdfViewer instance needed
            // const canvases = pdfViewerContainerRef.current?.querySelector('.pdf-viewer-container canvas'); // This needs to target canvases inside the PdfViewer rendered content
            // if (canvases && canvases[page - 1]) { ... }
          },
          onClose: () => setSidebarOpen(false)
        });
        leftSidebarContainerRef.current.innerHTML = '';
        leftSidebarContainerRef.current.appendChild(thumbnailSidebarElement);
        leftSidebarContainerRef.current.classList.remove('closed');
        if (openSidebarButtonRef.current) openSidebarButtonRef.current.style.display = 'none';
      } else {
        leftSidebarContainerRef.current.innerHTML = ''; // Clear content when closed
        leftSidebarContainerRef.current.classList.add('closed');
        if (openSidebarButtonRef.current) openSidebarButtonRef.current.style.display = 'flex';
      }
    }
  }, [sidebarOpen, id, currentPage]);

  // Active thumbnail logic - needs to be adapted as PdfViewer is a black box here
  // The original setActiveThumbnail manipulated DOM inside pdfViewer and leftSidebar directly.
  // This is harder when vanilla components are simply mounted.
  // For now, this part is simplified.

  return (
    <div className="viewer-root">
      <div ref={headerContainerRef} className="viewer-header-container"></div>
      <div className={`viewer-main ${!sidebarOpen ? 'left-sidebar-closed' : ''} ${rightSidebarOpen ? 'right-sidebar-open-class' : ''}`}>
        
        <div ref={leftSidebarContainerRef} className={`thumbnail-sidebar-wrapper ${!sidebarOpen ? 'closed' : ''}`}></div>
        {!sidebarOpen && (
            <button 
                ref={openSidebarButtonRef}
                className="thumbnail-sidebar-open-btn" 
                onClick={() => setSidebarOpen(true)} 
            >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
            </button>
        )}

        <div ref={pdfViewerContainerRef} className="pdf-viewer-wrapper"></div>
        
        <div className={`generated-contents-sidebar-wrapper ${!rightSidebarOpen ? 'closed' : 'open'}`}>
          {/* Render GeneratedContentsSidebar only when it should be open */}
          {/* The visibility/animation is handled by CSS based on parent's class */}
          {rightSidebarOpen && (
            <GeneratedContentsSidebar
              initialScreenshot={screenshot} // Pass the current screenshot state
              onClearScreenshot={() => setScreenshot(null)} // Allow sidebar to clear Viewer's screenshot state
            />
          )}
        </div>
      </div>
    </div>
  );
};
