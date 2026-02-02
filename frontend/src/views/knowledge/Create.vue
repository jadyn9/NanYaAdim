<template>
  <div class="knowledge-create">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>创建知识文章</span>
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回</span>
          </el-button>
        </div>
      </template>
      <el-form
        :model="articleForm"
        :rules="articleRules"
        ref="articleFormRef"
        class="article-form"
      >
        <el-form-item prop="title">
          <el-input
            v-model="articleForm.title"
            placeholder="文章标题"
          ></el-input>
        </el-form-item>
        <el-form-item prop="category_id">
          <el-select
            v-model="articleForm.category_id"
            placeholder="文章分类"
          >
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="tags">
          <div class="tag-input-container">
            <el-tag
              v-for="tag in articleForm.tags"
              :key="tag"
              closable
              @close="removeTag(tag)"
              class="tag-item"
            >
              {{ tag }}
            </el-tag>
            <el-input
              v-model="inputTag"
              placeholder="输入标签，按Enter添加"
              @keyup.enter="addTag"
              class="tag-input"
            ></el-input>
          </div>
        </el-form-item>
        <el-form-item prop="content">
          <el-input
            v-model="articleForm.content"
            type="textarea"
            :rows="10"
            placeholder="文章内容"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="submit-btn" :loading="loading" @click="submitForm">
            提交
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { knowledgeApi } from '@/services/api'

const router = useRouter()
const articleFormRef = ref()
const loading = ref(false)
const inputTag = ref('')

// 文章表单
const articleForm = reactive({
  title: '',
  category_id: '',
  tags: [] as string[],
  content: ''
})

// 文章分类
const categories = ref([])

// 添加标签
const addTag = () => {
  if (inputTag.value && !articleForm.tags.includes(inputTag.value)) {
    articleForm.tags.push(inputTag.value)
    inputTag.value = ''
  }
}

// 删除标签
const removeTag = (tag: string) => {
  const index = articleForm.tags.indexOf(tag)
  if (index > -1) {
    articleForm.tags.splice(index, 1)
  }
}

// 文章验证规则
const articleRules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' }
  ],
  category_id: [
    { required: true, message: '请选择文章分类', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' }
  ]
}

// 加载文章分类
const loadCategories = async () => {
  try {
    // 调用API获取文章分类列表
    const response = await knowledgeApi.getCategories()
    categories.value = response.data || []
  } catch (error) {
    ElMessage.error((error as Error).message || '获取文章分类失败')
  }
}

// 提交表单
const submitForm = async () => {
  if (!articleFormRef.value) return
  
  try {
    await articleFormRef.value.validate()
    loading.value = true
    
    // 调用API创建文章
    await knowledgeApi.createArticle(articleForm)
    
    ElMessage.success('创建成功')
    loading.value = false
    // 跳转到文章列表页面
    router.push('/knowledge/list')
  } catch (error) {
    console.error('表单验证失败', error)
    ElMessage.error((error as Error).message || '创建失败')
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  if (articleFormRef.value) {
    articleFormRef.value.resetFields()
  }
  articleForm.tags = []
}

// 返回上一页
const goBack = () => {
  router.push('/knowledge/list')
}

// 页面加载时获取文章分类
onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.knowledge-create {
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

.article-form {
  max-width: 800px;
}

.submit-btn {
  width: 120px;
}

.tag-input-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 8px;
  min-height: 40px;
  transition: border-color 0.3s;
}

.tag-input-container:hover {
  border-color: #c0c4cc;
}

.tag-item {
  margin-right: 8px;
}

.tag-input {
  flex: 1;
  min-width: 150px;
  border: none;
  outline: none;
  padding: 0;
}

.tag-input::placeholder {
  color: #c0c4cc;
}
</style>