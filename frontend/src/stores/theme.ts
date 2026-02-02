import { defineStore } from 'pinia'

// 主题类型定义
type ThemeType = 'default' | 'dark'

// 定义主题store
export const useThemeStore = defineStore('theme', {
  state: () => ({
    // 当前主题
    currentTheme: 'default' as ThemeType
  }),
  
  getters: {
    // 获取当前主题
    theme: (state) => state.currentTheme,
    
    // 是否为暗色主题
    isDarkTheme: (state) => state.currentTheme === 'dark'
  },
  
  actions: {
    // 初始化主题
    initTheme() {
      // 从localStorage获取保存的主题
      const savedTheme = localStorage.getItem('theme') as ThemeType
      if (savedTheme) {
        this.currentTheme = savedTheme
        this.applyTheme(savedTheme)
      }
    },
    
    // 切换主题
    switchTheme(theme: ThemeType) {
      this.currentTheme = theme
      this.applyTheme(theme)
      // 保存主题到localStorage
      localStorage.setItem('theme', theme)
    },
    
    // 应用主题
    applyTheme(theme: ThemeType) {
      if (theme === 'dark') {
        document.documentElement.classList.add('dark-theme')
      } else {
        document.documentElement.classList.remove('dark-theme')
      }
    },
    
    // 切换到暗色主题
    setDarkTheme() {
      this.switchTheme('dark')
    },
    
    // 切换到默认主题
    setDefaultTheme() {
      this.switchTheme('default')
    },
    
    // 切换主题（切换到相反的主题）
    toggleTheme() {
      const newTheme = this.currentTheme === 'default' ? 'dark' : 'default'
      this.switchTheme(newTheme)
    }
  }
})
