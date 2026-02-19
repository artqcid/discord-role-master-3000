<script setup>
import { useServerStore } from '@/stores/serverStore'
import { computed, ref } from 'vue'
import { PERMISSIONS, PERMISSION_NAMES, hasPermission, addPermission, removePermission } from '@/utils/permissions'

const store = useServerStore()
const channels = computed(() => store.channels)
const roles = computed(() => store.roles)

const expandedChannels = ref(new Set())

function toggleExpand(channelId) {
  if (expandedChannels.value.has(channelId)) {
    expandedChannels.value.delete(channelId)
  } else {
    expandedChannels.value.add(channelId)
  }
}

function getRoleName(roleId) {
  const role = roles.value.find(r => r.id === roleId)
  return role ? role.name : roleId
}

function getRoleColor(roleId) {
    const role = roles.value.find(r => r.id === roleId)
    if (!role || !role.color) return '#99aab5'
    return '#' + role.color.toString(16).padStart(6, '0')
}

// Important permissions to show in simple UI
const DISPLAY_PERMISSIONS = [
  PERMISSIONS.VIEW_CHANNEL,
  PERMISSIONS.SEND_MESSAGES,
  PERMISSIONS.READ_MESSAGE_HISTORY,
  PERMISSIONS.CONNECT,
  PERMISSIONS.SPEAK,
  PERMISSIONS.MANAGE_CHANNELS
]

async function togglePerm(channel, overwrite, permBit, type) {
    // type: 'allow' or 'deny'
    // If we toggle allow:
    //   if allowed -> remove allow
    //   if not allowed -> add allow, remove deny
    
    let newAllow = overwrite.allow
    let newDeny = overwrite.deny
    
    if (type === 'allow') {
        if (hasPermission(newAllow, permBit)) {
            newAllow = removePermission(newAllow, permBit)
        } else {
            newAllow = addPermission(newAllow, permBit)
            newDeny = removePermission(newDeny, permBit)
        }
    } else { // deny
        if (hasPermission(newDeny, permBit)) {
            newDeny = removePermission(newDeny, permBit)
        } else {
            newDeny = addPermission(newDeny, permBit)
            newAllow = removePermission(newAllow, permBit)
        }
    }
    
    await store.updateOverwrite(channel.id, overwrite.target_id, {
        target_type: overwrite.target_type,
        allow: newAllow,
        deny: newDeny
    })
}

async function startOverwriteAdd(channel) {
    // Simple prompt for now
    const targetId = prompt("Enter Role ID to add overwrite for:")
    if (!targetId) return
    
    // Check if exists
    if (channel.overwrites.find(o => o.target_id === targetId)) {
        alert("Overwrite already exists!")
        return
    }
    
    await store.updateOverwrite(channel.id, targetId, {
        target_type: 'role', // Assumption for prototype
        allow: '0',
        deny: '0'
    })
    
    toggleExpand(channel.id) // Ensure expanded
}

async function deleteOverwrite(channel, overwrite) {
    if(!confirm("Overwrite wirklich löschen?")) return
    await store.deleteOverwrite(channel.id, overwrite.target_id)
}
</script>

<template>
  <div class="channels-view">
    <h2>Kanäle & Berechtigungen</h2>
    
    <div v-if="store.isLoading" class="loading">Lade Kanäle...</div>
    <div v-else class="channels-list">
      <div v-for="channel in channels" :key="channel.id" class="channel-wrapper">
        <div class="channel-header" @click="toggleExpand(channel.id)">
            <span class="channel-icon">{{ channel.type === 'voice' ? '🔊' : '#' }}</span>
            <span class="channel-name">{{ channel.name }}</span>
            <span class="channel-meta" v-if="channel.category_id">
                (Kategorie: {{ channel.category_id }})
            </span>
            <span class="channel-expand-icon">{{ expandedChannels.has(channel.id) ? '▼' : '▶' }}</span>
        </div>
        
        <div v-if="expandedChannels.has(channel.id)" class="overwrites-panel">
            <div class="overwrites-header">
                <h3>Overwrites</h3>
                <button @click.stop="startOverwriteAdd(channel)" class="btn-add">+ Overwrite hinzufügen</button>
            </div>
            
            <table class="overwrites-table">
                <thead>
                    <tr>
                        <th>Target</th>
                        <th v-for="perm in DISPLAY_PERMISSIONS" :key="perm">
                            {{ PERMISSION_NAMES[perm] }}
                        </th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="ow in channel.overwrites" :key="ow.id">
                        <td>
                            <span :style="{ color: getRoleColor(ow.target_id) }">
                                {{ getRoleName(ow.target_id) }}
                            </span>
                             <small v-if="ow.target_type === 'member'">(User)</small>
                        </td>
                        <td v-for="perm in DISPLAY_PERMISSIONS" :key="perm" class="perm-cell">
                           <!-- Tri-State Logic: 
                                Green Check = Allow matches
                                Red Cross = Deny matches
                                Gray Slash = Inherit (neither)
                           -->
                           <div class="perm-controls">
                               <span 
                                    class="perm-icon allow" 
                                    :class="{ active: hasPermission(ow.allow, perm) }"
                                    @click="togglePerm(channel, ow, perm, 'allow')"
                               >✔</span>
                               <span 
                                    class="perm-icon deny" 
                                    :class="{ active: hasPermission(ow.deny, perm) }"
                                    @click="togglePerm(channel, ow, perm, 'deny')"
                               >✖</span>
                           </div>
                        </td>
                        <td>
                            <button @click="deleteOverwrite(channel, ow)" class="btn-delete">🗑</button>
                        </td>
                    </tr>
                    <tr v-if="!channel.overwrites?.length">
                        <td colspan="100" class="no-data">Keine Overwrites</td>
                    </tr>
                </tbody>
            </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.channels-view {
  padding: 20px;
  color: var(--text-normal);
}

.channel-wrapper {
    margin-bottom: 8px;
    background-color: var(--background-secondary);
    border-radius: 4px;
    overflow: hidden;
}

.channel-header {
    padding: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: bold;
}
.channel-header:hover {
    background-color: var(--background-modifier-hover);
}

.channel-expand-icon {
    margin-left: auto;
}

.overwrites-panel {
    padding: 12px;
    background-color: var(--background-secondary-alt);
    border-top: 1px solid var(--background-modifier-accent);
    overflow-x: auto;
}

.overwrites-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.overwrites-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9em;
}

.overwrites-table th, .overwrites-table td {
    border: 1px solid var(--background-modifier-accent);
    padding: 8px;
    text-align: center;
}

.overwrites-table th {
    background-color: var(--background-tertiary);
}

.perm-controls {
    display: flex;
    gap: 4px;
    justify-content: center;
}

.perm-icon {
    cursor: pointer;
    opacity: 0.3;
    font-weight: bold;
}

.perm-icon.active {
    opacity: 1;
}

.perm-icon.allow.active { color: var(--green); }
.perm-icon.deny.active { color: var(--red); }

.btn-add {
    background-color: var(--green);
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
}

.btn-delete {
    background-color: transparent;
    border: none;
    color: var(--red);
    cursor: pointer;
}
</style>
