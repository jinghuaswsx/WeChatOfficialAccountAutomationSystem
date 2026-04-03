<template>
  <el-menu :default-active="$route.path" router class="sidebar-menu">
    <el-menu-item index="/">
      <el-icon><Monitor /></el-icon>
      <span>仪表盘</span>
    </el-menu-item>
    <el-menu-item index="/key-points">
      <el-icon><List /></el-icon>
      <span>要点管理</span>
    </el-menu-item>
    <el-menu-item index="/workbench">
      <el-icon><Edit /></el-icon>
      <span>文章工作台</span>
    </el-menu-item>
    <el-menu-item index="/score-publish">
      <el-icon><DataAnalysis /></el-icon>
      <span>评分与发布</span>
    </el-menu-item>
    <el-menu-item index="/style">
      <el-icon><MagicStick /></el-icon>
      <span>风格管理</span>
    </el-menu-item>
    <el-menu-item index="/settings">
      <el-icon><Setting /></el-icon>
      <span>系统设置</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup lang="ts">
import { Monitor, List, Edit, DataAnalysis, MagicStick, Setting } from '@element-plus/icons-vue'
</script>
