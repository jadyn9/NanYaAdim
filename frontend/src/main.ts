// 导入Vue的createApp函数，用于创建Vue应用实例
import { createApp } from 'vue'

// 导入Pinia的createPinia函数，用于创建Pinia实例
import { createPinia } from 'pinia'

// 导入全局样式文件，包含Tailwind CSS基础样式
import './style.css'

// 导入根组件App.vue
import App from './App.vue'

// 导入路由配置
import router from './router'

// 导入Element Plus组件库
import ElementPlus from 'element-plus'

// 导入Element Plus的默认样式
import 'element-plus/dist/index.css'

// 导入Element Plus的中文语言包
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

// 导入主题store
import { useThemeStore } from './stores/theme'

// 创建Vue应用实例
const app = createApp(App)

// 创建并使用Pinia
const pinia = createPinia()
app.use(pinia)

// 使用路由插件
app.use(router)

// 使用Element Plus组件库，并配置为中文语言
app.use(ElementPlus, {
  locale: zhCn
})

// 初始化主题
const themeStore = useThemeStore()
themeStore.initTheme()

// 将Vue应用挂载到id为'app'的DOM元素上
app.mount('#app')