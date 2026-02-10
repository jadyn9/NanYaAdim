<template>
  <!-- 注册页面容器 -->
  <div class="login-container">
    <!-- 背景图案叠加层 -->
    <div class="login-bg"></div>
    <!-- 主题切换按钮 -->
    <div class="theme-toggle">
      <el-tooltip :content="isDarkTheme ? '切换到亮色主题' : '切换到暗色主题'" placement="bottom">
          <el-button 
            circle 
            size="small" 
            @click="toggleTheme"
            :title="isDarkTheme ? '切换到亮色主题' : '切换到暗色主题'"
          >
            {{ isDarkTheme ? '☀️' : '🌙' }}
          </el-button>
        </el-tooltip>
    </div>
    <!-- 登录内容区域 -->
    <div class="login-content">
      <!-- 左侧文字区域 -->
      <div class="login-text-section">
        <div class="text-content">
          <h1 class="main-title">南雅医院</h1>
          <p class="subtitle">企业后台管理系统</p>
          <div class="mission-statement">
            <p>致力于解决医院内部流程痛点需求和数据整合</p>
          </div>
        </div>
      </div>
      <!-- 右侧注册表单区域 -->
      <div class="login-form-section">
        <!-- 注册表单包装器 -->
        <div class="login-form-wrapper">
          <!-- 注册logo和标题，以及版本号 -->
          <div class="login-logo">
            <h1 class="text-2xl font-bold">南雅医院</h1>
            <span class="text-sm text-gray-200 ml-2">版本：v1.0.0</span>
            <p class="text-gray-600">企业后台管理系统</p>
          </div>
          <!-- 注册表单 -->
          <el-form
            :model="registerForm"
            :rules="registerRules"
            ref="registerFormRef"
            class="login-form"
            @keyup.enter="register"
          >
            <!-- 用户名输入框 -->
            <el-form-item prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="用户名"
                :prefix-icon="User"
                size="large"
                class="form-input"
              ></el-input>
            </el-form-item>
            <!-- 密码输入框 -->
            <el-form-item prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="密码"
                :prefix-icon="Lock"
                show-password
                size="large"
                class="form-input"
              ></el-input>
            </el-form-item>
            <!-- 确认密码输入框 -->
            <el-form-item prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="确认密码"
                :prefix-icon="Lock"
                show-password
                size="large"
                class="form-input"
              ></el-input>
            </el-form-item>
            <!-- 姓名输入框 -->
            <el-form-item prop="name">
              <el-input
                v-model="registerForm.name"
                placeholder="姓名"
                :prefix-icon="Avatar"
                size="large"
                class="form-input"
              ></el-input>
            </el-form-item>
            <!-- 邮箱输入框 -->
            <el-form-item prop="email">
              <el-input
                v-model="registerForm.email"
                placeholder="邮箱"
                :prefix-icon="Message"
                size="large"
                class="form-input"
              ></el-input>
            </el-form-item>
            <!-- 角色选择 -->
            <el-form-item prop="role_id">
              <el-select
                v-model="registerForm.role_id"
                placeholder="选择角色"
                size="large"
                class="form-input"
              >
                <el-option
                  label="管理员"
                  value="1"
                ></el-option>
                <el-option
                  label="普通用户"
                  value="2"
                ></el-option>
              </el-select>
            </el-form-item>
            <!-- 注册按钮 -->
            <el-form-item>
              <el-button
                type="primary"
                class="login-btn"
                :loading="loading"
                @click="register"
                size="large"
              >
                注册
              </el-button>
            </el-form-item>
            <!-- 登录链接 -->
            <el-form-item class="register-link">
              <span>已有账号？</span>
              <el-link type="primary" underline="never" @click="goToLogin">
                立即登录
              </el-link>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 导入Vue的ref和reactive函数，用于创建响应式数据
import { ref, reactive, onMounted, computed } from 'vue'

// 导入Vue Router的useRouter函数，用于路由跳转
import { useRouter } from 'vue-router'

// 导入Element Plus的消息组件，用于显示提示信息
import { ElMessage } from 'element-plus'

// 导入Element Plus的图标组件
import { User, Lock, Avatar, Message } from '@element-plus/icons-vue'

// 导入主题store
import { useThemeStore } from '@/stores/theme'

// 导入认证API
import { authApi } from '@/services/api'

// 创建路由实例
const router = useRouter()

// 创建表单引用，用于表单验证
const registerFormRef = ref()

// 创建加载状态，用于控制注册按钮的加载动画
const loading = ref(false)

// 初始化主题store
const themeStore = useThemeStore()

// 计算属性，判断是否为暗色主题
const isDarkTheme = computed(() => themeStore.isDarkTheme)

// 切换主题方法
const toggleTheme = () => {
  themeStore.toggleTheme()
}

// 注册表单数据，使用reactive创建响应式对象
const registerForm = reactive({
  username: '', // 用户名
  password: '', // 密码
  confirmPassword: '', // 确认密码
  name: '', // 姓名
  email: '', // 邮箱
  role_id: 2 // 角色ID，默认为普通用户
})

