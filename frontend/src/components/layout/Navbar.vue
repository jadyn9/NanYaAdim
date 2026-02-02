<template>
  <el-header height="60px" class="navbar">
    <div class="navbar-left">
      <el-button
        type="text"
        class="menu-toggle"
        @click="toggleMenu"
      >
        <el-icon><Menu /></el-icon>
      </el-button>
      <h3>{{ pageTitle }}</h3>
    </div>
    <div class="navbar-right">
      <!-- 主题切换按钮 -->
      <div class="theme-toggle">
        <el-button 
          circle 
          size="small" 
          @click="toggleTheme"
          :title="themeStore.isDarkTheme ? '切换到默认主题' : '切换到暗色主题'"
        >
          {{ themeStore.isDarkTheme ? '☀️' : '🌙' }}
        </el-button>
      </div>
      
      <el-dropdown>
        <span class="user-info">
          <el-avatar size="small" :src="userAvatar"></el-avatar>
          <span class="user-name">{{ userName }}</span>
          <el-icon><ArrowDown /></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="goToProfile">
              <el-icon><User /></el-icon>
              <span>个人信息</span>
            </el-dropdown-item>
            <el-dropdown-item @click="goToSettings">
              <el-icon><Setting /></el-icon>
              <span>设置</span>
            </el-dropdown-item>
            <el-dropdown-item divided @click="logout">
              <el-icon><SwitchButton /></el-icon>
              <span>退出登录</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-header>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu, User, Setting, SwitchButton, ArrowDown, Sunny, Moon } from '@element-plus/icons-vue'
import { useThemeStore } from '@/stores/theme'

const route = useRoute()
const router = useRouter()

// 初始化主题store
const themeStore = useThemeStore()

// 页面标题
const pageTitle = computed(() => {
  return route.meta.title || '南雅管理系统'})

// 用户信息
const userName = ref('管理员')
const userAvatar = ref('')

// 从localStorage获取用户信息
const loadUserInfo = () => {
  const rememberedUser = localStorage.getItem('rememberedUser')
  if (rememberedUser) {
    userName.value = rememberedUser
  }
  // 从localStorage获取用户头像
  const savedAvatar = localStorage.getItem('userAvatar')
  if (savedAvatar) {
    userAvatar.value = savedAvatar
  }
  // 从localStorage获取用户信息
  const savedUserInfo = localStorage.getItem('userInfo')
  if (savedUserInfo) {
    const userInfo = JSON.parse(savedUserInfo)
    if (userInfo.name) {
      userName.value = userInfo.name
    }
  }
}

// 页面加载时获取用户信息
loadUserInfo()

// 切换菜单
const toggleMenu = () => {
  // 这里可以添加菜单折叠/展开的逻辑
}

// 跳转到个人信息页面
const goToProfile = () => {
  router.push('/profile')
}

// 跳转到设置页面
const goToSettings = () => {
  router.push('/settings')
}

// 切换主题
const toggleTheme = () => {
  themeStore.toggleTheme()
}

// 退出登录
const logout = () => {
  // 清除本地存储的token
  localStorage.removeItem('token')
  // 重定向到登录页
  router.push('/auth/login')
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0 20px;
  position: fixed;
  top: 0;
  right: 0;
  left: 200px;
  z-index: 1000;
  transition: all 0.3s ease;
}

.navbar:hover {
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.menu-toggle {
  font-size: 20px;
  color: #333;
}

.navbar-left h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.user-name {
  font-size: 14px;
  color: #333;
}

/* 主题切换按钮 */
.theme-toggle {
  margin-right: 16px;
}

.theme-toggle .el-button {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: #333;
  transition: all 0.3s ease;
}

.theme-toggle .el-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

/* 暗色主题下的主题切换按钮 */
.dark-theme .theme-toggle .el-button {
  background-color: rgba(64, 64, 64, 0.5);
  border-color: rgba(80, 80, 80, 0.6);
  color: #e0e0e0;
}

.dark-theme .theme-toggle .el-button:hover {
  background-color: rgba(80, 80, 80, 0.6);
  border-color: rgba(96, 96, 96, 0.7);
}

:deep(.el-avatar) {
  margin-right: 8px;
}

:deep(.el-dropdown-menu) {
  min-width: 180px;
}

:deep(.el-dropdown-item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-dropdown-item .el-icon) {
  font-size: 14px;
}
</style>