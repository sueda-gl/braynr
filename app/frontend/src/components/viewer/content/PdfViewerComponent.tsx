import React, { useEffect, useRef } from 'react';
import { PdfViewer } from './PdfViewer'; // The original vanilla TS function

interface PdfViewerComponentProps {
  pdfId: string; // Or however you identify the PDF, e.g., file URL, base64 data
  onScreenshot?: (dataUrl: string) => void;
  // Add any other options your PdfViewer might need as props
}

export const PdfViewerComponent: React.FC<PdfViewerComponentProps> = ({ 
  pdfId, 
  onScreenshot 
}) => {
  const viewerContainerRef = useRef<HTMLDivElement>(null);
  // Optional: if your PdfViewer returns an instance with a cleanup method
  // const viewerInstanceRef = useRef<any>(null); 

  useEffect(() => {
    let viewerElement: HTMLElement | null = null;
    if (viewerContainerRef.current) {
      // Clear previous viewer if any, before mounting new one
      viewerContainerRef.current.innerHTML = '';
      
      // Call the original PdfViewer function
      // It might return an HTMLElement or an object with an element and a destroy method
      const returnedFromPdfViewer = PdfViewer(pdfId, { 
        onScreenshot 
        // Pass other opts if your PdfViewer expects them
      });

      // Assuming PdfViewer returns the HTMLElement to be appended
      if (returnedFromPdfViewer instanceof HTMLElement) {
        viewerElement = returnedFromPdfViewer;
        viewerContainerRef.current.appendChild(viewerElement);
      } else {
        // Handle other return types if necessary, e.g., if it returns an object
        // with an element and a destroy method.
        // For example: viewerInstanceRef.current = returnedFromPdfViewer;
        // if (returnedFromPdfViewer && returnedFromPdfViewer.element) {
        //   viewerContainerRef.current.appendChild(returnedFromPdfViewer.element);
        // }
        console.warn("PdfViewer function did not return an HTMLElement directly.")
      }
    }

    return () => {
      // Cleanup logic when the component unmounts or pdfId/opts change
      if (viewerContainerRef.current) {
        viewerContainerRef.current.innerHTML = ''; // Simple cleanup
      }
      // If your PdfViewer had a specific destroy method:
      // if (viewerInstanceRef.current && typeof viewerInstanceRef.current.destroy === 'function') {
      //   viewerInstanceRef.current.destroy();
      // }
      // viewerInstanceRef.current = null;
    };
  }, [pdfId, onScreenshot]); // Re-run if pdfId or callbacks change

  return <div ref={viewerContainerRef} style={{ width: '100%', height: '100%' }} className="pdf-viewer-react-container"></div>;
}; 