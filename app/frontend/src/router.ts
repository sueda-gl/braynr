// src/router.tsx
import { LibraryPage } from './pages/LibraryPage';
import { ViewerPage } from './pages/ViewerPage';

class Router {
  private container: HTMLElement | null = null;

  init(container: HTMLElement) {
    this.container = container;
    window.addEventListener('hashchange', () => this.route());
    this.route();
  }

  private route() {
    if (!this.container) {
      console.error('No container found');
      return;
    }
    const hash = window.location.hash;
    if (hash.startsWith('#/viewer/')) {
      const id = hash.replace('#/viewer/', '');
      this.renderViewer(id);
    } else {
      this.renderLibrary();
    }
  }

  private renderLibrary() {
    if (!this.container) return;
    this.container.innerHTML = '';
    this.container.appendChild(LibraryPage());
  }

  private renderViewer(id: string) {
    if (!this.container) return;
    this.container.innerHTML = '';
    this.container.appendChild(ViewerPage(id));
  }
}

export const router = new Router();