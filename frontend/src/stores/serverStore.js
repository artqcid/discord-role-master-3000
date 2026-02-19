/**
 * Pinia store for Discord server state.
 * State: guildInfo, categories, channels.
 * Actions call src/api/ – never fetch() directly.
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchGuild, fetchCategories, fetchChannels } from '@/api/index.js'

export const useServerStore = defineStore('server', () => {
  const guildInfo = ref(null)
  const categories = ref([])
  const channels = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  async function loadGuild() {
    try {
      guildInfo.value = await fetchGuild()
    } catch (err) {
      error.value = 'Serverdaten konnten nicht geladen werden.'
    }
  }

  async function loadCategories() {
    try {
      categories.value = await fetchCategories()
    } catch (err) {
      error.value = 'Kategorien konnten nicht geladen werden.'
    }
  }

  async function loadChannels() {
    try {
      channels.value = await fetchChannels()
    } catch (err) {
      error.value = 'Kanäle konnten nicht geladen werden.'
    }
  }

  async function loadAll() {
    isLoading.value = true
    error.value = null
    await Promise.all([loadGuild(), loadCategories(), loadChannels()])
    isLoading.value = false
  }

  return { guildInfo, categories, channels, isLoading, error, loadAll }
})
