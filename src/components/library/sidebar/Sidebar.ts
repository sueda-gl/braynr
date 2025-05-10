import { NavButton } from './NavButton';

export const Sidebar = (activeSection: string, onNavigate: (section: string) => void): HTMLElement => {
  const sidebar = document.createElement('aside');
  sidebar.className = 'sidebar';
  
  const title = document.createElement('h1');
  title.className = 'sidebar-title';
  title.textContent = 'Braynn';
  
  const libraryButton = NavButton({
    label: 'Library',
    count: 1,
    isActive: activeSection === 'library',
    onClick: () => onNavigate('library')
  });
  
  const flashcardButton = NavButton({
    label: 'Flashcard Decks',  
    count: 0,
    isActive: activeSection === 'flashcards',
    onClick: () => onNavigate('flashcards'),
    subItems: [
      { label: 'Flashcards to review', color: '#ff4444' },
      { label: 'Flashcards to do', color: '#ff8800' },
      { label: 'Flashcards waiting', color: '#ffbb33' }
    ]
  });
  
  sidebar.appendChild(title);
  sidebar.appendChild(libraryButton);
  sidebar.appendChild(flashcardButton);
  
  return sidebar;
};