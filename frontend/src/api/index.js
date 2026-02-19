/**
 * Axios instance and API call functions.
 * All HTTP communication goes through this module.
 * Components and stores must never import axios directly.
 */
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' },
})

export default {
  getGuild() {
    return apiClient.get('/guild')
  },
  getRoles() {
    return apiClient.get('/roles')
  },
  getCategories() {
    return apiClient.get('/categories')
  },
  getChannels() {
    return apiClient.get('/channels')
  },
  updateRole(roleId, data) {
    return apiClient.patch(`/roles/${roleId}`, data)
  },
  upsertOverwrite(channelId, targetId, data) {
    return apiClient.put(`/channels/${channelId}/overwrites/${targetId}`, data)
  },
  deleteOverwrite(channelId, targetId) {
    return apiClient.delete(`/channels/${channelId}/overwrites/${targetId}`)
  },
  getConflicts() {
    return apiClient.get('/conflicts')
  }
}
