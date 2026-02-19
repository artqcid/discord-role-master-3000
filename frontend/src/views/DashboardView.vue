<template>
  <div class="dashboard">
    <header class="dashboard__header">
      <div v-if="store.isLoading" class="loading-pulse">Lade Serverdaten…</div>
      <div v-else-if="store.error" class="error-msg">{{ store.error }}</div>
      <template v-else-if="store.guildInfo">
        <img
          v-if="store.guildInfo.icon_url"
          :src="store.guildInfo.icon_url"
          :alt="store.guildInfo.name"
          class="guild-icon"
        />
        <h1 class="guild-name">{{ store.guildInfo.name }}</h1>
      </template>
    </header>

    <div class="dashboard__body">
      <aside class="channel-list">
        <div
          v-for="cat in store.categories"
          :key="cat.id"
          class="category-block"
        >
          <div class="category-name">{{ cat.name }}</div>
          <div
            v-for="ch in channelsByCategory(cat.id)"
            :key="ch.id"
            class="channel-item"
            :class="{ active: selectedChannel?.id === ch.id }"
            @click="selectChannel(ch)"
          >
            <span class="channel-icon">{{ channelIcon(ch.type) }}</span>
            <span class="channel-label">{{ ch.name }}</span>
          </div>
        </div>

        <div v-if="uncategorized.length" class="category-block">
          <div class="category-name">— Ohne Kategorie —</div>
          <div 
            v-for="ch in uncategorized" 
            :key="ch.id" 
            class="channel-item"
            :class="{ active: selectedChannel?.id === ch.id }"
            @click="selectChannel(ch)"
          >
            <span class="channel-icon">{{ channelIcon(ch.type) }}</span>
            <span class="channel-label">{{ ch.name }}</span>
          </div>
        </div>
      </aside>

      <main class="main-content">
        <div v-if="selectedChannel" class="channel-details">
            <h2>{{ channelIcon(selectedChannel.type) }} {{ selectedChannel.name }}</h2>
            <div class="detail-grid">
                <div class="detail-item">
                    <label>ID</label>
                    <span>{{ selectedChannel.id }}</span>
                </div>
                <div class="detail-item">
                    <label>Typ</label>
                    <span>{{ selectedChannel.type }}</span>
                </div>
                <div class="detail-item">
                    <label>Position</label>
                    <span>{{ selectedChannel.position }}</span>
                </div>
                <div class="detail-item">
                    <label>Kategorie</label>
                    <span>{{ selectedChannel.category_id || 'Keine' }}</span>
                </div>
            </div>
            
            <div class="nsfw-badge" v-if="selectedChannel.nsfw">🔞 NSFW</div>
            
            <div class="actions">
                <router-link to="/channels" class="btn-manage">Berechtigungen verwalten</router-link>
            </div>
        </div>
        <p v-else class="welcome-text">
          Wähle einen Kanal aus, um Details zu sehen.
        </p>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useServerStore } from '@/stores/serverStore.js'

const store = useServerStore()
const selectedChannel = ref(null)

onMounted(() => store.loadAll())

function selectChannel(channel) {
    selectedChannel.value = channel
}

const CHANNEL_ICONS = {
  text: '#',
  voice: '🔊',
  forum: '🗂️',
  stage: '🎤',
  announcement: '📢',
  unknown: '?',
}


function channelIcon(type) {
  return CHANNEL_ICONS[type] ?? CHANNEL_ICONS.unknown
}

function channelsByCategory(categoryId) {
  return store.channels.filter((ch) => ch.category_id === categoryId)
}

const uncategorized = computed(() =>
  store.channels.filter((ch) => ch.category_id === null),
)
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.dashboard__header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: var(--color-bg-dark);
  border-bottom: 1px solid var(--color-border);
}

.guild-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.guild-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
}

.dashboard__body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.channel-list {
  width: 240px;
  overflow-y: auto;
  background: var(--color-bg-sidebar);
  padding: 0.75rem 0;
  flex-shrink: 0;
}

.category-block {
  margin-bottom: 0.5rem;
}

.category-name {
  padding: 0.4rem 1rem;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}

.channel-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  color: var(--color-text-secondary);
  transition: background 0.15s, color 0.15s;
}

.channel-item:hover, .channel-item.active {
  background: var(--color-hover);
  color: var(--color-text-primary);
}

.channel-icon {
  font-size: 0.9rem;
  opacity: 0.7;
}

.channel-label {
  font-size: 0.9rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.welcome-text {
  color: var(--color-text-muted);
  font-size: 1rem;
}

.loading-pulse {
  color: var(--color-accent);
  animation: pulse 1.5s infinite;
}

.error-msg {
  color: #ed4245;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.detail-item {
    background: var(--color-bg-sidebar);
    padding: 0.5rem;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
}

.detail-item label {
    font-size: 0.7em;
    color: var(--color-text-muted);
    font-weight: bold;
    text-transform: uppercase;
}

.nsfw-badge {
    display: inline-block;
    background: #ed4245;
    color: white;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.8em;
    margin-top: 1rem;
}

.actions {
    margin-top: 2rem;
}

.btn-manage {
    display: inline-block;
    background: var(--color-accent);
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 4px;
    transition: background 0.2s;
}

.btn-manage:hover {
    background: var(--color-accent-hover);
}
</style>
