import React from 'react';
import { NavButton } from './NavButton'; // Imports the new NavButton.tsx

interface SidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeSection, onSectionChange }) => {
  return (
    <aside className="sidebar">
      <h1 className="sidebar-title">Braynr</h1>
      <NavButton
        label="Library"
        count={1}
        isActive={activeSection === 'library'}
        onClick={() => onSectionChange('library')}
      />
      <NavButton
        label="Flashcard Decks"
        count={0}
        isActive={activeSection === 'flashcards'}
        onClick={() => onSectionChange('flashcards')}
        subItems={[
          { label: 'Flashcards to review', color: '#ff4444' },
          { label: 'Flashcards to do', color: '#ff8800' },
          { label: 'Flashcards waiting', color: '#ffbb33' },
        ]}
      />
    </aside>
  );
}; 