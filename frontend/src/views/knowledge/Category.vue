<template>
  <div class="knowledge-category">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>知识分类管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>
            <span>添加分类</span>
          </el-button>
        </div>
      </template>
      <el-table :data="categories" style="width: 100%">
        <el-table-column prop="id" label="分类ID" width="80"></el-table-column>
        <el-table-column prop="name" label="分类名称" width="180"></el-table-column>
        <el-table-column prop="description" label="分类描述"></el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteCategory(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 添加分类对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogType === 'add' ? '添加分类' : '编辑分类'"
        width="500px"
      >
        <el-form
          :model="categoryForm"
          :rules="categoryRules"
          ref="categoryFormRef"
          class="category-form"
        >
          <el-form-item prop="name">
            <el-input
              v-model="categoryForm.name"
              placeholder="分类名称"
            ></el-input>
          </el-form-item>
          <el-form-item prop="description">
            <el-input
              v-model="categoryForm.description"
              type="textarea"
              :rows="3"
              placeholder="分类描述"
            ></el-input>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" :loading="loading" @click="submitCategory">确定</el-button>
          </span>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const dialogVisible = ref(false)
const dialogType = ref('add')
const categoryFormRef = ref()
const loading = ref(false)

// 分类表单
const categoryForm = reactive({
  id: 0,
  name: '',
  description: ''
})

// 分类验证规则
const categoryRules = {
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入分类描述', trigger: 'blur' }
  ]
}

// 分类列表
const categories = ref([
  {
    id: 1,
    name: '技术文档',
    description: '技术相关的文档和指南',
    created_at: '2024-01-20 10:00:00'
  },
  {
    id: 2,
    name: '业务流程',
    description: '公司业务流程和操作规范',
    created_at: '2024-01-20 10:00:00'
  },
  {
    id: 3,
    name: '系统指南',
    description: '系统使用指南和帮助文档',
    created_at: '2024-01-20 10:00:00'
  },
  {
    id: 4,
    name: '常见问题',
    description: '常见问题和解答',
    created_at: '2024-01-20 10:00:00'
  }
])

// 打开添加分类对话框
const openAddDialog = () => {
  dialogType.value = 'add'
  categoryForm.id = 0
  categoryForm.name = ''
  categoryForm.description = ''
  dialogVisible.value = true
}

// 打开编辑分类对话框
const openEditDialog = (category: any) => {
  dialogType.value = 'edit'
  categoryForm.id = category.id
  categoryForm.name = category.name
  categoryForm.description = category.description
  dialogVisible.value = true
}

// 提交分类表单
const submitCategory = async () => {
  if (!categoryFormRef.value) return
  
  try {
    await categoryFormRef.value.validate()
    loading.value = true
    
    // 这里应该调用API添加或更新分类
    console.log(`${dialogType.value === 'add' ? '添加' : '更新'}分类:`, categoryForm)
    
    // 模拟操作成功
    setTimeout(() => {
      ElMessage.success(`${dialogType.value === 'add' ? '添加' : '更新'}成功`)
      loading.value = false
      dialogVisible.value = false
      // 重新加载分类列表
      loadCategories()
    }, 1000)
  } catch (error) {
    console.error('表单验证失败', error)
    loading.value = false
  }
}

// 删除分类
const deleteCategory = (id: number) => {
  ElMessageBox.confirm('确定要删除这个分类吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 这里应该调用API删除分类
    console.log('删除分类ID:', id)
    // 模拟删除成功
    ElMessage.success('删除成功')
    // 重新加载分类列表
    loadCategories()
  }).catch(() => {
    // 取消删除
  })
}

// 加载分类列表
const loadCategories = () => {
  // 这里应该调用API获取分类列表
  console.log('加载分类列表')
  // 模拟数据已在上面定义
}

// 页面加载时初始化数据
onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.knowledge-category {
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

.category-form {
  margin-top: 20px;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>