// 页面加载时处理主题初始化
onMounted(() => {
  // 初始化主题
  themeStore.initTheme()
})

// 注册验证规则
const registerRules = {
  username: [
    // 用户名必填验证
    { required: true, message: '请输入用户名', trigger: ['blur', 'change'] },
    // 用户名长度验证
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: ['blur', 'change'] }
  ],
  password: [
    // 密码必填验证
    { required: true, message: '请输入密码', trigger: ['blur', 'change'] },
    // 密码长度验证
    { min: 6, message: '密码长度至少6个字符', trigger: ['blur', 'change'] }
  ],
  confirmPassword: [
    // 确认密码必填验证
    { required: true, message: '请确认密码', trigger: ['blur', 'change'] },
    // 确认密码与密码一致验证
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: ['blur', 'change']
    }
  ],
  name: [
    // 姓名必填验证
    { required: true, message: '请输入姓名', trigger: ['blur', 'change'] }
  ],
  email: [
    // 邮箱必填验证
    { required: true, message: '请输入邮箱', trigger: ['blur', 'change'] },
    // 邮箱格式验证
    { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }
  ],
  role_id: [
    // 角色必填验证
    { required: true, message: '请选择角色', trigger: ['blur', 'change'] }
  ]
}

// 注册函数
const register = async () => {
  try {
    // 检查表单引用是否存在
    if (!registerFormRef.value) {
      ElMessage.error('表单初始化失败，请刷新页面重试')
      return
    }
    
    // 验证表单数据
    await registerFormRef.value.validate()
    
    // 设置加载状态为true，显示注册按钮的加载动画
    loading.value = true
    
    console.log('注册表单验证通过，开始处理注册请求')
    
    // 调用真实的注册API
    const response = await authApi.register({
      username: registerForm.username,
      password: registerForm.password,
      name: registerForm.name,
      email: registerForm.email,
      role_id: registerForm.role_id
    })
    
    // 注册成功的逻辑
    console.log('注册成功，准备跳转')
    
    // 显示成功消息
    ElMessage.success('注册成功，请登录')
    
    // 跳转到登录页面
    setTimeout(() => {
      router.push('/')
    }, 1500)
    
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error((error as Error).message || '注册失败，请重试')
  } finally {
    // 重置加载状态
    loading.value = false
  }
}

// 跳转到登录页函数
const goToLogin = () => {
  // 跳转到登录页面
  router.push('/')
}
</script>

<style scoped>
/* 登录页面容器 */
.login-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 背景渐变和图片 */
  background: linear-gradient(rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8)), url('/images/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  /* 确保在所有设备上都能全屏显示 */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
}

/* 主题切换按钮 */
.theme-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 2;
}

.theme-toggle .el-button {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.theme-toggle .el-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

/* 暗色主题下的登录表单包装器 */
.dark-theme .login-form-wrapper {
  background: rgba(45, 45, 45, 0.95);
  border-color: rgba(64, 64, 64, 0.5);
}

.dark-theme .login-logo h1 {
  color: #e0e0e0;
}

.dark-theme .login-logo p {
  color: #b0b0b0;
}

.dark-theme .el-form-item__label {
  color: #b0b0b0;
}

.dark-theme .el-input__wrapper {
  background-color: rgba(58, 58, 58, 0.9);
  border-color: rgba(64, 64, 64, 0.5);
}

.dark-theme .el-checkbox__label {
  color: #b0b0b0;
}

.dark-theme .register-link span {
  color: #b0b0b0;
}

.dark-theme .register-link .el-link {
  color: #409eff;
}

/* 暗色主题下的左侧文字 */
.dark-theme .main-title {
  color: #ffffff;
}

.dark-theme .subtitle {
  color: #e0e0e0;
}

.dark-theme .mission-statement p {
  color: #ffffff;
}

/* 背景图案叠加层 */
.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* SVG网格背景 */
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="none"/><path d="M10 10 L90 10 L90 90 L10 90 Z" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/></svg>');
  background-size: 100px 100px;
  opacity: 0.3;
}

/* 登录内容区域 - 左右布局 */
.login-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1200px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  gap: 60px;
}

/* 左侧文字区域 */
.login-text-section {
  flex: 1;
  max-width: 500px;
}

/* 文字内容 */
.text-content {
  color: white;
}

