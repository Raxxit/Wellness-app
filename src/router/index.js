import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import QuestionnaireView from '@/views/questionnaireView.vue'
import Profile from '@/views/Profile.vue'
import Error400 from '@/views/errors/Error400.vue'
import Error401 from '@/views/errors/Error401.vue'
import Error403 from '@/views/errors/Error403.vue'
import Error404 from '@/views/errors/Error404.vue'
import Error405 from '@/views/errors/Error405.vue'
import Error500 from '@/views/errors/Error500.vue'
import RegistrationView from '@/views/RegistrationView.vue'
import Login from '@/views/login.vue'

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
            component: RegistrationView
        },

        {
            path: '/profile',
            name: 'Profile',
            component: Profile
        },

        {
            path: '/error/400',
            name: 'Error400',
            component: Error400
        },

        {
            path: '/login',
            name: 'login',
            component: Login
        },

        {
            path: '/error/401',
            name: 'Error401',
            component: Error401
        },

        {
            path: '/error/403',
            name: 'Error403',
            component: Error403
        },

        {
            path: '/:pathMatch(.*)*',
            name: 'Error404',
            component: Error404
        },

        {
            path: '/error/405',
            name: 'Error405',
            component: Error405
        },

        {
            path: '/error/500',
            name: 'Error500',
            component: Error500
        },
    ]
})





export default router
