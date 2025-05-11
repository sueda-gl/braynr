import React from 'react';
import type { StoredUpload } from '../Library'; // Assuming StoredUpload is in Library.tsx

interface LibraryContentProps {
  activeSection: string;
  uploads: StoredUpload[];
}

export const LibraryContent: React.FC<LibraryContentProps> = ({ activeSection, uploads }) => {
  if (activeSection === 'library') {
    return (
      <div className='library-content'>
        {uploads.length === 0 && (
          <div style={{ textAlign: 'center', marginTop: '50px', color: '#777' }}>
            <h2>Your library is empty.</h2>
            <p>Upload some PDFs to get started!</p>
          </div>
        )}
        {uploads.map((upload) => (
          <div
            key={upload.uploadedAt}
            className='pdf-card'
            onClick={() => {
              window.location.hash = `#/viewer/${upload.uploadedAt}`;
            }}
          >
            <div className='pdf-icon'>
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="48" height="48" rx="8" fill="#F5F5F5"/>
                <path d="M16 12C16 10.8954 16.8954 10 18 10H30C31.1046 10 32 10.8954 32 12V36C32 37.1046 31.1046 38 30 38H18C16.8954 38 16 37.1046 16 36V12Z" fill="#A259FF"/>
                <path d="M20 18H28V20H20V18ZM20 22H28V24H20V22ZM20 26H28V28H20V26Z" fill="white"/>
              </svg>
            </div>
            {/* You might want to display the title or other info from 'upload' here */}
            {/* e.g., <p>{upload.title}</p> */}
          </div>
        ))}
      </div>
    );
  } else if (activeSection === 'flashcards') {
    return (
      <div className='library-content' style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <h2 style={{ textAlign: 'center', marginTop: '100px' }}>
          Coming Soon!
        </h2>
      </div>
    );
  }

  return null; // Default case, should ideally not be reached if activeSection is always valid
}; 