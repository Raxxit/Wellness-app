import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import Profile from '@/views/Profile.vue'
import login from '@/views/login.vue'
import resources from '@/views/resources.vue'
import RegistrationView from '@/views/RegistrationView.vue'
import ProfessionalRegistration from '@/views/ProfessionalRegistration.vue'
import AdminQuestionManager from '@/views/AdminQuestionManager.vue'
import DynamicQuestionnaire from '@/views/DynamicQuestionnaire.vue'
import Report from '@/views/Report.vue'
import Dashboard from '@/views/Dashboard.vue'
import AdminVerification from '@/views/AdminVerification.vue'
import Advisordash from '@/views/advisordash.vue'
import Patienthistory from '@/views/patienthistory.vue'

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
            path: '/adminverify',
            name: 'adminverify',
            component: AdminVerification,
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
            path: '/advisordash',
            name: 'advisordash',
            component: Advisordash,
        },
        {
            path: '/advisor/patient/:id',
            name: 'PatientHistory',
            component: Patienthistory,
        },

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