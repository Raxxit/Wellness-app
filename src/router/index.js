import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import QuestionnaireView from '@/views/QuestionnaireView.vue'
import Profile from '@/views/Profile.vue'
import Error400 from '@/views/errors/Error400.vue'
import Error401 from '@/views/errors/Error401.vue'
import Error403 from '@/views/errors/Error403.vue'
import Error404 from '@/views/errors/Error404.vue'
import Error405 from '@/views/errors/Error405.vue'
import Error500 from '@/views/errors/Error500.vue'

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

{
  path: '/error/400',
  name: 'Error400',
  component: () => import('@/views/errors/Error400.vue')
},

{
  path: '/error/401',
  name: 'Error401',
  component: () => import('@/views/errors/Error401.vue')
},

{
  path: '/error/403',
  name: 'Error403',
  component: () => import('@/views/errors/Error403.vue')
},

{
  path: '/error/404',
  name: 'Error404',
  component: () => import('@/views/errors/Error404.vue')
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



