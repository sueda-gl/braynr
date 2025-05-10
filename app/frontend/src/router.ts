// src/router.tsx
import { LibraryPage } from './pages/LibraryPage';

class Router {
  private container: HTMLElement | null = null;

  init(container: HTMLElement) {
    console.log('Router initializing...');
    this.container = container;
    this.renderLibrary();
  }

  private renderLibrary() {
    if (!this.container) {
      console.error('No container found');
      return;
    }

    console.log('Rendering Library Page');
    this.container.innerHTML = '';
    this.container.appendChild(LibraryPage());
  }
}

export const router = new Router();