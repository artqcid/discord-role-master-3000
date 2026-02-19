/**
 * Pinia store for Discord server state.
 * State: guildInfo, categories, channels.
 * Actions call src/api/ – never fetch() directly.
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/index.js'

export const useServerStore = defineStore('server', () => {
  const guildInfo = ref(null)
  const categories = ref([])
  const channels = ref([])
  const roles = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  async function loadGuild() {
    try {
      const response = await api.getGuild()
      guildInfo.value = response.data
    } catch (err) {
      error.value = 'Serverdaten konnten nicht geladen werden.'
      console.error(err)
    }
  }

  async function loadRoles() {
    try {
      const response = await api.getRoles()
      roles.value = response.data
      console.log("loadRoles: Success, count:", roles.value.length)
    } catch (err) {
      console.error("loadRoles Error:", err)
      const detail = err.response?.data?.detail || err.message
      error.value = `Rollen-Fehler: ${detail}`
    }
  }

  async function loadCategories() {
    try {
      const response = await api.getCategories()
      categories.value = response.data
    } catch (err) {
      error.value = 'Kategorien-Fehler: ' + (err.response?.data?.detail || err.message)
      console.error(err)
    }
  }

  async function loadChannels() {
    try {
      const response = await api.getChannels()
      channels.value = response.data
    } catch (err) {
      error.value = 'Kanäle-Fehler: ' + (err.response?.data?.detail || err.message)
      console.error(err)
    }
  }

  async function loadAll() {
    isLoading.value = true
    error.value = null
    // Load Guild first to get ID for roles
    await loadGuild()
    await Promise.all([loadRoles(), loadCategories(), loadChannels()])
    isLoading.value = false
  }

  async function updateRole(roleId, data) {
    // Guild info not strictly needed for the API call anymore, but good check
    try {
      const response = await api.updateRole(roleId, data)
      // Update local state
      const index = roles.value.findIndex(r => r.id === roleId)
      if (index !== -1) {
        roles.value[index] = response.data
      }
    } catch (err) {
      console.error(err)
      throw err
    }
  }

  async function updateOverwrite(channelId, targetId, data) {
    try {
      await api.upsertOverwrite(channelId, targetId, data)
      await loadChannels() // Reload to get fresh overwrites
    } catch (err) {
      console.error(err)
      throw err
    }
  }

  async function deleteOverwrite(channelId, targetId) {
    try {
      await api.deleteOverwrite(channelId, targetId)
      await loadChannels()
    } catch (err) {
      console.error(err)
      throw err
    }
  }

  return { 
    guildInfo, categories, channels, roles, isLoading, error, 
    loadAll, updateRole, updateOverwrite, deleteOverwrite 
  }
})
