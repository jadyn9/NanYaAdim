<template>
  <div class="archive-detail">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>档案详情</span>
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            <span>返回</span>
          </el-button>
        </div>
      </template>
      <div class="detail-content">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form :model="archiveDetail" label-width="100px" class="detail-form">
              <el-form-item label="档案名称">
                <span>{{ archiveDetail.name }}</span>
              </el-form-item>
              <el-form-item label="档案分类">
                <span>{{ archiveDetail.category_name }}</span>
              </el-form-item>
              <el-form-item label="创建时间">
                <span>{{ archiveDetail.created_at }}</span>
              </el-form-item>
              <el-form-item label="更新时间">
                <span>{{ archiveDetail.updated_at }}</span>
              </el-form-item>
              <el-form-item label="档案描述">
                <div class="description-content">{{ archiveDetail.description }}</div>
              </el-form-item>
            </el-form>
          </el-col>
          <el-col :span="12">
            <el-card class="file-card">
              <template #header>
                <span>相关文件</span>
              </template>
              <el-list>
                <el-list-item
                  v-for="file in files"
                  :key="file.id"
                  class="file-item"
                >
                  <el-icon><Document /></el-icon>
                  <span class="file-name">{{ file.name }}</span>
                  <span class="file-size">({{ file.size }})</span>
                  <el-button type="primary" size="small" @click="downloadFile(file.id)" style="margin-left: auto;">
                    下载
                  </el-button>
                </el-list-item>
              </el-list>
            </el-card>
          </el-col>
        </el-row>
        <div class="action-buttons">
          <el-button type="primary" @click="goToEdit">
            <el-icon><Edit /></el-icon>
            <span>编辑</span>
          </el-button>
          <el-button type="danger" @click="deleteArchive">
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
import { ArrowLeft, Document, Edit, Delete } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const archiveId = route.params.id as string

// 档案详情
const archiveDetail = reactive({
  id: Number(archiveId),
  name: '',
  category_name: '',
  description: '',
  created_at: '',
  updated_at: ''
})

// 相关文件
const files = ref([
  { id: 1, name: '档案文件1.pdf', size: '1.2MB' },
  { id: 2, name: '档案文件2.docx', size: '850KB' }
])

// 加载档案详情
const loadArchiveDetail = () => {
  // 这里应该调用API获取档案详情
  console.log('加载档案详情ID:', archiveId)
  // 模拟数据
  archiveDetail.name = '员工入职档案-张三'
  archiveDetail.category_name = '人事档案'
  archiveDetail.description = '张三的入职档案，包含个人基本信息、学历证明、工作经历等材料。'
  archiveDetail.created_at = '2024-01-20 10:30:00'
  archiveDetail.updated_at = '2024-01-20 10:30:00'
}

// 跳转到编辑页面
const goToEdit = () => {
  router.push(`/archive/edit/${archiveId}`)
}

// 删除档案
const deleteArchive = () => {
  ElMessageBox.confirm('确定要删除这条档案吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 这里应该调用API删除档案
    console.log('删除档案ID:', archiveId)
    // 模拟删除成功
    ElMessage.success('删除成功')
    // 跳转到档案列表页面
    router.push('/archive/list')
  }).catch(() => {
    // 取消删除
  })
}

// 下载文件
const downloadFile = (fileId: number) => {
  // 这里应该调用API下载文件
  console.log('下载文件ID:', fileId)
  // 模拟下载成功
  ElMessage.success('下载成功')
}

// 返回上一页
const goBack = () => {
  router.push('/archive/list')
}

// 页面加载时初始化数据
onMounted(() => {
  loadArchiveDetail()
})
</script>

<style scoped>
.archive-detail {
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

.detail-form {
  margin-bottom: 30px;
}

.description-content {
  white-space: pre-wrap;
  line-height: 1.6;
}

.file-card {
  min-height: 300px;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.file-name {
  flex: 1;
  font-size: 14px;
}

.file-size {
  font-size: 12px;
  color: #909399;
}

.action-buttons {
  margin-top: 30px;
  display: flex;
  gap: 12px;
}
</style>