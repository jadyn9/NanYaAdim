// API服务文件，处理与后端的通信

// API基础URL
const API_BASE_URL = 'http://localhost:8001'

// 请求超时时间
const REQUEST_TIMEOUT = 30000

// 请求头配置
const getHeaders = () => {
  const token = localStorage.getItem('token')
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  }
}

// 错误处理
const handleError = (error: any) => {
  console.error('API请求错误:', error)
  
  if (error.response) {
    // 服务器返回错误状态码
    const status = error.response.status
    const message = error.response.data?.detail || '请求失败'
    
    switch (status) {
      case 401:
        // 未授权，跳转到登录页
        localStorage.removeItem('token')
        window.location.href = '/'
        break
      case 403:
        return new Error('权限不足')
      case 404:
        return new Error('资源不存在')
      case 500:
        return new Error('服务器内部错误')
      default:
        return new Error(message)
    }
  } else if (error.request) {
    // 请求已发送但没有收到响应
    return new Error('网络错误，请检查网络连接')
  } else {
    // 请求配置出错
    return new Error('请求配置错误')
  }
}

// 通用请求方法
class ApiService {
  // GET请求
  async get<T>(url: string, params?: any): Promise<T> {
    try {
      const queryString = params ? '?' + new URLSearchParams(params).toString() : ''
      const response = await fetch(`${API_BASE_URL}${url}${queryString}`, {
        method: 'GET',
        headers: getHeaders(),
        signal: AbortSignal.timeout(REQUEST_TIMEOUT)
      })
      
      if (!response.ok) {
        throw { response }
      }
      
      return await response.json()
    } catch (error) {
      throw handleError(error)
    }
  }
  
  // POST请求
  async post<T>(url: string, data?: any, formData?: boolean): Promise<T> {
    try {
      const headers = formData ? {
        'Authorization': getHeaders()['Authorization']
      } : getHeaders();
      
      const response = await fetch(`${API_BASE_URL}${url}`, {
        method: 'POST',
        headers: headers,
        body: formData && data ? new URLSearchParams(data as Record<string, string>) : data ? JSON.stringify(data) : undefined,
        signal: AbortSignal.timeout(REQUEST_TIMEOUT)
      })
      
      if (!response.ok) {
        throw { response }
      }
      
      return await response.json()
    } catch (error) {
      throw handleError(error)
    }
  }
  
  // PUT请求
  async put<T>(url: string, data?: any): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}${url}`, {
        method: 'PUT',
        headers: getHeaders(),
        body: data ? JSON.stringify(data) : undefined,
        signal: AbortSignal.timeout(REQUEST_TIMEOUT)
      })
      
      if (!response.ok) {
        throw { response }
      }
      
      return await response.json()
    } catch (error) {
      throw handleError(error)
    }
  }
  
  // DELETE请求
  async delete<T>(url: string): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}${url}`, {
        method: 'DELETE',
        headers: getHeaders(),
        signal: AbortSignal.timeout(REQUEST_TIMEOUT)
      })
      
      if (!response.ok) {
        throw { response }
      }
      
      return await response.json()
    } catch (error) {
      throw handleError(error)
    }
  }
}

// 创建API服务实例
const apiService = new ApiService()

// 档案管理API
export const archiveApi = {
  // 获取档案列表
  getArchives: (params?: { page?: number; page_size?: number; name?: string; category_id?: string }) => {
    return apiService.get('/api/archive', params)
  },
  
  // 获取档案详情
  getArchive: (id: number) => {
    return apiService.get(`/api/archive/${id}`)
  },
  
  // 创建档案
  createArchive: (data: any) => {
    return apiService.post('/api/archive', data)
  },
  
  // 更新档案
  updateArchive: (id: number, data: any) => {
    return apiService.put(`/api/archive/${id}`, data)
  },
  
  // 删除档案
  deleteArchive: (id: number) => {
    return apiService.delete(`/api/archive/${id}`)
  },
  
  // 获取档案分类列表
  getCategories: () => {
    return apiService.get('/api/archive/category')
  },
  
  // 创建档案分类
  createCategory: (data: any) => {
    return apiService.post('/api/archive/category', data)
  },
  
  // 更新档案分类
  updateCategory: (id: number, data: any) => {
    return apiService.put(`/api/archive/category/${id}`, data)
  },
  
  // 删除档案分类
  deleteCategory: (id: number) => {
    return apiService.delete(`/api/archive/category/${id}`)
  }
}

// 知识库管理API
export const knowledgeApi = {
  // 获取文章列表
  getArticles: (params?: { page?: number; page_size?: number; title?: string; category_id?: string; tag?: string }) => {
    return apiService.get('/api/knowledge', params)
  },
  
  // 获取文章详情
  getArticle: (id: number) => {
    return apiService.get(`/api/knowledge/${id}`)
  },
  
  // 创建文章
  createArticle: (data: any) => {
    return apiService.post('/api/knowledge', data)
  },
  
  // 更新文章
  updateArticle: (id: number, data: any) => {
    return apiService.put(`/api/knowledge/${id}`, data)
  },
  
  // 删除文章
  deleteArticle: (id: number) => {
    return apiService.delete(`/api/knowledge/${id}`)
  },
  
  // 获取文章分类列表
  getCategories: () => {
    return apiService.get('/api/knowledge/category')
  },
  
  // 创建文章分类
  createCategory: (data: any) => {
    return apiService.post('/api/knowledge/category', data)
  },
  
  // 更新文章分类
  updateCategory: (id: number, data: any) => {
    return apiService.put(`/api/knowledge/category/${id}`, data)
  },
  
  // 删除文章分类
  deleteCategory: (id: number) => {
    return apiService.delete(`/api/knowledge/category/${id}`)
  }
}

// 认证API
export const authApi = {
  // 登录
  login: (data: { username: string; password: string }) => {
    return apiService.post('/api/auth/login', data, true)
  },
  
  // 注册
  register: (data: any) => {
    return apiService.post('/api/auth/register', data)
  },
  
  // 获取当前用户信息
  getCurrentUser: () => {
    return apiService.get('/api/auth/me')
  }
}

export default apiService