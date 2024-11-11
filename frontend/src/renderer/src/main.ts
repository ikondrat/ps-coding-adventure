import './assets/main.css'

import App from './App.svelte'

const app = new App({
  target: document.getElementById('app'),
  props: {
    // Pass any necessary props to the TodoLayout if needed
  }
})

export default app