/* 主标题 */
.main-title {
  font-size: 42px;
  font-weight: bold;
  color: white;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* 副标题 */
.subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 40px 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* 使命宣言 */
.mission-statement {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 30px;
  border-left: 4px solid #ffffff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

/* 使命宣言悬停效果 */
.mission-statement:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(10px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

/* 使命宣言文字 */
.mission-statement p {
  font-size: 18px;
  line-height: 1.6;
  color: white;
  margin: 0;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* 右侧登录表单区域 */
.login-form-section {
  flex: 1;
  max-width: 480px;
}

/* 登录表单包装器 */
.login-form-wrapper {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 40px;
  transition: all 0.3s ease;
}

/* 登录表单包装器悬停效果 */
.login-form-wrapper:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
}

/* 登录logo区域 */
.login-logo {
  text-align: center;
  margin-bottom: 40px;
}

/* 登录logo标题 */
.login-logo h1 {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin: 0 0 8px 0;
}

/* 登录logo副标题 */
.login-logo p {
  font-size: 16px;
  color: #909399;
  margin: 0;
}

/* 登录表单 */
.login-form {
  width: 100%;
}

/* 表单输入框 */
.form-input {
  border-radius: 12px;
  transition: all 0.3s ease;
}

/* 表单输入框聚焦效果 */
.form-input:focus {
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

/* 表单底部区域 */
.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

/* 忘记密码链接 */
.forgot-password {
  font-size: 14px;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

/* 登录按钮悬停效果 */
.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

/* 登录按钮点击效果 */
.login-btn:active {
  transform: translateY(0);
}

/* 注册链接区域 */
.register-link {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
}

/* 注册链接文本 */
.register-link span {
  color: #606266;
}

/* 响应式设计 - 中等屏幕设备 */
@media screen and (max-width: 1024px) {
  .login-content {
    max-width: 90%;
    gap: 40px;
  }
  
  .main-title {
    font-size: 36px;
  }
  
  .subtitle {
    font-size: 18px;
  }
  
  .mission-statement p {
    font-size: 16px;
  }
  
  .login-form-wrapper {
    padding: 30px;
  }
}

/* 响应式设计 - 平板设备 */
@media screen and (max-width: 768px) {
  .login-content {
    flex-direction: column;
    gap: 30px;
    padding: 0 20px;
  }
  
  .login-text-section {
    max-width: 100%;
    text-align: center;
  }
  
  .login-form-section {
    max-width: 100%;
    width: 100%;
  }
  
  .main-title {
    font-size: 32px;
  }
  
  .subtitle {
    font-size: 16px;
    margin-bottom: 30px;
  }
  
  .mission-statement {
    padding: 24px;
  }
  
  .mission-statement p {
    font-size: 15px;
  }
  
  .login-form-wrapper {
    padding: 30px 20px;
  }
  
  .login-logo h1 {
    font-size: 24px;
  }
  
  .login-logo p {
    font-size: 14px;
  }
  
  .login-btn {
    height: 44px;
  }
  
  /* 优化背景图显示 */
  .login-container {
    background-attachment: scroll;
  }
}

/* 响应式设计 - 小屏幕平板和大屏手机 */
@media screen and (max-width: 640px) {
  .login-form-wrapper {
    padding: 28px 18px;
  }
  
  .login-logo {
    margin-bottom: 32px;
  }
  
  .login-logo h1 {
    font-size: 22px;
  }
  
  .form-input {
    height: 44px;
  }
  
  .main-title {
    font-size: 28px;
  }
  
  .subtitle {
    font-size: 15px;
  }
  
  .mission-statement {
    padding: 20px;
  }
  
  .mission-statement p {
    font-size: 14px;
  }
}

/* 响应式设计 - 手机设备 */
@media screen and (max-width: 480px) {
  .login-form-wrapper {
    padding: 24px 16px;
  }
  
  .login-logo {
    margin-bottom: 30px;
  }
  
  .login-logo h1 {
    font-size: 20px;
  }
  
  .login-logo p {
    font-size: 12px;
  }
  
  .form-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .forgot-password {
    align-self: flex-end;
  }
  
  .form-input {
    height: 42px;
  }
  
  .login-btn {
    height: 42px;
    font-size: 15px;
  }
  
  .main-title {
    font-size: 24px;
  }
  
  .subtitle {
    font-size: 14px;
    margin-bottom: 24px;
  }
  
  .mission-statement {
    padding: 18px;
  }
  
  .mission-statement p {
    font-size: 13px;
  }
}

/* 响应式设计 - 小屏手机设备 */
@media screen and (max-width: 360px) {
  .login-form-wrapper {
    padding: 20px 14px;
  }
  
  .login-logo {
    margin-bottom: 24px;
  }
  
  .login-logo h1 {
    font-size: 18px;
  }
  
  .login-logo p {
    font-size: 11px;
  }
  
  .register-link {
    font-size: 13px;
    margin-top: 20px;
  }
  
  .main-title {
    font-size: 20px;
  }
  
  .subtitle {
    font-size: 12px;
  }
  
  .mission-statement {
    padding: 16px;
  }
  
  .mission-statement p {
    font-size: 12px;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  .login-form-wrapper:hover {
    /* 移除触摸设备上的悬停效果 */
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transform: none;
  }
  
  .login-btn:hover {
    transform: none;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  }
  
  .mission-statement:hover {
    transform: none;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }
  
  /* 增大触摸目标 */
  .form-input {
    min-height: 44px;
  }
  
  .login-btn {
    min-height: 44px;
  }
  
  .forgot-password {
    padding: 8px 0;
  }
}
</style>