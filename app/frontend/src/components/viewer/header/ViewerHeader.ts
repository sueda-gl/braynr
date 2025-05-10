export function ViewerHeader({
  onToggleSidebar,
  onToggleRightSidebar
}: {
  onToggleSidebar?: () => void,
  onToggleRightSidebar?: () => void
}): HTMLElement {
  const header = document.createElement('div');
  header.className = 'viewer-header';

  // Home button (left, with icon)
  const homeBtn = document.createElement('button');
  homeBtn.className = 'viewer-home-btn';
  homeBtn.innerHTML = `
    <svg width="22" height="22" fill="none" stroke="#222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M3 12L12 3l9 9"/><path d="M9 21V9h6v12"/></svg>
    <span>Home</span>
  `;
  homeBtn.onclick = () => {
    window.location.hash = '';
  };

  // Vertical divider
  const divider = document.createElement('div');
  divider.className = 'viewer-header-divider';

  // Four-dot menu (optional, can be removed if not in your design)
  const dotsMenu = document.createElement('div');
  dotsMenu.className = 'viewer-header-dots';
  dotsMenu.innerHTML = `
    <span class="dot vertical-dot"></span>
    <span class="dot vertical-dot"></span>
    <span class="dot vertical-dot"></span>
  `;

  // Center mock buttons with icons
  const center = document.createElement('div');
  center.className = 'viewer-header-center';
  const buttons = [
    {
      label: 'Text',
      icon: `<svg width="22" height="22" fill="none" stroke="#222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></svg>`
    },
    {
      label: 'Maps',
      icon: `<svg width="22" height="22" fill="none" stroke="#222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>`
    },
    {
      label: 'Add',
      icon: `<svg width="22" height="22" fill="none" stroke="#222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>`
    },
    {
      label: 'Braynr card',
      icon: `<svg width="22" height="22" fill="none" stroke="#222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>`
    }
  ];
  buttons.forEach(({ label, icon }) => {
    const btn = document.createElement('button');
    btn.className = 'viewer-mock-btn';
    btn.innerHTML = `${icon}<span>${label}</span>`;
    center.appendChild(btn);
  });

  // Right: search bar with icon and sidebar toggle
  const right = document.createElement('div');
  right.className = 'viewer-header-right';
  const searchWrapper = document.createElement('div');
  searchWrapper.className = 'viewer-search-wrapper';
  searchWrapper.innerHTML = `
    <svg width="18" height="18" fill="none" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
    <input class="viewer-search-input" type="text" placeholder="Search text..." />
  `;
  const iconBtn = document.createElement('button');
  iconBtn.className = 'viewer-sidebar-toggle-btn';
  iconBtn.innerHTML = `<svg width="22" height="22" fill="none" stroke="#a259ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18"/></svg>`;
  iconBtn.onclick = () => {
    if (onToggleRightSidebar) onToggleRightSidebar();
  };
  right.appendChild(searchWrapper);
  right.appendChild(iconBtn);

  header.appendChild(homeBtn);
  header.appendChild(divider);
  header.appendChild(dotsMenu);
  header.appendChild(center);
  header.appendChild(right);
  return header;
}
