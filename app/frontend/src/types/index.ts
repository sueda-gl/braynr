export interface NavItem {
    id: string;
    label: string;
    count: number;
    isActive?: boolean;
    statusColor?: string;
  }
  
  export interface FlashcardDeck {
    id: string;
    title?: string;
    preview?: string;
  }
  
  export const NAV_ITEMS: NavItem[] = [
    { id: 'library', label: 'Library', count: 1 },
    { id: 'flashcard-decks', label: 'Flashcard Decks', count: 0 },
    { id: 'flashcards-review', label: 'Flashcards to review', count: 0, statusColor: '#ff4444' },
    { id: 'flashcards-todo', label: 'Flashcards to do', count: 0, statusColor: '#ff8800' },
    { id: 'flashcards-waiting', label: 'Flashcards waiting', count: 0, statusColor: '#ffbb33' }
  ];