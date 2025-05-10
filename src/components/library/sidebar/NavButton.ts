export interface NavButtonProps {
    label: string;
    count?: number;
    isActive: boolean;
    onClick: () => void;
    subItems?: { label: string; color?: string }[];
  }
  
  export const NavButton = (props: NavButtonProps): HTMLElement => {
    const button = document.createElement('div');
    button.className = `nav-button ${props.isActive ? 'active' : ''}`;
    
    const mainRow = document.createElement('div');
    mainRow.className = 'nav-button-main';
    
    const label = document.createElement('span');
    label.textContent = props.label;
    
    const count = document.createElement('span');
    count.className = 'nav-count';
    count.textContent = props.count?.toString() || '0';
    
    mainRow.appendChild(label);
    mainRow.appendChild(count);
    button.appendChild(mainRow);
    
    // Add sub-items if they exist
    if (props.subItems) {
      props.subItems.forEach(item => {
        const subItem = document.createElement('div');
        subItem.className = 'nav-sub-item';
        
        const subLabel = document.createElement('span');
        subLabel.textContent = item.label;
        
        const subCount = document.createElement('span');
        subCount.textContent = '0';
        
        if (item.color) {
          const dot = document.createElement('span');
          dot.className = 'status-dot';
          dot.style.backgroundColor = item.color;
          subItem.appendChild(dot);
        }
        
        subItem.appendChild(subLabel);
        subItem.appendChild(subCount);
        button.appendChild(subItem);
      });
    }
    
    button.addEventListener('click', props.onClick);
    return button;
  };