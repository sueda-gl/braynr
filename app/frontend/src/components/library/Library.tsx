import React, { useState, useCallback } from 'react';
import { Sidebar } from './sidebar/Sidebar';
import { Header } from './header/Header';
import { LibraryContent } from './content/LibraryContent.tsx';
import { UploadDetailPopUp } from './header/UploadDetailPopUp.tsx';
import type { UploadFormData } from './header/UploadDetailPopUp.tsx';

export interface StoredUpload extends UploadFormData {
  pdfData: string | ArrayBuffer | null;
  fileName: string;
  uploadedAt: number;
}

export const Library: React.FC = () => {
  const [activeSection, setActiveSection] = useState<string>('library');
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [modalFile, setModalFile] = useState<File | null>(null);
  // We need a way to trigger re-renders in LibraryContent when uploads change
  const [uploads, setUploads] = useState<StoredUpload[]>(() => {
    const savedUploads = localStorage.getItem('libraryUploads');
    return savedUploads ? JSON.parse(savedUploads) : [];
  });

  const handleShowModal = useCallback((file: File) => {
    setModalFile(file);
    setIsModalOpen(true);
  }, []);

  const handleModalSubmit = useCallback((data: UploadFormData) => {
    if (modalFile) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const pdfData = e.target?.result ?? null;
        const newUpload: StoredUpload = {
          ...data,
          pdfData,
          fileName: modalFile.name,
          uploadedAt: Date.now(),
        };
        setUploads(prevUploads => {
          const updatedUploads = [...prevUploads, newUpload];
          localStorage.setItem('libraryUploads', JSON.stringify(updatedUploads));
          return updatedUploads;
        });
        setIsModalOpen(false);
        setModalFile(null);
      };
      reader.readAsDataURL(modalFile);
    }
  }, [modalFile]);

  const handleModalCancel = useCallback(() => {
    setIsModalOpen(false);
    setModalFile(null);
  }, []);

  const handleSectionChange = useCallback((section: string) => {
    setActiveSection(section);
  }, []);

  return (
    <div className='library-container'>
      <Sidebar activeSection={activeSection} onSectionChange={handleSectionChange} />
      <div className='main-content'>
        <Header onShowModal={handleShowModal} />
        {/* Pass uploads or a key to LibraryContent if it needs to re-render on new uploads */}
        <LibraryContent activeSection={activeSection} uploads={uploads} />
      </div>
      {isModalOpen && modalFile && (
        <UploadDetailPopUp
          fileName={modalFile.name}
          onSubmit={handleModalSubmit}
          onCancel={handleModalCancel}
        />
      )}
    </div>
  );
};