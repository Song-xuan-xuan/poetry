<template>
  <header class="top-nav lg:hidden">
    <div class="top-nav-inner">
      <!-- Logo -->
      <div class="nav-brand" @click="go('/')">
        <div class="brand-icon">诗</div>
        <span class="brand-text">诗词雅韵</span>
      </div>

      <!-- Tab 切换 -->
      <nav class="nav-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.name"
          class="nav-tab"
          :class="{ active: activeTab === tab.name }"
          @click="go(tab.path)"
        >
          {{ tab.label }}
        </button>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const tabs = [
  { name: 'home', label: '鉴赏', path: '/' },
  { name: 'challenge', label: '挑战', path: '/challenge' },
  { name: 'create', label: '创作', path: '/create' }
]

const activeTab = computed(() => {
  if (route.path.startsWith('/challenge')) return 'challenge'
  if (route.path.startsWith('/create')) return 'create'
  return 'home'
})

function go(path) {
  router.push(path)
}
</script>

<style scoped>
.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.top-nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  height: 52px;
  background: rgba(250, 250, 248, 0.72);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.06);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.brand-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: linear-gradient(135deg, #c8851a, #e54d42);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-family: 'Noto Serif SC', 'KaiTi', '楷体', serif;
  font-size: 14px;
  font-weight: 600;
}

.brand-text {
  font-family: 'Noto Serif SC', 'KaiTi', '楷体', serif;
  font-size: 16px;
  font-weight: 600;
  color: #1D1D1F;
}

.nav-tabs {
  display: flex;
  gap: 4px;
  background: rgba(0, 0, 0, 0.04);
  border-radius: 10px;
  padding: 3px;
}

.nav-tab {
  padding: 5px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: #6E6E73;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.nav-tab.active {
  background: white;
  color: #1D1D1F;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.nav-tab:active {
  transform: scale(0.96);
}
</style>
