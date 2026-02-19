import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import Profile from '@/views/Profile.vue'
import login from '@/views/login.vue'
import resources from '@/views/resources.vue'
import AdminResource from '@/views/AdminResource.vue'
import RegistrationView from '@/views/RegistrationView.vue'
import AdminQuestionManager from '@/views/AdminQuestionManager.vue'
import DynamicQuestionnaire from '@/views/DynamicQuestionnaire.vue'
import Report from '@/views/Report.vue'
import Dashboard from '@/views/Dashboard.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import ManageResources from '@/views/ManageResources.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: HomeView,
            meta: { guestOnly: true }
        },
        {
            path: '/about',
            name: 'about',
            component: AboutView
        },
        {
            path: '/register',
            name: 'register',
            component: RegistrationView,
            meta: { guestOnly: true }
        },
        {
            path: '/register-professional',
            name: 'register-professional',
            component: ProfessionalRegistration,
            meta: { guestOnly: true }
        },
        {
            path: '/login',
            name: 'login',
            component: login,
            meta: { guestOnly: true }
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
            component: resources,
        },
        {
            path: '/AdminResource',
            name: 'AdminResource',
            component: AdminResource,
        },
        {
            path: '/questions',
            name: 'questions',
            component: AdminQuestionManager,
            meta: { requiresAuth: true }
        },
        {
            path: '/dynamicques',
            name: 'dynamicques',
            component: DynamicQuestionnaire,
            meta: { requiresAuth: true }
        },
        {
            path: '/report',
            name: 'report',
            component: Report,
            meta: { requiresAuth: true }
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: Dashboard,
            meta: { requiresAuth: true }
        },
        {
            path: '/ad',
            name: 'ad',
            component: AdminDashboard,
        },
        {
            path: '/manageresources',
            name: 'ManageResources',
            component: ManageResources,
        }
    ]
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('token');

    const requiresAuth = to.meta.requiresAuth;
    const isGuestOnly = to.meta.guestOnly;

    if (requiresAuth && !isAuthenticated) {
        next('/login');
    }
    else if (isGuestOnly && isAuthenticated) {
        next('/dashboard');
    }
    else {
        next();
    }
});

export default router