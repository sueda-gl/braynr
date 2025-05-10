export const FlashcardCard = (): HTMLElement => {
    const card = document.createElement('div');
    card.className = 'flashcard-card';
    
    const dotsMenu = document.createElement('div');
    dotsMenu.className = 'dots-menu';
    dotsMenu.textContent = '⋯';
    
    const content = document.createElement('div');
    content.className = 'card-content';
    content.innerHTML = `
      <p>Contract & Procedure:</p>
      <p>Buyer Offer:</p>
      <p>QA Evaluation:</p>
      <p>Negotiation & Closing:</p>
    `;
    
    card.appendChild(dotsMenu);
    card.appendChild(content);
    
    return card;
  };