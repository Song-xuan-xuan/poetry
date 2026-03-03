<template>
  <div class="min-h-screen bg-sys-bg">
    <!-- 页面标题 -->
    <div class="content-container pt-4 pb-3 flex items-center gap-3">
      <button class="text-ink-light lg:hidden" @click="router.back()">
        <van-icon name="arrow-left" size="20" />
      </button>
      <h1 class="text-[17px] lg:text-[24px] font-semibold text-ink">{{ poem?.title || '鉴赏' }}</h1>
    </div>

    <Loading v-if="loading" text="正在加载…" />

    <div v-else-if="poem" class="animate-fade-in">
      <!-- 诗词正文 -->
      <div class="content-container py-4">
        <div class="reading-container">
          <div class="glass-card-accent p-6 lg:p-8">
            <PoemText :poem="poem" @author-click="goAuthor" />
          </div>
        </div>
      </div>

      <div class="reading-container">
        <div class="divider-brush mx-8" />
      </div>

      <!-- 赏析与文化拓展 -->
      <div class="content-container pb-20">
        <div class="reading-container">
          <AnalysisPanel :poem="poem" />
        </div>
      </div>
    </div>

    <EmptyState v-else message="诗词不存在" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPoemDetail } from '@/api/poem'
import { usePoemStore } from '@/stores/poem'
import PoemText from '@/components/poetry/PoemText.vue'
import AnalysisPanel from '@/components/poetry/AnalysisPanel.vue'
import Loading from '@/components/common/Loading.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const route = useRoute()
const router = useRouter()
const poemStore = usePoemStore()

const poem = ref(poemStore.currentPoem)
const loading = ref(false)

function goAuthor(name) {
  router.push(`/author/${encodeURIComponent(name)}`)
}

onMounted(async () => {
  const id = route.params.id
  loading.value = !poem.value
  try {
    const data = await getPoemDetail(id)
    poem.value = data
    poemStore.setCurrentPoem(data)
  } catch {
    // 保持缓存数据
  } finally {
    loading.value = false
  }
})
</script>
