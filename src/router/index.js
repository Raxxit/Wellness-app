import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import QuestionnaireView from '@/views/questionnaireView.vue'
import Profile from '@/views/Profile.vue'

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
            component: () => import('../views/RegistrationView.vue')
        },

        {
            path: '/login',
            name: 'login',
            component: () => import('../views/login.vue')
        },

        {
            path: '/profile',
            name: 'profile',
            component: () => import('../views/Profile.vue'),
            meta: { requiresAuth: true } 
        }

    
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