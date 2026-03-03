<template>
  <div class="min-h-screen bg-sys-bg">
    <!-- 页面标题 -->
    <div class="content-container pt-4 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button class="text-ink-light lg:hidden" @click="router.back()">
          <van-icon name="arrow-left" size="20" />
        </button>
        <h1 class="text-[24px] lg:text-[32px] font-semibold text-ink tracking-tight">诗词库</h1>
      </div>
    </div>

    <div class="content-container pb-8">
      <p v-if="total" class="text-ink-light text-[13px] mb-3">共收录 {{ total }} 首</p>

      <van-list
        v-model:loading="loading"
        v-model:error="error"
        :finished="finished"
        finished-text="已加载全部诗词"
        error-text="加载失败，点击重试"
        :offset="300"
        @load="onLoad"
      >
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          <PoemCard
            v-for="poem in poems"
            :key="poem.id"
            :poem="poem"
            @click="goDetail"
          />
        </div>
      </van-list>

      <EmptyState v-if="finished && !poems.length" message="暂无诗词" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { getAllPoems } from '@/api/poem'
import { usePoemStore } from '@/stores/poem'
import PoemCard from '@/components/poetry/PoemCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()
const poemStore = usePoemStore()

const poems = ref([])
const total = ref(0)
const page = ref(0)
const pageSize = 18
const loading = ref(false)
const finished = ref(false)
const error = ref(false)

function goDetail(poem) {
  poemStore.setCurrentPoem(poem)
  router.push(`/poem/${poem.id}`)
}

async function onLoad() {
  try {
    page.value++
    const data = await getAllPoems(page.value, pageSize)
    const items = Array.isArray(data) ? data : (data?.items || [])
    const serverTotal = Array.isArray(data) ? data.length : (data?.total || 0)

    poems.value.push(...items)
    total.value = serverTotal
    loading.value = false

    if (!items.length || poems.value.length >= serverTotal) {
      finished.value = true
    }
  } catch {
    loading.value = false
    error.value = true
  }
}
</script>
