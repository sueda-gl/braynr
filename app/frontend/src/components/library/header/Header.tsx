import React, { useState, useEffect, useRef } from 'react';
import { SearchBar } from './SearchBar'; // Imports the new SearchBar.tsx

interface HeaderProps {
  onShowModal?: (file: File) => void; // Changed from onAddPdf based on Library.tsx usage
}

export const Header: React.FC<HeaderProps> = ({ onShowModal }) => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const toggleDropdown = (e: React.MouseEvent) => {
    e.stopPropagation();
    setDropdownOpen(!dropdownOpen);
  };

  const handleAddTextClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files && event.target.files[0];
    if (file && onShowModal) {
      onShowModal(file);
      if (fileInputRef.current) {
        fileInputRef.current.value = ''; // Reset file input
      }
    }
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);

  return (
    <header className="header">
      <div className="header-left">
        <div className="dots-menu-container" ref={dropdownRef}>
          <button className="dots-menu-button" onClick={toggleDropdown}>
            <span className="dot vertical-dot"></span>
            <span className="dot vertical-dot"></span>
            <span className="dot vertical-dot"></span>
          </button>
          {dropdownOpen && (
            <div className="dots-dropdown show"> {/* 'show' class managed by conditional rendering */}
              <div className="dropdown-item grid-view">
                <span className="dropdown-icon">⊞</span>
                <span>Grid view</span>
                <span className="dropdown-check">✓</span>
              </div>
              <div className="dropdown-item">
                <span className="dropdown-icon">☰</span>
                <span>List view</span>
              </div>
              <div className="dropdown-divider"></div>
              <div className="dropdown-item">
                <span className="dropdown-icon">⟲</span>
                <span>Order by update</span>
                <span className="dropdown-check">✓</span>
              </div>
              <div className="dropdown-item">
                <span className="dropdown-icon">⏰</span>
                <span>Order by upload</span>
              </div>
              <div className="dropdown-item">
                <span className="dropdown-icon">T</span>
                <span>Order by title</span>
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="header-center">
        <button className="add-text-button" onClick={handleAddTextClick}>
          <span className="plus-icon">+</span> Add text
        </button>
        <input
          type="file"
          accept="application/pdf"
          style={{ display: 'none' }}
          ref={fileInputRef}
          onChange={handleFileChange}
        />
      </div>
      <div className="header-right">
        <SearchBar />
      </div>
    </header>
  );
}; 