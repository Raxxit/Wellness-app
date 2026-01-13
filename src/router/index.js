import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import QuestionnaireView from '@/views/questionnaireView.vue'
import login from '@/views/login.vue'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'home', component: HomeView },

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
        {
            path: '/login',
            name: 'login',
            component: login
        },




        {
            path: '/error/405',
            name: 'Error405',
            component: () => import('@/views/errors/Error405.vue')
        },

        {
            path: '/error/500',
            name: 'Error500',
            component: () => import('@/views/errors/Error500.vue')
        },
    ]
})





export default router



