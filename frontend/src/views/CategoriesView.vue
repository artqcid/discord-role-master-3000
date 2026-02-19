<script setup>
import { useServerStore } from '@/stores/serverStore'
import { computed, ref, onMounted, nextTick } from 'vue'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import '@vue-flow/controls/dist/style.css'
import '@vue-flow/minimap/dist/style.css'

const store = useServerStore()
const { onInit, fitView } = useVueFlow()

const nodes = ref([])
const edges = ref([])
const containerRef = ref(null)

onMounted(async () => {
    if (!store.channels.length) await store.loadAll()
    buildGraph()
    
    await nextTick()
    setTimeout(() => {
        window.dispatchEvent(new Event('resize'))
        fitView()
    }, 300)
})

function buildGraph() {
    const newNodes = []
    const newEdges = []
    const X_CAT = 0
    const X_CHAN = 350
    
    // Guild Node
    if (store.guildInfo) {
        newNodes.push({ 
            id: 'guild', 
            label: store.guildInfo.name, 
            position: { x: 175, y: -150 },
            style: { background: '#5865F2', color: 'white', border: 'none', borderRadius: '8px', padding: '10px' }
        })
    }
    
    // Sort channels by position
    const sortedChannels = [...store.channels].sort((a, b) => a.position - b.position)
    
    // Group by Category
    const categories = store.categories
    const channelsByCategory = {}
    
    sortedChannels.forEach(c => {
        const catId = c.category_id || 'uncategorized'
        if (!channelsByCategory[catId]) channelsByCategory[catId] = []
        channelsByCategory[catId].push(c)
    })
    
    // Uncategorized first? Or follow category position?
    // Let's iterate categories sorted by position
    const sortedCats = [...categories].sort((a, b) => a.position - b.position)
    
    // Add Uncategorized bucket if needed
    if (channelsByCategory['uncategorized']?.length) {
        sortedCats.unshift({ id: 'uncategorized', name: 'Uncategorized', position: -1 })
    }
    
    let yOffset = 0
    
    sortedCats.forEach(cat => {
        const catId = cat.id
        const catChannels = channelsByCategory[catId] || []
        
        if (catChannels.length === 0 && catId !== 'uncategorized') {
             // Show empty categories too
             newNodes.push({
                id: catId,
                label: cat.name,
                position: { x: X_CAT, y: yOffset },
                style: { background: '#2f3136', color: '#b9bbbe', width: '200px' }
            })
             newEdges.push({ id: `e-guild-${catId}`, source: 'guild', target: catId, animated: true })
             yOffset += 100
             return
        }
        
        if (catChannels.length > 0) {
            // Category Node
             newNodes.push({
                id: catId,
                label: cat.name || 'Uncategorized',
                position: { x: X_CAT, y: yOffset + (catChannels.length * 60) / 2 - 30 },
                style: { background: '#2f3136', color: '#b9bbbe', width: '250px', fontWeight: 'bold' }
            })
            newEdges.push({ id: `e-guild-${catId}`, source: 'guild', target: catId })
            
            // Channel Nodes
            catChannels.forEach((chan, idx) => {
                newNodes.push({
                    id: chan.id,
                    label: (chan.type === 'voice' ? '🔊 ' : '# ') + chan.name,
                    position: { x: X_CHAN, y: yOffset + (idx * 60) },
                    style: { background: '#36393f', color: 'white', width: '250px' }
                })
                newEdges.push({ id: `e-${catId}-${chan.id}`, source: catId, target: chan.id })
            })
             yOffset += (catChannels.length * 60) + 80
        }
    })
    
    nodes.value = newNodes
    edges.value = newEdges
}

</script>

<template>
  <div class="categories-view" ref="containerRef">
    <div class="flow-wrapper">
      <VueFlow
        v-model:nodes="nodes"
        v-model:edges="edges"
        :default-viewport="{ zoom: 0.8 }"
        fit-view-on-init
        class="categories-flow"
      >
        <Background pattern-color="#333" :gap="16" />
        <Controls />
        <MiniMap />
      </VueFlow>
    </div>
  </div>
</template>

<style scoped>
.categories-view {
  flex: 1;
  width: 100%;
  /* Use viewport height to be absolutely sure */
  height: calc(100vh - 2rem); 
  padding: 1rem;
  display: flex;
  flex-direction: column;
}

.flow-wrapper {
  flex: 1;
  width: 100%;
  height: 100%;
  position: relative; /* Base for absolute child */
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: #1e1f22;
}

.categories-flow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* Ensure the internal container takes all space */
:deep(.vue-flow__container) {
  width: 100% !important;
  height: 100% !important;
}

:deep(.vue-flow__node) {
    border-radius: 4px;
    border: 1px solid #202225;
}

:deep(.vue-flow__edge-path) {
  stroke: #4f545c;
  stroke-width: 2;
}
</style>
