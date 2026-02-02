<template>
  <el-aside width="200px" class="sidebar">
    <div class="sidebar-header">
      <h2>企业管理系统</h2>
    </div>
    <el-menu
      :default-active="activeMenu"
      :default-openeds="openedMenus"
      class="sidebar-menu"
      router
      :unique-opened="true"
    >
      <el-menu-item index="/home">
        <el-icon><House /></el-icon>
        <span>首页</span>
      </el-menu-item>
      <el-sub-menu index="/archive">
        <template #title>
          <el-icon><Document /></el-icon>
          <span>档案管理</span>
        </template>
        <el-menu-item index="/archive/list">档案列表</el-menu-item>
        <el-menu-item index="/archive/create">创建档案</el-menu-item>
        <el-menu-item index="/archive/category">分类管理</el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/knowledge">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>知识库管理</span>
        </template>
        <el-menu-item index="/knowledge/list">文章列表</el-menu-item>
        <el-menu-item index="/knowledge/create">创建文章</el-menu-item>
        <el-menu-item index="/knowledge/category">分类管理</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </el-aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { House, Document, Menu } from '@element-plus/icons-vue'

const route = useRoute()

// 计算当前激活的菜单
const activeMenu = computed(() => {
  return route.path
})

// 计算需要展开的菜单
const openedMenus = computed(() => {
  const path = route.path
  const menus = []
  if (path.startsWith('/archive/')) {
    menus.push('/archive')
  }
  if (path.startsWith('/knowledge/')) {
    menus.push('/knowledge')
  }
  return menus
})
</script>

<style scoped>
.sidebar {
  height: 100vh;
  background-color: rgba(0, 21, 41, 0.8);
  backdrop-filter: blur(10px);
  color: #fff;
  position: fixed;
  left: 0;
  top: 0;
  overflow-y: auto;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 2px 0 16px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.sidebar:hover {
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: linear-gradient(rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
}

.sidebar-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-menu {
  margin-top: 20px;
  background-color: transparent !important;
}

.sidebar-menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.65);
  height: 48px;
  line-height: 48px;
  margin: 0;
}

.sidebar-menu :deep(.el-menu-item:hover),
.sidebar-menu :deep(.el-menu-item.is-active) {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-menu :deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.65);
  height: 48px;
  line-height: 48px;
}

.sidebar-menu :deep(.el-sub-menu__title:hover) {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-menu :deep(.el-icon) {
  margin-right: 8px;
}

/* 子菜单下拉面板样式 */
.sidebar-menu :deep(.el-sub-menu .el-menu) {
  background-color: rgba(0, 21, 41, 0.9) !important;
  border: none;
}

/* 子菜单项样式 */
.sidebar-menu :deep(.el-sub-menu .el-menu-item) {
  color: rgba(255, 255, 255, 0.65);
  background-color: transparent !important;
}

.sidebar-menu :deep(.el-sub-menu .el-menu-item:hover),
.sidebar-menu :deep(.el-sub-menu .el-menu-item.is-active) {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1) !important;
}
</style>