<template>
  <div class="login-container">
    <el-form :model="form" label-width="80px" @submit.prevent="handleSubmit">
      <h2>用户登录</h2>
      <el-form-item label="用户名">
        <el-input v-model="form.username" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const form = reactive({
  username: '',
  password: ''
})

const handleSubmit = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/login', form)
    if (response.data.success) {
      ElMessage.success(response.data.message)
      // 这里可以跳转到主页
    } else {
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    ElMessage.error('登录请求失败')
  }
}
</script>

<style scoped>
.login-container {
  width: 400px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
