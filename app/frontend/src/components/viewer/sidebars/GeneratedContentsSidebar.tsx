import './GeneratedContentsSidebar.css';

export function GeneratedContentsSidebar(): HTMLElement {
  const sidebar = document.createElement('div');
  sidebar.className = 'generated-contents-sidebar';

  // Create the menu container
  const menu = document.createElement('div');
  menu.className = 'sidebar-menu';

  // Define menu items
  const menuItems = ['Images', 'Keywords', 'Notes', 'Mindmaps', 'Summaries', 'Video Explanations'];
  let activeItem: string | null = null;

  // Create menu buttons
  menuItems.forEach(item => {
    const button = document.createElement('button');
    button.className = 'menu-button';
    button.textContent = item;
    button.addEventListener('click', () => {
      // Remove active class from all buttons
      menu.querySelectorAll('.menu-button').forEach(btn => btn.classList.remove('active'));
      // Add active class to clicked button
      button.classList.add('active');
      activeItem = item;
      updateContent();
    });
    menu.appendChild(button);
  });

  // Create the content area
  const content = document.createElement('div');
  content.className = 'sidebar-content';

  // Function to update content based on active menu item
  function updateContent() {
    content.innerHTML = '';
    if (activeItem === 'Video Explanations') {
      const placeholder = document.createElement('div');
      placeholder.className = 'placeholder-icon';
      placeholder.innerHTML = '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#a259ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M10 8l6 4-6 4V8z"/></svg>';
      content.appendChild(placeholder);
    }
  }

  // Append menu and content to sidebar
  sidebar.appendChild(menu);
  sidebar.appendChild(content);

  // Resizable logic
  let isResizing = false;
  let startX: number;
  let startWidth: number;

  const resizer = document.createElement('div');
  resizer.className = 'sidebar-resizer';
  sidebar.appendChild(resizer);

  resizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    startX = e.clientX;
    startWidth = sidebar.offsetWidth;
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  });

  function handleMouseMove(e: MouseEvent) {
    if (!isResizing) return;
    const delta = e.clientX - startX;
    const newWidth = startWidth - delta; // Subtract delta to expand left, contract right
    if (newWidth > 100) { // Minimum width
      sidebar.style.width = `${newWidth}px`;
    }
  }

  function handleMouseUp() {
    isResizing = false;
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
  }

  return sidebar;
} 