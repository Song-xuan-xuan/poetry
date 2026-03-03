<template>
  <div class="min-h-screen bg-sys-bg">
    <!-- Hero Section -->
    <div class="hero-section px-5 lg:px-0 pt-8 pb-6">
      <div class="content-container">
        <h1 class="poem-title text-[28px] lg:text-[36px] text-ink tracking-tight mb-1">诗词雅韵</h1>
        <p class="text-ink-light text-[15px] lg:text-[16px] font-normal">学诗 · 练诗 · 创诗</p>

        <!-- 搜索框 -->
        <div class="mt-5 max-w-lg">
          <div
            class="search-box flex items-center gap-3 px-4 py-3 bg-sys-bg-secondary rounded-apple cursor-pointer transition-shadow hover:shadow-apple"
            @click="onSearchFocus"
          >
            <van-icon name="search" color="#AEAEB2" size="18" />
            <span class="text-text-tertiary text-[15px]">搜诗句、作者、意象…</span>
          </div>
        </div>
      </div>
    </div>

    <div class="content-container">
      <!-- 功能入口 -->
      <div class="pb-4 grid grid-cols-3 md:grid-cols-6 gap-3">
        <div
          v-for="item in featureCards"
          :key="item.name"
          class="glass-card glass-card-hover flex flex-col items-center py-5 px-2 gap-2.5 cursor-pointer active:scale-[0.96] transition-all"
          @click="router.push(item.path)"
        >
          <div class="w-10 h-10 rounded-apple flex items-center justify-center" :class="item.bgClass">
            <component :is="item.icon" class="w-5 h-5" :class="item.iconClass" />
          </div>
          <span class="text-[13px] font-medium text-ink">{{ item.name }}</span>
        </div>
      </div>

      <!-- 诗词选粹 -->
      <div class="py-3 pb-8">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-[20px] lg:text-[24px] font-semibold text-ink">诗词选粹</h2>
          <button
            class="text-[13px] text-primary font-medium cursor-pointer"
            @click="router.push('/poems')"
          >
            查看全部
          </button>
        </div>

        <Loading v-if="loading" />

        <div v-else-if="poems.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          <PoemCard
            v-for="poem in poems.slice(0, 12)"
            :key="poem.id"
            :poem="poem"
            @click="goDetail"
          />
        </div>

        <EmptyState v-else message="暂无诗词数据" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { getAllPoems } from '@/api/poem'
import { usePoemStore } from '@/stores/poem'
import PoemCard from '@/components/poetry/PoemCard.vue'
import Loading from '@/components/common/Loading.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()
const poemStore = usePoemStore()

const searchQuery = ref('')
const poems = ref([])
const loading = ref(false)

// SVG icon components
const IconLibrary = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [h('path', { d: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z' }), h('path', { d: 'M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z' })]) }
const IconFlower = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [h('circle', { cx: '12', cy: '12', r: '3' }), h('path', { d: 'M12 7.5a4.5 4.5 0 1 1 4.5 4.5M12 7.5A4.5 4.5 0 1 0 7.5 12M12 7.5V9m-4.5 3a4.5 4.5 0 1 0 4.5 4.5M7.5 12H9m3 4.5a4.5 4.5 0 1 0 4.5-4.5M12 16.5V15m4.5-3a4.5 4.5 0 1 1-4.5-4.5M16.5 12H15' })]) }
const IconPen = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [h('path', { d: 'M12 20h9' }), h('path', { d: 'M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z' })]) }
const IconQuiz = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [h('path', { d: '9 11l3 3L22 4' }), h('path', { d: 'M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11' })]) }
const IconWand = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [h('path', { d: 'M15 4V2' }), h('path', { d: 'M15 16v-2' }), h('path', { d: 'M8 9h2' }), h('path', { d: 'M20 9h2' }), h('path', { d: 'M17.8 11.8L19 13' }), h('path', { d: 'M15 9h0' }), h('path', { d: 'M17.8 6.2L19 5' }), h('path', { d: 'M3 21l9-9' }), h('path', { d: 'M12.2 6.2L11 5' })]) }
const IconImage = { render: () => h('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [h('rect', { x: '3', y: '3', width: '18', height: '18', rx: '2', ry: '2' }), h('circle', { cx: '8.5', cy: '8.5', r: '1.5' }), h('polyline', { points: '21 15 16 10 5 21' })]) }

const featureCards = [
  { name: '诗词库', icon: IconLibrary, path: '/poems', bgClass: 'bg-primary/8', iconClass: 'text-primary' },
  { name: '飞花令', icon: IconFlower, path: '/challenge/chain', bgClass: 'bg-accent/8', iconClass: 'text-accent' },
  { name: '答题闯关', icon: IconQuiz, path: '/challenge/quiz', bgClass: 'bg-success/8', iconClass: 'text-success' },
  { name: '诗词创作', icon: IconPen, path: '/create', bgClass: 'bg-primary/8', iconClass: 'text-primary' },
  { name: '仿写工坊', icon: IconWand, path: '/create/mimic', bgClass: 'bg-accent/8', iconClass: 'text-accent' },
  { name: '诗画互生', icon: IconImage, path: '/create/image', bgClass: 'bg-success/8', iconClass: 'text-success' },
]

function onSearchFocus() {
  router.push('/search')
}

function goDetail(poem) {
  poemStore.setCurrentPoem(poem)
  router.push(`/poem/${poem.id}`)
}

onMounted(async () => {
  loading.value = true
  try {
    const data = await getAllPoems(1, 12)
    // 兼容两种返回格式：分页对象 {items, total} 或 旧版纯数组
    poems.value = Array.isArray(data) ? data.slice(0, 12) : (data?.items || [])
  } catch {
    poems.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.hero-section {
  background: linear-gradient(180deg, #FAFAF8 0%, #F2F1EF 100%);
}
</style>
