<template>
  <!-- 登录页面容器 -->
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
  
          <div class="mission-statement">
            <p>致力于解决医院内部需求和数据整合</p>
            <p>好的创意需求,请联系信息科反馈</p>
          </div>
        </div>
      </div>
      <!-- 右侧登录表单区域 -->
      <div class="login-form-section">
        <!-- 登录表单包装器 -->
        <div class="login-form-wrapper">
          <!-- 登录logo和标题，以及版本号 -->
          <div class="login-logo">
            <h1 class="text-2xl font-bold">南雅医院</h1>
            <span class="text-sm text-gray-200 ml-2">版本：v1.0.0</span>
            <p class="text-gray-600">企业后台管理系统</p>
          </div>
          <!-- 登录表单 -->
          <el-form
            :model="loginForm"
            :rules="loginRules"
            ref="loginFormRef"
            class="login-form"
            @keyup.enter="login"
          >
            <!-- 用户名输入框 -->
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="用户名"
                :prefix-icon="User"
                size="large"
                class="form-input"
              ></el-input>
            </el-form-item>
            <!-- 密码输入框 -->
            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="密码"
                :prefix-icon="Lock"
                show-password
                size="large"
                class="form-input"
              ></el-input>
            </el-form-item>
            <!-- 记住我和忘记密码 -->
            <el-form-item>
              <div class="form-footer">
                <el-checkbox v-model="loginForm.remember" size="large">
                  记住我
                  </el-checkbox>
                <el-link type="primary" underline="never" class="forgot-password">
                  忘记密码？
                </el-link>
              <!-- 版 -->
              </div>
            </el-form-item>
            <!-- 登录按钮 -->
            <el-form-item>
              <el-button
                type="primary"
                class="login-btn"
                :loading="loading"
                @click="login"
                size="large"
              >
                登录
              </el-button>
            </el-form-item>
            <!-- 注册链接 -->
            <el-form-item class="register-link">
              <span>还没有账号？</span>
              <el-link type="primary" underline="never" @click="goToRegister">
                立即注册
              </el-link>
            </el-form-item>
             <!-- 开发年份，联系邮箱，联系QQ，联系电话 -->  
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
import { User, Lock, Sunny, Moon } from '@element-plus/icons-vue'

// 导入主题store
import { useThemeStore } from '@/stores/theme'

// 导入认证API
import { authApi } from '@/services/api'

// 创建路由实例
const router = useRouter()

// 创建表单引用，用于表单验证
const loginFormRef = ref()

// 创建加载状态，用于控制登录按钮的加载动画
const loading = ref(false)

// 初始化主题store
const themeStore = useThemeStore()

// 计算属性，判断是否为暗色主题
const isDarkTheme = computed(() => themeStore.isDarkTheme)

// 切换主题方法
const toggleTheme = () => {
  themeStore.toggleTheme()
}

// 登录表单数据，使用reactive创建响应式对象
const loginForm = reactive({
  username: 'admin', // 用户名
  password: 'admin123', // 密码
  remember: false // 记住我
})

// 页面加载时处理记住我功能和初始化主题
onMounted(() => {
  // 初始化主题
  themeStore.initTheme()
  
  // 从localStorage获取记住的用户信息
  const rememberedUser = localStorage.getItem('rememberedUser')
  if (rememberedUser) {
    // 如果有记住的用户信息，填充到登录表单
    loginForm.username = rememberedUser
    loginForm.remember = true
  }
})

// 登录验证规则
const loginRules = {
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
  ]
}

// 登录函数
const login = async () => {
  try {
    // 检查表单引用是否存在
    if (!loginFormRef.value) {
      ElMessage.error('表单初始化失败，请刷新页面重试')
      return
    }
    
    // 验证表单数据
    await loginFormRef.value.validate()
    
    // 设置加载状态为true，显示登录按钮的加载动画
    loading.value = true
    
    console.log('登录表单验证通过，开始处理登录请求')
    
    // 调用真实的登录API
    const response = await authApi.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    // 登录成功的逻辑
    console.log('登录成功，准备存储token并跳转')
    
    // 存储token到本地存储
    localStorage.setItem('token', response.access_token)
    console.log('token已存储到localStorage:', response.access_token)
    
    // 处理记住我功能
    if (loginForm.remember) {
      localStorage.setItem('rememberedUser', loginForm.username)
    } else {
      localStorage.removeItem('rememberedUser')
    }
    
    // 先执行路由跳转，再清除表单数据和显示成功消息
    console.log('准备跳转到首页')
    
    // 确认token已经存储成功
    const storedToken = localStorage.getItem('token')
    console.log('存储的token:', storedToken)
    
    if (storedToken) {
      // 直接执行路由跳转
      router.push('/home').then(() => {
        console.log('路由跳转成功')
        
        // 清除表单数据
        loginForm.username = ''
        loginForm.password = ''
        loginForm.remember = false
        
        // 显示成功消息
        ElMessage.success('登录成功')
        
        // 重置loading状态
        loading.value = false
      }).catch((error) => {
        console.error('路由跳转失败:', error)
        ElMessage.error('跳转失败，请重试')
        
        // 重置loading状态
        loading.value = false
      })
    } else {
      console.error('token存储失败')
      ElMessage.error('登录失败，请重试')
      loading.value = false
    }
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error((error as Error).message || '用户名或密码错误，请重新输入')
    loading.value = false
  }
}

// 跳转到注册页函数
const goToRegister = () => {
  // 跳转到注册页面
  router.push('/auth/register')
}
</script>

<style>
/* 全局样式重置，确保全屏显示 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

#app {
  width: 100%;
  height: 100%;
}
</style>

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
  /* 使命宣言文字颜色 */
  color: #ffffff;
  /* 文字阴影 */
  text-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  /* 添加字体大小; */
  font-size: 25px;
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