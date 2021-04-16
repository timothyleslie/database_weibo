import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            component: resolve => require(['../index.vue'], resolve)
        },
        {
            path: '/login',
            component: resolve => require(['../login.vue'], resolve)
        },
        {
            path: '/register',
            component: resolve => require(['../register.vue'], resolve)
        },

        {
            path: '/admin',
            component: resolve => require(['../admin/common/Home.vue'], resolve),
            children:[
                {
                    path: '/account_admin',
                    component: resolve => require(['../admin/page/account_admin.vue'], resolve)
                },
                // {
                //     path: '/favorite_admin',
                //     component: resolve => require(['../admin/page/favorite_admin.vue'], resolve)
                // },
                {
                    path: '/article_admin',
                    component: resolve => require(['../admin/page/article_admin.vue'], resolve)
                },
                {
                    path: '/browse',
                    component: resolve => require(['../admin/page/browse.vue'], resolve)
                },
                {
                    path: '/fav_admin',
                    component: resolve => require(['../admin/page/fav_admin.vue'], resolve)
                },
                {
                    path: '/comment',
                    component: resolve => require(['../admin/page/comment.vue'], resolve)
                },
                {
                    path: '/focus_admin',
                    component: resolve => require(['../admin/page/focus_admin.vue'], resolve)
                },
                {
                    path: '/my_focus',
                    component: resolve => require(['../admin/page/my_focus.vue'], resolve)
                },
                {
                    path: '/private_message',
                    component: resolve => require(['../admin/page/private_message.vue'], resolve)
                },
            ]
        }
    ]
})
