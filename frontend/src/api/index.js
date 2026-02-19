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

export async function fetchGuild() {
  const response = await apiClient.get('/guild')
  return response.data
}

export async function fetchCategories() {
  const response = await apiClient.get('/categories')
  return response.data
}

export async function fetchChannels() {
  const response = await apiClient.get('/channels')
  return response.data
}
