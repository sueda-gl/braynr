import { Sidebar } from './sidebar/Sidebar';
import { Header } from './header/Header';
import { LibraryContent } from './content/LibraryContent';
import { UploadDetailPopUp } from './header/UploadDetailPopUp';

export const Library = (): HTMLElement => {
  let activeSection = 'library';
  let modal: HTMLElement | null = null;
  
  const container = document.createElement('div');
  container.className = 'library-container';
  
  const mainContent = document.createElement('div');
  mainContent.className = 'main-content';
  
  function showModal(file: File) {
    // Show the upload detail popup
    modal = UploadDetailPopUp({
      fileName: file.name,
      onSubmit: (data) => {
        // Read file as data URL for storage
        const reader = new FileReader();
        reader.onload = function (e) {
          const pdfData = e.target?.result;
          // Save to localStorage
          const stored = JSON.parse(localStorage.getItem('libraryUploads') || '[]');
          stored.push({
            ...data,
            pdfData,
            fileName: file.name,
            uploadedAt: Date.now(),
          });
          localStorage.setItem('libraryUploads', JSON.stringify(stored));
          render();
        };
        reader.readAsDataURL(file);
      },
      onCancel: () => {
        if (modal) modal.remove();
        modal = null;
      }
    });
    document.body.appendChild(modal);
  }

  const render = () => {
    container.innerHTML = '';
    mainContent.innerHTML = '';
    
    const sidebar = Sidebar(activeSection, (section) => {
      activeSection = section;
      render();
    });
    
    const header = Header(showModal);
    const content = LibraryContent(activeSection);
    
    mainContent.appendChild(header);
    mainContent.appendChild(content);
    
    container.appendChild(sidebar);
    container.appendChild(mainContent);
  };
  
  render();
  return container;
};