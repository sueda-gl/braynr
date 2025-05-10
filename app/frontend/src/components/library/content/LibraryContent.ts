export const LibraryContent = (activeSection: string): HTMLElement => {
  const content = document.createElement('div');
  content.className = 'library-content';
  
  if (activeSection === 'library') {
    // Load uploaded PDFs from localStorage
    const uploads = JSON.parse(localStorage.getItem('libraryUploads') || '[]');
    uploads.forEach((upload: any) => {
      const card = document.createElement('div');
      card.className = 'pdf-card';
      // PDF icon
      const icon = document.createElement('div');
      icon.className = 'pdf-icon';
      icon.innerHTML = `<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="48" height="48" rx="8" fill="#F5F5F5"/><path d="M16 12C16 10.8954 16.8954 10 18 10H30C31.1046 10 32 10.8954 32 12V36C32 37.1046 31.1046 38 30 38H18C16.8954 38 16 37.1046 16 36V12Z" fill="#A259FF"/><path d="M20 18H28V20H20V18ZM20 22H28V24H20V22ZM20 26H28V28H20V26Z" fill="white"/></svg>`;
      card.appendChild(icon);
      card.onclick = () => {
        window.location.hash = `#/viewer/${upload.uploadedAt}`;
      };
      content.appendChild(card);
    });
  } else if (activeSection === 'flashcards') {
    const message = document.createElement('h2');
    message.textContent = 'Coming Soon!';
    message.style.textAlign = 'center';
    message.style.marginTop = '100px';
    content.appendChild(message);
  }
  
  return content;
};