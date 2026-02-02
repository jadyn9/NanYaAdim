<template>
  <div class="knowledge-list">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>知识文章列表</span>
          <el-button type="primary" @click="goToCreate">
            <el-icon><Plus /></el-icon>
            <span>创建文章</span>
          </el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchForm.title"
              placeholder="文章标题"
              prefix-icon="Search"
            ></el-input>
          </el-col>
          <el-col :span="6">
            <el-select
              v-model="searchForm.category_id"
              placeholder="文章分类"
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
            <el-input
              v-model="searchForm.tag"
              placeholder="标签"
              prefix-icon="Reading"
            ></el-input>
          </el-col>
          <el-col :span="6">
            <el-button type="primary" @click="search">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-col>
        </el-row>
      </div>
      <el-table :data="articles" style="width: 100%">
        <el-table-column prop="id" label="文章ID" width="80"></el-table-column>
        <el-table-column prop="title" label="文章标题" min-width="200"></el-table-column>
        <el-table-column prop="category_name" label="分类" width="120"></el-table-column>
        <el-table-column prop="tags" label="标签" width="180">
          <template #default="scope">
            <el-tag
              v-for="tag in scope.row.tags"
              :key="tag"
              size="small"
              style="margin-right: 4px"
            >
              {{ tag }}
            </el-tag>
          </template>
        </el-table-column>
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
            <el-button type="danger" size="small" @click="deleteArticle(scope.row.id)">
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
import { Plus, Search, Reading } from '@element-plus/icons-vue'
import { knowledgeApi } from '@/services/api'

const router = useRouter()

// 搜索表单
const searchForm = reactive({
  title: '',
  category_id: '',
  tag: ''
})

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 加载状态
const loading = ref(false)

// 文章分类
const categories = ref([])

// 文章列表
const articles = ref([])

// 搜索
const search = () => {
  pagination.currentPage = 1
  loadArticles()
  ElMessage.success('搜索成功')
}

// 重置搜索
const resetSearch = () => {
  searchForm.title = ''
  searchForm.category_id = ''
  searchForm.tag = ''
  pagination.currentPage = 1
  loadArticles()
}

// 跳转到创建文章页面
const goToCreate = () => {
  router.push('/knowledge/create')
}

// 跳转到文章详情页面
const goToDetail = (id: number) => {
  router.push(`/knowledge/detail/${id}`)
}

// 跳转到编辑文章页面
const goToEdit = (id: number) => {
  router.push(`/knowledge/edit/${id}`)
}

// 删除文章
const deleteArticle = (id: number) => {
  ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      loading.value = true
      // 调用API删除文章
      await knowledgeApi.deleteArticle(id)
      ElMessage.success('删除成功')
      // 重新加载文章列表
      loadArticles()
    } catch (error) {
      ElMessage.error((error as Error).message || '删除失败')
    } finally {
      loading.value = false
    }
  }).catch(() => {
    // 取消删除
  })
}

// 加载文章列表
const loadArticles = async () => {
  try {
    loading.value = true
    // 调用API获取文章列表
    const response = await knowledgeApi.getArticles({
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      title: searchForm.title,
      category_id: searchForm.category_id,
      tag: searchForm.tag
    })
    // 更新文章列表和分页信息
    articles.value = response.data || []
    pagination.total = response.total || 0
  } catch (error) {
    ElMessage.error((error as Error).message || '获取文章列表失败')
  } finally {
    loading.value = false
  }
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

// 分页大小变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  loadArticles()
}

// 当前页码变化
const handleCurrentChange = (current: number) => {
  pagination.currentPage = current
  loadArticles()
}

// 页面加载时初始化数据
onMounted(() => {
  loadCategories()
  loadArticles()
})
</script>

<style scoped>
.knowledge-list {
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