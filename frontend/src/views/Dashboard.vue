<template>
  <div class="dashboard">
    <el-menu default-active="1" class="el-menu-vertical-demo">
      <el-menu-item index="1">智能问答</el-menu-item>
      <el-menu-item index="2">学习规划</el-menu-item>
      <el-menu-item index="3">个人信息</el-menu-item>
    </el-menu>
    <div class="content">
      <h2>欢迎进入计算机网络实验课程系统</h2>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
}

.el-menu {
  width: 200px;
  height: 100vh;
}

.content {
  padding: 20px;
  flex: 1;
}
</style>
