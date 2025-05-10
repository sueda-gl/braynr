import { FlashcardCard } from './FlashcardCard';

export const LibraryContent = (activeSection: string): HTMLElement => {
  const content = document.createElement('div');
  content.className = 'library-content';
  
  if (activeSection === 'library') {
    content.appendChild(FlashcardCard());
  } else if (activeSection === 'flashcards') {
    const message = document.createElement('h2');
    message.textContent = 'Coming Soon!';
    message.style.textAlign = 'center';
    message.style.marginTop = '100px';
    content.appendChild(message);
  }
  
  return content;
};