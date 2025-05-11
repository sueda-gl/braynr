import React from 'react';

export const SearchBar: React.FC = () => {
  return (
    <div className="search-bar-container">
      <input type="text" placeholder="Search library..." className="search-input" />
    </div>
  );
}; 