import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import QuestionnaireView from '@/views/questionnaireView.vue'
import Profile from '@/views/Profile.vue'
import login from '@/views/login.vue'


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
            component: RegistrationView
        },

        {
            path: '/login',
            name: 'login',
            component: () => import('../views/login.vue')
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



