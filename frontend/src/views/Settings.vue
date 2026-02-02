<template>
  <MainLayout>
    <div class="settings-container">
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <el-icon><Setting /></el-icon>
            <span>系统设置</span>
          </div>
        </template>
        
        <div class="settings-content">
          <!-- 设置选项卡 -->
          <el-tabs v-model="activeTab">
            <!-- 账号设置 -->
            <el-tab-pane label="账号设置" name="account">
              <el-form ref="accountFormRef" :model="accountSettings" class="settings-form">
                <el-form-item label="当前密码">
                  <el-input v-model="accountSettings.currentPassword" type="password"></el-input>
                </el-form-item>
                
                <el-form-item label="新密码">
                  <el-input v-model="accountSettings.newPassword" type="password"></el-input>
                </el-form-item>
                
                <el-form-item label="确认密码">
                  <el-input v-model="accountSettings.confirmPassword" type="password"></el-input>
                </el-form-item>
                
                <el-form-item>
                  <el-button type="primary" @click="changePassword">修改密码</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <!-- 通知设置 -->
            <el-tab-pane label="通知设置" name="notification">
              <el-form ref="notificationFormRef" :model="notificationSettings" class="settings-form">
                <el-form-item label="邮件通知">
                  <el-switch v-model="notificationSettings.emailNotification" active-text="开启" inactive-text="关闭"></el-switch>
                </el-form-item>
                
                <el-form-item label="短信通知">
                  <el-switch v-model="notificationSettings.smsNotification" active-text="开启" inactive-text="关闭"></el-switch>
                </el-form-item>
                
                <el-form-item label="系统通知">
                  <el-switch v-model="notificationSettings.systemNotification" active-text="开启" inactive-text="关闭"></el-switch>
                </el-form-item>
                
                <el-form-item label="通知接收邮箱" :disabled="!notificationSettings.emailNotification">
                  <el-input v-model="notificationSettings.notificationEmail" :disabled="!notificationSettings.emailNotification"></el-input>
                </el-form-item>
                
                <el-form-item>
                  <el-button type="primary" @click="saveNotificationSettings">保存设置</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <!-- 界面设置 -->
            <el-tab-pane label="界面设置" name="interface">
              <el-form ref="interfaceFormRef" :model="interfaceSettings" class="settings-form">
                <el-form-item label="主题">
                  <el-select v-model="interfaceSettings.theme">
                    <el-option label="默认主题" value="default"></el-option>
                    <el-option label="暗色主题" value="dark"></el-option>
                  </el-select>
                </el-form-item>
                
                <el-form-item label="语言">
                  <el-select v-model="interfaceSettings.language">
                    <el-option label="简体中文" value="zh-CN"></el-option>
                    <el-option label="English" value="en-US"></el-option>
                  </el-select>
                </el-form-item>
                
                <el-form-item label="菜单折叠">
                  <el-switch v-model="interfaceSettings.menuCollapse" active-text="开启" inactive-text="关闭"></el-switch>
                </el-form-item>
                
                <el-form-item label="侧边栏宽度">
                  <el-slider v-model="interfaceSettings.sidebarWidth" :min="180" :max="250" :step="10"></el-slider>
                  <span class="slider-value">{{ interfaceSettings.sidebarWidth }}px</span>
                </el-form-item>
                
                <el-form-item>
                  <el-button type="primary" @click="saveInterfaceSettings">保存设置</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            
            <!-- 系统信息 -->
            <el-tab-pane label="系统信息" name="system">
              <div class="system-info">
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="系统版本">
                    {{ systemInfo.version }}
                  </el-descriptions-item>
                  <el-descriptions-item label="更新时间">
                    {{ systemInfo.updateTime }}
                  </el-descriptions-item>
                  <el-descriptions-item label="开发团队">
                    {{ systemInfo.devTeam }}
                  </el-descriptions-item>
                  <el-descriptions-item label="技术栈">
                    {{ systemInfo.techStack }}
                  </el-descriptions-item>
                  <el-descriptions-item label="服务器环境">
                    {{ systemInfo.serverEnv }}
                  </el-descriptions-item>
                  <el-descriptions-item label="数据库">
                    {{ systemInfo.database }}
                  </el-descriptions-item>
                </el-descriptions>
                
                <div class="system-actions">
                  <el-button type="primary" size="small" @click="checkUpdate">检查更新</el-button>
                  <el-button size="small" @click="exportSettings">导出设置</el-button>
                  <el-button size="small" @click="importSettingsDialogVisible = true">导入设置</el-button>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-card>
      
      <!-- 导入设置对话框 -->
      <el-dialog v-model="importSettingsDialogVisible" title="导入设置" width="400px">
        <div class="import-container">
          <el-upload
            class="import-uploader"
            action="#"
            :show-file-list="false"
            :on-change="handleImportFile"
            accept=".json"
          >
            <el-button type="primary">选择设置文件</el-button>
          </el-upload>
          <div class="import-tip">
            请选择之前导出的设置文件（JSON格式）
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="importSettingsDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmImportSettings" :disabled="!importFile">确认导入</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Setting } from '@element-plus/icons-vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import { useThemeStore } from '@/stores/theme'

