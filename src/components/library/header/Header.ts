// src/components/library/header/Header.tsx
import { SearchBar } from './SearchBar';

export const Header = (): HTMLElement => {
  const header = document.createElement('header');
  header.className = 'header';
  
  const leftSection = document.createElement('div');
  leftSection.className = 'header-left';
  
  const rightSection = document.createElement('div');
  rightSection.className = 'header-right';
  
  // Three dot menu
  const dotsMenu = document.createElement('div');
  dotsMenu.className = 'dots-menu-container';
  
  const dotsButton = document.createElement('button');
  dotsButton.className = 'dots-menu-button';
  dotsButton.innerHTML = '⋮';
  
  const dropdown = document.createElement('div');
  dropdown.className = 'dots-dropdown';
  dropdown.innerHTML = `
    <div class="dropdown-item grid-view">
      <span class="dropdown-icon">⊞</span>
      <span>Grid view</span>
      <span class="dropdown-check">✓</span>
    </div>
    <div class="dropdown-item">
      <span class="dropdown-icon">☰</span>
      <span>List view</span>
    </div>
    <div class="dropdown-divider"></div>
    <div class="dropdown-item">
      <span class="dropdown-icon">⟲</span>
      <span>Order by update</span>
      <span class="dropdown-check">✓</span>
    </div>
    <div class="dropdown-item">
      <span class="dropdown-icon">⏰</span>
      <span>Order by upload</span>
    </div>
    <div class="dropdown-item">
      <span class="dropdown-icon">T</span>
      <span>Order by title</span>
    </div>
  `;
  
  dotsButton.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('show');
  });
  
  document.addEventListener('click', () => {
    dropdown.classList.remove('show');
  });
  
  dotsMenu.appendChild(dotsButton);
  dotsMenu.appendChild(dropdown);
  
  // Add text button
  const addButton = document.createElement('button');
  addButton.className = 'add-text-button';
  addButton.innerHTML = '<span class="plus-icon">+</span> Add text';
  
  // Search bar
  const searchBar = SearchBar();
  
  leftSection.appendChild(dotsMenu);
  leftSection.appendChild(addButton);
  rightSection.appendChild(searchBar);
  
  header.appendChild(leftSection);
  header.appendChild(rightSection);
  
  return header;
};