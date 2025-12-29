import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'home', component: HomeView },
        // You will create these other files later as you need them
        // { path: '/community', component: () => import('../views/CommunityView.vue') },
        // { path: '/login', component: () => import('../views/LoginView.vue') }

        {
            path: '/about',
            name: 'about',
            component: AboutView
        }


    ]
})

export default router