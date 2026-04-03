<template>
  <el-container class="app-container">
    <el-aside width="200px">
      <div class="logo">
        <h3>公众号自动化</h3>
      </div>
      <Sidebar />
    </el-aside>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
</script>

<style>
html, body, #app { margin: 0; padding: 0; height: 100%; }
.app-container { height: 100vh; }
.logo { padding: 20px; text-align: center; border-bottom: 1px solid #e6e6e6; }
.logo h3 { margin: 0; color: #409eff; }
.el-aside { background: #fff; border-right: 1px solid #e6e6e6; }
.sidebar-menu { border-right: none; }
</style>
