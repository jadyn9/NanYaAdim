<template>
  <div class="archive-edit">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>编辑档案</span>
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回</span>
          </el-button>
        </div>
      </template>
      <el-form
        :model="archiveForm"
        :rules="archiveRules"
        ref="archiveFormRef"
        class="archive-form"
      >
        <el-form-item prop="name">
          <el-input
            v-model="archiveForm.name"
            placeholder="档案名称"
          ></el-input>
        </el-form-item>
        <el-form-item prop="category_id">
          <el-select
            v-model="archiveForm.category_id"
            placeholder="档案分类"
          >
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="description">
          <el-input
            v-model="archiveForm.description"
            type="textarea"
            rows="4"
            placeholder="档案描述"
          ></el-input>
        </el-form-item>
        <el-form-item prop="file">
          <el-upload
            class="upload-demo"
            action=""
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="fileList"
            multiple
          >
            <el-button type="primary">
              <el-icon><Upload /></el-icon>
              <span>选择文件</span>
            </el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持上传PDF、Word、Excel等格式文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="submit-btn" :loading="loading" @click="submitForm">
            保存
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Upload } from '@element-plus/icons-vue'
import { archiveApi } from '@/services/api'

const router = useRouter()
const route = useRoute()
const archiveFormRef = ref()
const loading = ref(false)
const archiveId = route.params.id as string

// 档案表单
const archiveForm = reactive({
  id: Number(archiveId),
  name: '',
  category_id: '',
  description: '',
  file: ''
})

// 档案分类
const categories = ref([])

// 文件列表
const fileList = ref([])

// 加载档案分类
const loadCategories = async () => {
  try {
    // 调用API获取档案分类列表
    const response = await archiveApi.getCategories()
    categories.value = response.data || []
  } catch (error) {
    ElMessage.error((error as Error).message || '获取档案分类失败')
  }
}

// 加载档案详情
const loadArchiveDetail = async () => {
  try {
    loading.value = true
    // 调用API获取档案详情
    const response = await archiveApi.getArchive(Number(archiveId))
    const archive = response.data || {}
    // 更新表单数据
    archiveForm.name = archive.name || ''
    archiveForm.category_id = archive.category_id || ''
    archiveForm.description = archive.description || ''
    // 模拟文件列表
    fileList.value = [
      { name: '档案文件1.pdf', url: '' },
      { name: '档案文件2.docx', url: '' }
    ]
  } catch (error) {
    ElMessage.error((error as Error).message || '获取档案详情失败')
  } finally {
    loading.value = false
  }
}

// 文件变化处理
const handleFileChange = (file: any, fileList: any[]) => {
  console.log('文件变化:', file, fileList)
  // 这里可以处理文件上传逻辑
}

// 提交表单
const submitForm = async () => {
  if (!archiveFormRef.value) return
  
  try {
    await archiveFormRef.value.validate()
    loading.value = true
    
    // 调用API更新档案
    await archiveApi.updateArchive(Number(archiveId), archiveForm)
    
    ElMessage.success('保存成功')
    loading.value = false
    // 跳转到档案详情页面
    router.push(`/archive/detail/${archiveId}`)
  } catch (error) {
    console.error('表单验证失败', error)
    ElMessage.error((error as Error).message || '保存失败')
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  if (archiveFormRef.value) {
    archiveFormRef.value.resetFields()
  }
  // 重新加载档案详情
  loadArchiveDetail()
}

// 返回上一页
const goBack = () => {
  router.push(`/archive/detail/${archiveId}`)
}

// 页面加载时初始化数据
onMounted(() => {
  loadCategories()
  loadArchiveDetail()
})
</script>

<style scoped>
.archive-edit {
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

.archive-form {
  max-width: 600px;
}

.submit-btn {
  width: 120px;
}

.upload-demo {
  margin-bottom: 20px;
}
</style>