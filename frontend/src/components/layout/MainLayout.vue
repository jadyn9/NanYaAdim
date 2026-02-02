<template>
  <div class="main-layout-container">
    <div class="layout-bg"></div>
    <el-container class="main-layout">
      <!-- 侧边栏 -->
      <Sidebar />
      
      <el-container>
        <!-- 顶部导航栏 -->
        <Navbar />
        
        <!-- 主内容区域 -->
        <el-main class="main-content">
          <slot></slot>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import Sidebar from './Sidebar.vue'
import Navbar from './Navbar.vue'
</script>

<style scoped>
.main-layout-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.layout-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)), url('https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=modern%20abstract%20technology%20background%20with%20blue%20and%20purple%20hues%20for%20login%20page&image_size=landscape_16_9');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  z-index: 0;
}

/* SVG图案叠加层 */
.layout-bg::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="none"/><path d="M10 10 L90 10 L90 90 L10 90 Z" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></svg>');
  background-size: 100px 100px;
  opacity: 0.3;
  pointer-events: none;
  z-index: 1;
}

.main-layout {
  position: relative;
  height: 100vh;
  overflow: hidden;
  z-index: 1;
}

.main-content {
  margin-top: 60px;
  margin-left: 200px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.2);
  min-height: calc(100vh - 60px);
  overflow-y: auto;
  z-index: 2;
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
}
</style>