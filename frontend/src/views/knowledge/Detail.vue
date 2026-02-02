<template>
  <div class="knowledge-detail">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>知识文章详情</span>
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回</span>
          </el-button>
        </div>
      </template>
      <div class="detail-content">
        <h1 class="article-title">{{ articleDetail.title }}</h1>
        <div class="article-meta">
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            <span>{{ articleDetail.created_at }}</span>
          </span>
          <span class="meta-item">
            <el-icon><Folder /></el-icon>
            <span>{{ articleDetail.category_name }}</span>
          </span>
          <span class="meta-item tags">
            <el-icon><Reading /></el-icon>
            <el-tag
              v-for="tag in articleDetail.tags"
              :key="tag"
              size="small"
              class="tag-item"
            >
              {{ tag }}
            </el-tag>
          </span>
        </div>
        <div class="article-content">
          {{ articleDetail.content }}
        </div>
        <div class="action-buttons">
          <el-button type="primary" @click="goToEdit">
            <el-icon><Edit /></el-icon>
            <span>编辑</span>
          </el-button>
          <el-button type="danger" @click="deleteArticle">
            <el-icon><Delete /></el-icon>
            <span>删除</span>
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Calendar, Folder, Reading, Edit, Delete } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const articleId = route.params.id as string

// 文章详情
const articleDetail = reactive({
  id: Number(articleId),
  title: '',
  category_name: '',
  tags: [] as string[],
  content: '',
  created_at: '',
  updated_at: ''
})

// 加载文章详情
const loadArticleDetail = () => {
  // 这里应该调用API获取文章详情
  console.log('加载文章详情ID:', articleId)
  // 模拟数据
  articleDetail.title = '系统使用指南'
  articleDetail.category_name = '系统指南'
  articleDetail.tags = ['系统', '指南', '使用']
  articleDetail.content = '# 系统使用指南\n\n## 1. 系统登录\n\n打开系统登录页面，输入用户名和密码，点击登录按钮即可进入系统。\n\n## 2. 档案管理\n\n在左侧导航栏中点击「档案管理」，可以查看、创建、编辑和删除档案。\n\n### 2.1 创建档案\n\n点击「创建档案」按钮，填写档案名称、选择分类、输入描述并上传相关文件，点击提交按钮即可创建档案。\n\n### 2.2 编辑档案\n\n在档案列表中点击「编辑」按钮，修改档案信息后点击保存按钮即可更新档案。\n\n### 2.3 删除档案\n\n在档案列表中点击「删除」按钮，确认后即可删除档案。\n\n## 3. 知识库管理\n\n在左侧导航栏中点击「知识库管理」，可以查看、创建、编辑和删除知识文章。\n\n### 3.1 创建文章\n\n点击「创建文章」按钮，填写文章标题、选择分类、添加标签并输入内容，点击提交按钮即可创建文章。\n\n### 3.2 编辑文章\n\n在文章列表中点击「编辑」按钮，修改文章信息后点击保存按钮即可更新文章。\n\n### 3.3 删除文章\n\n在文章列表中点击「删除」按钮，确认后即可删除文章。\n\n## 4. 常见问题\n\n### 4.1 忘记密码\n\n点击登录页面的「忘记密码？」链接，按照提示操作即可重置密码。\n\n### 4.2 无法上传文件\n\n请检查文件大小是否超过限制，或文件格式是否支持。\n\n### 4.3 系统响应缓慢\n\n请检查网络连接是否正常，或联系系统管理员。'
  articleDetail.created_at = '2024-01-20 10:30:00'
  articleDetail.updated_at = '2024-01-20 10:30:00'
}

// 跳转到编辑文章页面
const goToEdit = () => {
  router.push(`/knowledge/edit/${articleId}`)
}

// 删除文章
const deleteArticle = () => {
  ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 这里应该调用API删除文章
    console.log('删除文章ID:', articleId)
    // 模拟删除成功
    ElMessage.success('删除成功')
    // 跳转到文章列表页面
    router.push('/knowledge/list')
  }).catch(() => {
    // 取消删除
  })
}

// 返回上一页
const goBack = () => {
  router.push('/knowledge/list')
}

// 页面加载时初始化数据
onMounted(() => {
  loadArticleDetail()
})
</script>

<style scoped>
.knowledge-detail {
  min-height: 600px;
}

.page-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-content {
  margin-top: 20px;
}

.article-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.tags {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tag-item {
  margin-right: 4px;
}

.article-content {
  line-height: 1.8;
  white-space: pre-wrap;
  margin-bottom: 40px;
  color: #303133;
}

.action-buttons {
  margin-top: 30px;
  display: flex;
  gap: 12px;
}
</style>