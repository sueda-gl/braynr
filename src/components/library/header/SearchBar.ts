export const SearchBar = (): HTMLElement => {
    const container = document.createElement('div');
    container.className = 'search-bar-container';
    
    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Search library...';
    input.className = 'search-input';
    
    container.appendChild(input);
    
    return container;
  };