<template>
  <MainLayout>
    <div class="profile-container">
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <el-icon><User /></el-icon>
            <span>个人信息</span>
          </div>
        </template>
        
        <div class="profile-content">
          <!-- 头像设置 -->
          <div class="avatar-section">
            <el-avatar size="large" :src="userInfo.avatar"></el-avatar>
            <el-button type="primary" size="small" class="avatar-upload-btn" @click="avatarUploadDialogVisible = true">
              更换头像
            </el-button>
          </div>
          
          <!-- 用户信息表单 -->
          <el-form ref="userFormRef" :model="userInfo" class="user-info-form">
            <el-form-item label="用户名">
              <el-input v-model="userInfo.username" disabled></el-input>
            </el-form-item>
            
            <el-form-item label="姓名">
              <el-input v-model="userInfo.name"></el-input>
            </el-form-item>
            
            <el-form-item label="邮箱">
              <el-input v-model="userInfo.email" type="email"></el-input>
            </el-form-item>
            
            <el-form-item label="手机号">
              <el-input v-model="userInfo.phone"></el-input>
            </el-form-item>
            
            <el-form-item label="部门">
              <el-input v-model="userInfo.department" disabled></el-input>
            </el-form-item>
            
            <el-form-item label="职位">
              <el-input v-model="userInfo.position"></el-input>
            </el-form-item>
            
            <el-form-item label="入职时间">
              <el-date-picker v-model="userInfo.joinDate" type="date" placeholder="选择日期" disabled></el-date-picker>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveUserInfo">保存修改</el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
      
      <!-- 头像上传对话框 -->
      <el-dialog v-model="avatarUploadDialogVisible" title="更换头像" width="400px">
        <div class="avatar-upload-container">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :on-change="handleAvatarChange"
            :before-upload="beforeAvatarUpload"
          >
            <img v-if="userInfo.avatar" :src="userInfo.avatar" class="avatar">
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="avatar-tip">
            请上传JPG、PNG格式的图片，大小不超过2MB
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="avatarUploadDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmAvatarUpload">确认</el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Plus } from '@element-plus/icons-vue'
import MainLayout from '@/components/layout/MainLayout.vue'

// 个人信息表单引用
const userFormRef = ref()

// 头像上传对话框可见性
const avatarUploadDialogVisible = ref(false)

// 用户信息
const userInfo = reactive({
  username: 'admin',
  name: '管理员',
  email: 'admin@example.com',
  phone: '13800138000',
  department: '技术部',
  position: '系统管理员',
  joinDate: '2024-01-01',
  avatar: ''
})

// 临时头像URL
const tempAvatar = ref('')

// 页面加载时获取用户信息
onMounted(() => {
  loadUserInfo()
})

// 加载用户信息
const loadUserInfo = () => {
  // 这里应该调用API获取用户信息
  // 模拟从localStorage获取
  const savedUserInfo = localStorage.getItem('userInfo')
  if (savedUserInfo) {
    const parsedUserInfo = JSON.parse(savedUserInfo)
    Object.assign(userInfo, parsedUserInfo)
  }
  
  // 从localStorage获取头像
  const savedAvatar = localStorage.getItem('userAvatar')
  if (savedAvatar) {
    userInfo.avatar = savedAvatar
  }
}

// 保存用户信息
const saveUserInfo = () => {
  // 这里应该调用API保存用户信息
  // 模拟保存到localStorage
  localStorage.setItem('userInfo', JSON.stringify(userInfo))
  
  ElMessage.success('保存成功')
}

// 重置表单
const resetForm = () => {
  loadUserInfo()
}

// 处理头像上传
const handleAvatarChange = (file: any) => {
  // 生成预览URL
  const reader = new FileReader()
  reader.readAsDataURL(file.raw)
  reader.onload = (e) => {
    tempAvatar.value = e.target?.result as string
  }
}

// 头像上传前验证
const beforeAvatarUpload = (file: any) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isJPG) {
    ElMessage.error('请上传JPG或PNG格式的图片')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB')
    return false
  }
  return true
}

// 确认头像上传
const confirmAvatarUpload = () => {
  if (tempAvatar.value) {
    userInfo.avatar = tempAvatar.value
    // 保存到localStorage
    localStorage.setItem('userAvatar', tempAvatar.value)
    avatarUploadDialogVisible.value = false
    ElMessage.success('头像更新成功')
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-card {
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

.profile-content {
  padding: 20px 0;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e6e6e6;
}

.avatar-section .el-avatar {
  width: 100px;
  height: 100px;
  border: 2px solid #f0f0f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.avatar-upload-btn {
  margin-top: 10px;
}

.user-info-form {
  max-width: 600px;
}

.user-info-form .el-form-item {
  margin-bottom: 20px;
}

/* 头像上传对话框样式 */
.avatar-upload-container {
  text-align: center;
  padding: 20px 0;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 32px;
  color: #c0c4cc;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}

.avatar-tip {
  margin-top: 12px;
  font-size: 12px;
  color: #909399;
}

/* 响应式设计 */
@media screen and (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }
  
  .avatar-section {
    flex-direction: column;
    text-align: center;
  }
  
  .user-info-form {
    max-width: 100%;
  }
}
</style>