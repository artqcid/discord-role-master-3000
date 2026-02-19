<script setup>
import { useServerStore } from '@/stores/serverStore'
import { computed, ref } from 'vue'

const store = useServerStore()
const roles = computed(() => store.roles)

// Local edit state to avoid direct mutation of store state before save
const editingRoleId = ref(null)
const editForm = ref({ name: '', color: 0 })

function startEdit(role) {
  editingRoleId.value = role.id
  editForm.value = { 
    name: role.name, 
    color: intToHex(role.color) 
  }
}

function cancelEdit() {
  editingRoleId.value = null
}

async function saveEdit(roleId) {
  const hex = editForm.value.color
  const intColor = parseInt(hex.replace('#', ''), 16)
  
  try {
    await store.updateRole(roleId, {
      name: editForm.value.name,
      color: intColor
    })
    editingRoleId.value = null
  } catch (e) {
    alert("Fehler beim Speichern: " + e)
  }
}

function intToHex(intColor) {
  if (!intColor && intColor !== 0) return '#99aab5' 
  return '#' + intColor.toString(16).padStart(6, '0')
}
</script>

<template>
  <div class="roles-view">
    <h2>Rollenverwaltung ({{ roles.length }})</h2>
    
    <div v-if="store.isLoading" class="loading">Lade Rollen...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>
    
    <div v-else class="roles-list">
      <div v-for="role in roles" :key="role.id" class="role-item" :class="{ 'is-editing': editingRoleId === role.id }">
        
        <!-- View Mode -->
        <template v-if="editingRoleId !== role.id">
          <div class="role-color" :style="{ backgroundColor: intToHex(role.color) }"></div>
          <div class="role-info">
            <span class="role-name" :style="{ color: intToHex(role.color) }">{{ role.name }}</span>
            <span class="role-meta">ID: {{ role.id }} | Pos: {{ role.position }}</span>
          </div>
          <div class="role-actions">
            <span v-if="role.managed" class="badge">Managed</span>
            <button v-else @click="startEdit(role)" class="btn-edit">Bearbeiten</button>
          </div>
        </template>

        <!-- Edit Mode -->
        <template v-else>
          <div class="edit-mode">
            <input type="color" v-model="editForm.color" class="input-color">
            <input type="text" v-model="editForm.name" class="input-name">
            <button @click="saveEdit(role.id)" class="btn-save">Speichern</button>
            <button @click="cancelEdit" class="btn-cancel">Abbrechen</button>
          </div>
        </template>

      </div>
    </div>
  </div>
</template>

<style scoped>
.roles-view {
  padding: 20px;
  color: var(--text-normal);
}

.roles-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 16px;
}

.role-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background-color: var(--background-secondary);
  padding: 10px;
  border-radius: 4px;
}

.role-color {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.role-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.role-name {
  font-weight: bold;
}

.role-meta {
  font-size: 0.8em;
  color: var(--text-muted);
}

.role-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.edit-mode {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.input-color {
  width: 40px;
  height: 30px;
  padding: 0;
  border: none;
  background: none;
}

.input-name {
  flex: 1;
  padding: 4px 8px;
  background: var(--background-tertiary);
  border: 1px solid var(--background-modifier-accent);
  color: white;
  border-radius: 4px;
}

.btn-edit, .btn-save, .btn-cancel {
  padding: 4px 12px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.9em;
}

.btn-edit {
  background-color: var(--background-secondary-alt);
  color: var(--text-normal);
}

.btn-save {
  background-color: var(--green);
  color: white;
}

.btn-cancel {
  background-color: var(--red);
  color: white;
}

.badge {
  background-color: var(--primary);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7em;
  text-transform: uppercase;
}
</style>
