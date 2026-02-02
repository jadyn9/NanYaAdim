<template>
  <MainLayout>
    <div class="dashboard-container">
      <el-card class="dashboard-card">
        <template #header>
          <div class="card-header">
            <el-icon><DataAnalysis /></el-icon>
            <span>系统仪表盘</span>
          </div>
        </template>
        
        <div class="dashboard-content">
          <!-- 统计卡片 -->
          <div class="stats-section">
            <el-row :gutter="20">
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon bg-primary">
                      <el-icon><Document /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.archives }}</div>
                      <div class="stat-label">档案总数</div>
                      <div class="stat-change positive">+12% 本月</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon bg-success">
                      <el-icon><Reading /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.articles }}</div>
                      <div class="stat-label">知识文章</div>
                      <div class="stat-change positive">+8% 本月</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon bg-warning">
                      <el-icon><User /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.users }}</div>
                      <div class="stat-label">活跃用户</div>
                      <div class="stat-change positive">+5% 本月</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="6">
                <el-card class="stat-card">
                  <div class="stat-content">
                    <div class="stat-icon bg-danger">
                      <el-icon><View /></el-icon>
                    </div>
                    <div class="stat-info">
                      <div class="stat-number">{{ stats.views }}</div>
                      <div class="stat-label">总访问量</div>
                      <div class="stat-change positive">+15% 本月</div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          
          <!-- 图表区域 -->
          <div class="charts-section">
            <el-row :gutter="20">
              <!-- 左侧图表 -->
              <el-col :span="12">
                <el-card class="chart-card">
                  <template #header>
                    <span>档案分类分布</span>
                  </template>
                  <div class="chart-container">
                    <!-- 这里将使用图表库渲染饼图 -->
                    <div class="chart-placeholder">
                      <el-icon class="chart-icon"><PieChart /></el-icon>
                      <p>档案分类分布饼图</p>
                      <ul class="chart-data-list">
                        <li v-for="item in archiveDistribution" :key="item.name">
                          <span class="data-name">{{ item.name }}</span>
                          <span class="data-value">{{ item.value }} ({{ item.percentage }}%)</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </el-card>
              </el-col>
              
              <!-- 右侧图表 -->
              <el-col :span="12">
                <el-card class="chart-card">
                  <template #header>
                    <span>最近30天数据趋势</span>
                  </template>
                  <div class="chart-container">
                    <!-- 这里将使用图表库渲染折线图 -->
                    <div class="chart-placeholder">
                      <el-icon class="chart-icon"><LineChart /></el-icon>
                      <p>最近30天数据趋势图</p>
                      <div class="trend-chart">
                        <div class="trend-item" v-for="(item, index) in recentTrends" :key="index">
                          <span class="trend-date">{{ item.date }}</span>
                          <div class="trend-bar-container">
                            <div class="trend-bar" :style="{ height: item.value + '%' }"></div>
                          </div>
                          <span class="trend-value">{{ item.value }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          
          <!-- 最近活动 -->
          <div class="activity-section">
            <el-card class="activity-card">
              <template #header>
                <div class="activity-header">
                  <span>最近活动</span>
                  <el-button type="primary" size="small">查看全部</el-button>
                </div>
              </template>
              <div class="activity-list">
                <el-timeline>
                  <el-timeline-item 
                    v-for="(item, index) in recentActivities" 
                    :key="index"
                    :timestamp="item.time"
                    :type="item.type"
                  >
                    <div class="activity-item">
                      <div class="activity-title">{{ item.title }}</div>
                      <div class="activity-desc">{{ item.description }}</div>
                      <div class="activity-user">{{ item.user }}</div>
                    </div>
                  </el-timeline-item>
                </el-timeline>
              </div>
            </el-card>
          </div>
        </div>
      </el-card>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { DataAnalysis, Document, Reading, User, View, PieChart, LineChart } from '@element-plus/icons-vue'
import MainLayout from '@/components/layout/MainLayout.vue'

// 统计数据
const stats = reactive({
  archives: 128,
  articles: 89,
  users: 24,
  views: 1256
})

// 档案分类分布
const archiveDistribution = reactive([
  { name: '人事档案', value: 45, percentage: 35 },
  { name: '财务档案', value: 32, percentage: 25 },
  { name: '项目档案', value: 28, percentage: 22 },
  { name: '合同档案', value: 23, percentage: 18 }
])

// 最近30天数据趋势
const recentTrends = reactive([
  { date: '1月20日', value: 65 },
  { date: '1月22日', value: 72 },
  { date: '1月24日', value: 58 },
  { date: '1月26日', value: 85 },
  { date: '1月28日', value: 92 },
  { date: '1月30日', value: 78 },
  { date: '2月1日', value: 95 }
])

// 最近活动
const recentActivities = reactive([
  {
    time: '2026-02-01 14:30',
    type: 'primary',
    title: '创建档案',
    description: '创建了新的员工档案：张三',
    user: '管理员'
  },
  {
    time: '2026-02-01 13:15',
    type: 'success',
    title: '编辑知识',
    description: '更新了文章：企业规章制度',
    user: '管理员'
  },
  {
    time: '2026-02-01 11:20',
    type: 'warning',
    title: '删除档案',
    description: '删除了过期档案：2023年度报告',
    user: '管理员'
  },
  {
    time: '2026-02-01 10:05',
    type: 'info',
    title: '创建知识',
    description: '创建了新文章：系统使用指南',
    user: '管理员'
  }
])

// 页面加载时获取数据
onMounted(() => {
  // 这里可以调用API获取真实数据
  console.log('加载仪表盘数据')
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-card {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.dashboard-card:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 统计卡片 */
.stats-section {
  margin-bottom: 30px;
}

.stat-card {
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8));
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.bg-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-icon.bg-success {
  background: linear-gradient(135deg, #67c23a, #85ce61);
}

.stat-icon.bg-warning {
  background: linear-gradient(135deg, #e6a23c, #f7ba2a);
}

.stat-icon.bg-danger {
  background: linear-gradient(135deg, #f56c6c, #f78989);
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.stat-change {
  font-size: 12px;
  font-weight: 500;
}

.stat-change.positive {
  color: #67c23a;
}

.stat-change.negative {
  color: #f56c6c;
}

/* 图表区域 */
.charts-section {
  margin-bottom: 30px;
}

.chart-card {
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8));
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.chart-container {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: #909399;
}

.chart-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.chart-data-list {
  list-style: none;
  padding: 0;
  margin: 20px 0 0 0;
  width: 100%;
  max-width: 200px;
  text-align: left;
}

.chart-data-list li {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.data-name {
  font-size: 14px;
}

.data-value {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

/* 趋势图表 */
.trend-chart {
  display: flex;
  align-items: end;
  gap: 8px;
  height: 120px;
  margin-top: 20px;
  padding: 0 20px;
  width: 100%;
}

.trend-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.trend-date {
  font-size: 10px;
  color: #909399;
  transform: rotate(-45deg);
  white-space: nowrap;
}

.trend-bar-container {
  flex: 1;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 4px 4px 0 0;
  display: flex;
  align-items: end;
  overflow: hidden;
}

.trend-bar {
  width: 100%;
  background: linear-gradient(180deg, #667eea, #764ba2);
  border-radius: 4px 4px 0 0;
  transition: height 0.5s ease;
}

.trend-value {
  font-size: 10px;
  color: #303133;
  font-weight: 500;
}

/* 最近活动 */
.activity-section {
  margin-bottom: 30px;
}

.activity-card {
  border-radius: 12px;
  background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8));
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-list {
  padding: 20px 0;
}

.activity-item {
  padding: 16px;
  background-color: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  margin-left: 20px;
  border-left: 3px solid #667eea;
}

.activity-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.activity-desc {
  font-size: 12px;
  color: #606266;
  margin-bottom: 8px;
}

.activity-user {
  font-size: 11px;
  color: #909399;
}

/* 暗色主题样式 */
.dark-theme .dashboard-card {
  background-color: rgba(45, 45, 45, 0.9);
  border-color: rgba(64, 64, 64, 0.5);
}

.dark-theme .stat-card {
  background: linear-gradient(rgba(45, 45, 45, 0.9), rgba(58, 58, 58, 0.8));
  border-color: rgba(80, 80, 80, 0.6);
}

.dark-theme .stat-number {
  color: #e0e0e0;
}

.dark-theme .stat-label {
  color: #b0b0b0;
}

.dark-theme .chart-card {
  background: linear-gradient(rgba(45, 45, 45, 0.9), rgba(58, 58, 58, 0.8));
  border-color: rgba(80, 80, 80, 0.6);
}

.dark-theme .chart-placeholder {
  color: #b0b0b0;
}

.dark-theme .data-name {
  color: #b0b0b0;
}

.dark-theme .data-value {
  color: #e0e0e0;
}

.dark-theme .trend-date {
  color: #808080;
}

.dark-theme .trend-bar-container {
  background-color: rgba(255, 255, 255, 0.1);
}

.dark-theme .trend-value {
  color: #e0e0e0;
}

.dark-theme .activity-card {
  background: linear-gradient(rgba(45, 45, 45, 0.9), rgba(58, 58, 58, 0.8));
  border-color: rgba(80, 80, 80, 0.6);
}

.dark-theme .activity-item {
  background-color: rgba(64, 64, 64, 0.6);
  border-left-color: #409eff;
}

.dark-theme .activity-title {
  color: #e0e0e0;
}

.dark-theme .activity-desc {
  color: #b0b0b0;
}

.dark-theme .activity-user {
  color: #808080;
}

/* 响应式设计 */
@media screen and (max-width: 1200px) {
  .stats-section .el-col {
    :span: 8;
  }
  
  .charts-section .el-col {
    :span: 24;
    margin-bottom: 20px;
  }
}

@media screen and (max-width: 768px) {
  .dashboard-container {
    padding: 10px;
  }
  
  .stats-section .el-col {
    :span: 12;
    margin-bottom: 16px;
  }
  
  .stat-content {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .activity-item {
    margin-left: 10px;
    padding: 12px;
  }
}
</style>