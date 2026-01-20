import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import QuestionnaireView from '@/views/questionnaireView.vue'
import Profile from '@/views/Profile.vue'
import login from '@/views/login.vue'
import resources from '@/views/resources.vue'
import RegistrationView from '@/views/RegistrationView.vue'
import AdminQuestionManager from '@/views/AdminQuestionManager.vue'
import DynamicQuestionnaire from '@/views/DynamicQuestionnaire.vue'
import Report from '@/views/Report.vue'
import Dashboard from '@/views/Dashboard.vue'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: HomeView,
            beforeEnter: (to, from, next) => {
                if (localStorage.getItem('token')) {
                    next('/dashboard'); // Redirect if token exists
                } else {
                    next(); // Continue to Home if no token
                }
            }
        },

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
            path: '/login',
            name: 'login',
            component: login
        },

        {
            path: '/profile',
            name: 'profile',
            component: Profile,
            meta: { requiresAuth: true }
        },

        {
            path: '/resources',
            name: 'resources',
            component: resources
        },
        {
            path: '/questions',
            name: 'questions',
            component: AdminQuestionManager
        },
        {
            path: '/dynamicques',
            name: 'dynamicques',
            component: DynamicQuestionnaire
        },
        {
            path: '/report',
            name: 'report',
            component: Report

        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: Dashboard
        },



    ]
})

router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

    const isAuthenticated = localStorage.getItem('token') !== null

    if (requiresAuth && !isAuthenticated) {
        next({
            name: 'login',
            query: { redirect: to.fullPath }
        })
    } else if (to.name === 'login' && isAuthenticated) {
        next({ name: 'profile' })
    } else {
        next()
    }
})


export default router