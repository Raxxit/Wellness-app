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


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
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