// 当前激活的选项卡
const activeTab = ref('account')

// 账号设置表单引用
const accountFormRef = ref()
// 通知设置表单引用
const notificationFormRef = ref()
// 界面设置表单引用
const interfaceFormRef = ref()

// 导入设置对话框可见性
const importSettingsDialogVisible = ref(false)
// 导入的文件
const importFile = ref<any>(null)

// 初始化主题store
const themeStore = useThemeStore()

// 账号设置
const accountSettings = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 通知设置
const notificationSettings = reactive({
  emailNotification: true,
  smsNotification: false,
  systemNotification: true,
  notificationEmail: 'admin@example.com'
})

// 界面设置
const interfaceSettings = reactive({
  theme: themeStore.theme,
  language: 'zh-CN',
  menuCollapse: false,
  sidebarWidth: 200
})

// 系统信息
const systemInfo = reactive({
  version: '1.0.0',
  updateTime: '2024-01-20',
  devTeam: '技术开发部',
  techStack: 'Vue 3 + TypeScript + Element Plus + FastAPI',
  serverEnv: 'Development',
  database: 'SQLite'
})

// 监听主题变化，同步到主题store
watch(
  () => interfaceSettings.theme,
  (newTheme) => {
    themeStore.switchTheme(newTheme as 'default' | 'dark')
  }
)

// 页面加载时获取设置
onMounted(() => {
  loadSettings()
})

// 加载设置
const loadSettings = () => {
  // 这里应该调用API获取用户设置
  // 模拟从localStorage获取
  const savedNotificationSettings = localStorage.getItem('notificationSettings')
  if (savedNotificationSettings) {
    Object.assign(notificationSettings, JSON.parse(savedNotificationSettings))
  }
  
  const savedInterfaceSettings = localStorage.getItem('interfaceSettings')
  if (savedInterfaceSettings) {
    Object.assign(interfaceSettings, JSON.parse(savedInterfaceSettings))
  }
}

// 修改密码
const changePassword = () => {
  // 这里应该调用API修改密码
  if (!accountSettings.currentPassword) {
    ElMessage.error('请输入当前密码')
    return
  }
  
  if (!accountSettings.newPassword) {
    ElMessage.error('请输入新密码')
    return
  }
  
  if (accountSettings.newPassword !== accountSettings.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  // 模拟修改密码成功
  ElMessage.success('密码修改成功')
  
  // 清空表单
  accountSettings.currentPassword = ''
  accountSettings.newPassword = ''
  accountSettings.confirmPassword = ''
}

// 保存通知设置
const saveNotificationSettings = () => {
  // 这里应该调用API保存设置
  localStorage.setItem('notificationSettings', JSON.stringify(notificationSettings))
  ElMessage.success('通知设置保存成功')
}

// 保存界面设置
const saveInterfaceSettings = () => {
  // 这里应该调用API保存设置
  localStorage.setItem('interfaceSettings', JSON.stringify(interfaceSettings))
  ElMessage.success('界面设置保存成功')
}

// 检查更新
const checkUpdate = () => {
  ElMessage.info('当前已是最新版本')
}

// 导出设置
const exportSettings = () => {
  const settings = {
    notification: notificationSettings,
    interface: interfaceSettings
  }
  
  const settingsStr = JSON.stringify(settings, null, 2)
  const blob = new Blob([settingsStr], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `settings-${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
  
  ElMessage.success('设置导出成功')
}

// 处理导入文件
const handleImportFile = (file: any) => {
  importFile.value = file
  
  // 读取文件内容
  const reader = new FileReader()
  reader.readAsText(file.raw)
  reader.onload = (e) => {
    try {
      const settings = JSON.parse(e.target?.result as string)
      if (settings.notification) {
        Object.assign(notificationSettings, settings.notification)
      }
      if (settings.interface) {
        Object.assign(interfaceSettings, settings.interface)
      }
      ElMessage.success('设置文件解析成功')
    } catch (error) {
      ElMessage.error('设置文件格式错误')
      importFile.value = null
    }
  }
}

// 确认导入设置
const confirmImportSettings = () => {
  if (importFile.value) {
    saveNotificationSettings()
    saveInterfaceSettings()
    importSettingsDialogVisible.value = false
    ElMessage.success('设置导入成功')
  }
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.settings-card {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 500;
}

.settings-content {
  padding: 20px 0;
}

.settings-form {
  max-width: 600px;
}

.settings-form .el-form-item {
  margin-bottom: 20px;
}

.slider-value {
  margin-left: 12px;
  font-size: 14px;
  color: #606266;
}

.system-info {
  padding: 20px 0;
}

.system-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.import-container {
  padding: 20px 0;
}

.import-tip {
  margin-top: 12px;
  font-size: 12px;
  color: #909399;
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .settings-container {
    padding: 10px;
  }
  
  .settings-form {
    max-width: 100%;
  }
}
</style>