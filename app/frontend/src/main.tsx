import './style.css';
import { router } from './router';

const app = document.querySelector<HTMLDivElement>('#app');

if (app) {
  console.log('App element found, initializing router...');
  router.init(app);
} else {
  console.error('App element not found!');
}