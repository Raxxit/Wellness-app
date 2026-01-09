import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import QuestionnaireView from '@/views/questionnaireView.vue'
import Profile from '@/views/Profile.vue'

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
        },

        {
            path: '/questionnaire',
            name: 'questionnaire',
            component: QuestionnaireView
        },

        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegistrationView.vue')
        },

        {
            path: '/profile',
            name: 'Profile',
            component: () => import('../views/Profile.vue')
        },
        
        {  path: '/dashboard',
  name: 'dashboard',
  component: () => import('../views/DashboardView.vue')
}


    ]
})





export default router



