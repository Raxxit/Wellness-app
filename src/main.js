import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 1. Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// 2. Your Custom CSS Assets
import './assets/css/animate.min.css'      // For the WOW.js animations
import './assets/css/loaders.css'          // For any loading spinners
import './assets/css/nivo-lightbox.css'    // For the lightbox gallery
import './assets/css/nivo_themes/default/default.css' // Lightbox theme
import './assets/css/custom.css'           // Your main custom styles (Load this LAST)



const app = createApp(App)

app.use(router)
app.mount('#app')