import { Sidebar } from './sidebar/Sidebar';
import { Header } from './header/Header';
import { LibraryContent } from './content/LibraryContent';

export const Library = (): HTMLElement => {
  let activeSection = 'library';
  
  const container = document.createElement('div');
  container.className = 'library-container';
  
  const mainContent = document.createElement('div');
  mainContent.className = 'main-content';
  
  const render = () => {
    container.innerHTML = '';
    mainContent.innerHTML = '';
    
    const sidebar = Sidebar(activeSection, (section) => {
      activeSection = section;
      render();
    });
    
    const header = Header();
    const content = LibraryContent(activeSection);
    
    mainContent.appendChild(header);
    mainContent.appendChild(content);
    
    container.appendChild(sidebar);
    container.appendChild(mainContent);
  };
  
  render();
  return container;
};