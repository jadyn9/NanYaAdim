<template>
  <div class="auth-container">
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
// 认证模块的父组件
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}
</style>