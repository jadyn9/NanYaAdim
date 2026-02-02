<template>
  <el-card class="register-card" shadow="hover">
    <template #header>
      <div class="register-header">
        <h2>企业管理系统</h2>
        <p>创建新账号</p>
      </div>
    </template>
    <el-form
      :model="registerForm"
      :rules="registerRules"
      ref="registerFormRef"
      class="register-form"
    >
      <el-form-item prop="username">
        <el-input
          v-model="registerForm.username"
          placeholder="用户名"
          prefix-icon="User"
        ></el-input>
      </el-form-item>
      <el-form-item prop="email">
        <el-input
          v-model="registerForm.email"
          placeholder="邮箱"
          prefix-icon="Message"
        ></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="registerForm.password"
          type="password"
          placeholder="密码"
          prefix-icon="Lock"
          show-password
        ></el-input>
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <el-input
          v-model="registerForm.confirmPassword"
          type="password"
          placeholder="确认密码"
          prefix-icon="Check"
          show-password
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          class="register-btn"
          :loading="loading"
          @click="register"
        >
          注册
        </el-button>
      </el-form-item>
      <el-form-item class="login-link">
        <span>已有账号？</span>
        <el-link type="primary" :underline="false" @click="goToLogin">立即登录</el-link>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const registerFormRef = ref()
const loading = ref(false)

// 注册表单
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 注册验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 注册
const register = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    // 模拟注册请求
    setTimeout(() => {
      // 这里应该是真实的注册API调用
      console.log('注册请求:', registerForm)
      
      // 注册成功后跳转到登录页
      router.push('/auth/login')
      
      ElMessage.success('注册成功，请登录')
      loading.value = false
    }, 1000)
  } catch (error) {
    console.error('注册验证失败', error)
    loading.value = false
  }
}

// 跳转到登录页
const goToLogin = () => {
  router.push('/auth/login')
}
</script>

<style scoped>
.register-card {
  width: 400px;
  border-radius: 8px;
  overflow: hidden;
}

.register-header {
  text-align: center;
  padding: 20px 0;
}

.register-header h2 {
  margin: 0 0 10px 0;
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.register-header p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.register-form {
  padding: 0 30px 30px 30px;
}

.register-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

.login-link {
  text-align: center;
  margin-top: 20px;
}

.login-link span {
  font-size: 14px;
  color: #606266;
}
</style>