// src/router.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { LibraryPage } from './pages/LibraryPage';
import { ViewerPage } from './pages/ViewerPage';

class Router {
  private container: HTMLElement | null = null;
  private reactRoot: ReactDOM.Root | null = null;

  init(container: HTMLElement) {
    this.container = container;
    this.container.innerHTML = '';
    this.reactRoot = ReactDOM.createRoot(container);
    window.addEventListener('hashchange', () => this.route());
    this.route();
  }

  private route() {
    if (!this.reactRoot) {
      console.error('Router not properly initialized with a React root.');
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
    if (!this.reactRoot) return;
    this.reactRoot.render(
      <React.StrictMode>
        <LibraryPage />
      </React.StrictMode>
    );
  }

  private renderViewer(id: string) {
    if (!this.reactRoot) return;
    this.reactRoot.render(
      <React.StrictMode>
        <ViewerPage id={id} />
      </React.StrictMode>
    );
  }
}

export const router = new Router();