<template>
  <MainLayout>
    <el-card class="home-card">
      <template #header>
        <div class="card-header">
          <span>系统概览</span>
        </div>
      </template>
      <div class="home-stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">128</div>
                <div class="stat-label">档案总数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">89</div>
                <div class="stat-label">知识文章</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">24</div>
                <div class="stat-label">用户数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-number">12</div>
                <div class="stat-label">今日新增</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div class="home-recent">
        <h3>最近操作</h3>
        <el-table :data="recentActivities" style="width: 100%">
          <el-table-column prop="time" label="时间" width="180"></el-table-column>
          <el-table-column prop="user" label="用户" width="120"></el-table-column>
          <el-table-column prop="action" label="操作" width="180"></el-table-column>
          <el-table-column prop="detail" label="详情"></el-table-column>
        </el-table>
      </div>
    </el-card>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/components/layout/MainLayout.vue'

// 最近操作数据
const recentActivities = [
  {
    time: '2024-01-29 14:30',
    user: '管理员',
    action: '创建档案',
    detail: '创建了新的员工档案：张三'
  },
  {
    time: '2024-01-29 13:15',
    user: '管理员',
    action: '编辑知识',
    detail: '更新了文章：企业规章制度'
  },
  {
    time: '2024-01-29 11:20',
    user: '管理员',
    action: '删除档案',
    detail: '删除了过期档案：2023年度报告'
  },
  {
    time: '2024-01-29 10:05',
    user: '管理员',
    action: '创建知识',
    detail: '创建了新文章：系统使用指南'
  }
]
</script>

<style scoped>
.home-card {
  margin-bottom: 20px;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.home-card:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.home-stats {
  margin-bottom: 30px;
}

.stat-card {
  height: 120px;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.6));
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
  transform: translateY(-4px);
}

.stat-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.home-recent {
  margin-top: 30px;
}

.home-recent h3 {
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 500;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 表格样式 */
:deep(.el-table) {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(8px);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

:deep(.el-table th) {
  background-color: rgba(102, 126, 234, 0.1);
  color: #303133;
}

:deep(.el-table tr:hover) {
  background-color: rgba(102, 126, 234, 0.05);
}
</style>