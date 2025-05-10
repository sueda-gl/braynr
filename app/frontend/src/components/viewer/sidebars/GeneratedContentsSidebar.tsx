import './GeneratedContentsSidebar.css';

interface SidebarOptions {
  getScreenshot?: () => string | null;
  onClearScreenshot?: () => void;
}

export function GeneratedContentsSidebar(opts?: SidebarOptions): HTMLElement {
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
      const screenshot = opts && typeof opts.getScreenshot === 'function' ? opts.getScreenshot() : null;
      if (screenshot) {
        const img = document.createElement('img');
        img.src = screenshot;
        img.alt = 'Screenshot';
        img.style.maxWidth = '100%';
        img.style.display = 'block';
        img.style.margin = '16px auto';
        content.appendChild(img);
        const clearBtn = document.createElement('button');
        clearBtn.textContent = 'Clear Screenshot';
        clearBtn.className = 'clear-screenshot-btn';
        clearBtn.onclick = () => {
          if (opts && typeof opts.onClearScreenshot === 'function') {
            opts.onClearScreenshot();
          }
        };
        content.appendChild(clearBtn);
      } else {
        const placeholder = document.createElement('div');
        placeholder.className = 'placeholder-text';
        placeholder.textContent = 'Make a selection by dragging and dropping to select the area.';
        placeholder.style.color = '#888';
        placeholder.style.textAlign = 'center';
        placeholder.style.marginBottom = '8px';
        const infoIcon = document.createElement('div');
        infoIcon.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>';
        infoIcon.style.textAlign = 'center';
        content.appendChild(placeholder);
        content.appendChild(infoIcon);
      }
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

  // Expose updateScreenshot for parent
  (sidebar as any).updateScreenshot = function () {
    updateContent();
  };

  return sidebar;
} 