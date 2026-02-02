// 导入Vue Router的createRouter和createWebHistory函数
import { createRouter, createWebHistory } from 'vue-router'

// 导入RouteRecordRaw类型，用于路由配置的类型定义
import type { RouteRecordRaw } from 'vue-router'

// 定义路由配置数组
const routes: RouteRecordRaw[] = [
  {
    // 根路径，直接显示登录页面
    path: '/',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { title: '登录' }
  },
  {
    // 登录路径，重定向到根路径
    path: '/login',
    redirect: '/'
  },
  {
    // 首页路由，需要认证
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页', requiresAuth: true }
  },
  {
    // 认证模块路由
    path: '/auth',
    name: 'Auth',
    component: () => import('@/views/auth/Login.vue'),
    children: [
      {
        // 登录子路由，重定向到根路径
        path: 'login',
        redirect: '/'
      },
      {
        // 注册子路由
        path: 'register',
        name: 'Register',
        component: () => import('@/views/auth/Register.vue'),
        meta: { title: '注册' }
      }
    ]
  },
  {
    // 档案管理模块路由，需要认证
    path: '/archive',
    name: 'Archive',
    component: () => import('@/views/archive/Index.vue'),
    meta: { title: '档案管理', requiresAuth: true },
    children: [
      {
        // 档案列表子路由
        path: 'list',
        name: 'ArchiveList',
        component: () => import('@/views/archive/List.vue'),
        meta: { title: '档案列表' }
      },
      {
        // 档案详情子路由，带动态参数id
        path: 'detail/:id',
        name: 'ArchiveDetail',
        component: () => import('@/views/archive/Detail.vue'),
        meta: { title: '档案详情' }
      },
      {
        // 创建档案子路由
        path: 'create',
        name: 'ArchiveCreate',
        component: () => import('@/views/archive/Create.vue'),
        meta: { title: '创建档案' }
      },
      {
        // 编辑档案子路由，带动态参数id
        path: 'edit/:id',
        name: 'ArchiveEdit',
        component: () => import('@/views/archive/Edit.vue'),
        meta: { title: '编辑档案' }
      },
      {
        // 档案分类管理子路由
        path: 'category',
        name: 'ArchiveCategory',
        component: () => import('@/views/archive/Category.vue'),
        meta: { title: '档案分类管理' }
      }
    ]
  },
  {
    // 知识库管理模块路由，需要认证
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('@/views/knowledge/Index.vue'),
    meta: { title: '知识库管理', requiresAuth: true },
    children: [
      {
        // 知识文章列表子路由
        path: 'list',
        name: 'KnowledgeList',
        component: () => import('@/views/knowledge/List.vue'),
        meta: { title: '知识文章列表' }
      },
      {
        // 知识文章详情子路由，带动态参数id
        path: 'detail/:id',
        name: 'KnowledgeDetail',
        component: () => import('@/views/knowledge/Detail.vue'),
        meta: { title: '知识文章详情' }
      },
      {
        // 创建知识文章子路由
        path: 'create',
        name: 'KnowledgeCreate',
        component: () => import('@/views/knowledge/Create.vue'),
        meta: { title: '创建知识文章' }
      },
      {
        // 编辑知识文章子路由，带动态参数id
        path: 'edit/:id',
        name: 'KnowledgeEdit',
        component: () => import('@/views/knowledge/Edit.vue'),
        meta: { title: '编辑知识文章' }
      },
      {
        // 知识分类管理子路由
        path: 'category',
        name: 'KnowledgeCategory',
        component: () => import('@/views/knowledge/Category.vue'),
        meta: { title: '知识分类管理' }
      }
    ]
  },
  {
    // 404页面路由，匹配所有未定义的路径
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面不存在' }
  },
  {
    // 个人信息页面
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { title: '个人信息', requiresAuth: true }
  },
  {
    // 设置页面
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { title: '设置', requiresAuth: true }
  }
]

// 创建路由实例
const router = createRouter({
  // 使用HTML5 History模式
  history: createWebHistory(),
  // 应用路由配置
  routes
})

// 路由守卫，用于权限控制和页面标题设置
router.beforeEach((to, _from, next) => {
  // 设置页面标题，优先使用路由配置的title，否则使用默认标题
  document.title = `${to.meta.title || '企业中后台管理系统'}`
  
  // 检查当前路由是否需要认证
  const requiresAuth = to.meta.requiresAuth
  
  // 从localStorage获取token，判断用户是否已登录
  const token = localStorage.getItem('token')
  
  // 如果需要认证但没有token，重定向到登录页
  if (requiresAuth && !token) {
    next({ name: 'Login' })
  } else {
    // 否则继续导航
    next()
  }
})

// 导出路由实例
export default router