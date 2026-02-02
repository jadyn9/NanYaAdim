<template>
  <div class="not-found">
    <div class="not-found-content">
      <el-result
        icon="warning"
        title="404"
        sub-title="抱歉，页面不存在"
      >
        <template #extra>
          <el-button type="primary" @click="goHome">返回首页</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

// 返回首页
const goHome = () => {
  router.push('/home')
}
</script>

<style scoped>
.not-found {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.not-found-content {
  width: 100%;
  max-width: 600px;
  padding: 40px;
}
</style>