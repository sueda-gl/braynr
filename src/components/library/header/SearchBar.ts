export const SearchBar = (): HTMLElement => {
    const container = document.createElement('div');
    container.className = 'search-bar-container';
    
    const searchIcon = document.createElement('span');
    searchIcon.className = 'search-icon';
    searchIcon.innerHTML = '🔍';
    
    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Search library...';
    input.className = 'search-input';
    
    container.appendChild(searchIcon);
    container.appendChild(input);
    
    return container;
  };