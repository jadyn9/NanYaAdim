<template>
  <div class="archive-list">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>档案列表</span>
          <el-button type="primary" @click="goToCreate">
            <el-icon><Plus /></el-icon>
            <span>创建档案</span>
          </el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchForm.name"
              placeholder="档案名称"
              prefix-icon="Search"
            ></el-input>
          </el-col>
          <el-col :span="6">
            <el-select
              v-model="searchForm.category_id"
              placeholder="档案分类"
              clearable
            >
              <el-option
                v-for="category in categories"
                :key="category.id"
                :label="category.name"
                :value="category.id"
              ></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-date-picker
              v-model="searchForm.date_range"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            ></el-date-picker>
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="search">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-col>
        </el-row>
      </div>
      <el-table :data="archives" style="width: 100%">
        <el-table-column prop="id" label="档案ID" width="80"></el-table-column>
        <el-table-column prop="name" label="档案名称" min-width="180"></el-table-column>
        <el-table-column prop="category_name" label="分类" width="120"></el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
        <el-table-column prop="updated_at" label="更新时间" width="180"></el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="goToDetail(scope.row.id)">
              查看
            </el-button>
            <el-button type="warning" size="small" @click="goToEdit(scope.row.id)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteArchive(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { archiveApi } from '@/services/api'

const router = useRouter()

// 搜索表单
const searchForm = reactive({
  name: '',
  category_id: '',
  date_range: []
})

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 加载状态
const loading = ref(false)

// 档案分类
const categories = ref([])

// 档案列表
const archives = ref([])

// 搜索
const search = () => {
  pagination.currentPage = 1
  loadArchives()
  ElMessage.success('搜索成功')
}

// 重置搜索
const resetSearch = () => {
  searchForm.name = ''
  searchForm.category_id = ''
  searchForm.date_range = []
  pagination.currentPage = 1
  loadArchives()
}

// 跳转到创建档案页面
const goToCreate = () => {
  router.push('/archive/create')
}

// 跳转到档案详情页面
const goToDetail = (id: number) => {
  router.push(`/archive/detail/${id}`)
}

// 跳转到编辑档案页面
const goToEdit = (id: number) => {
  router.push(`/archive/edit/${id}`)
}

// 删除档案
const deleteArchive = (id: number) => {
  ElMessageBox.confirm('确定要删除这条档案吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      loading.value = true
      // 调用API删除档案
      await archiveApi.deleteArchive(id)
      ElMessage.success('删除成功')
      // 重新加载档案列表
      loadArchives()
    } catch (error) {
      ElMessage.error((error as Error).message || '删除失败')
    } finally {
      loading.value = false
    }
  }).catch(() => {
    // 取消删除
  })
}

// 加载档案列表
const loadArchives = async () => {
  try {
    loading.value = true
    // 调用API获取档案列表
    const response = await archiveApi.getArchives({
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      name: searchForm.name,
      category_id: searchForm.category_id
    })
    // 更新档案列表和分页信息
    archives.value = response.data || []
    pagination.total = response.total || 0
  } catch (error) {
    ElMessage.error((error as Error).message || '获取档案列表失败')
  } finally {
    loading.value = false
  }
}

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

// 分页大小变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  loadArchives()
}

// 当前页码变化
const handleCurrentChange = (current: number) => {
  pagination.currentPage = current
  loadArchives()
}

// 页面加载时初始化数据
onMounted(() => {
  loadCategories()
  loadArchives()
})
</script>

<style scoped>
.archive-list {
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

.search-bar {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>