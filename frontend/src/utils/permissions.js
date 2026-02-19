export const PERMISSIONS = {
  // General
  CREATE_INSTANT_INVITE: 1n << 0n,
  KICK_MEMBERS: 1n << 1n,
  BAN_MEMBERS: 1n << 2n,
  ADMINISTRATOR: 1n << 3n,
  MANAGE_CHANNELS: 1n << 4n,
  MANAGE_GUILD: 1n << 5n,
  
  // Text
  ADD_REACTIONS: 1n << 6n,
  VIEW_AUDIT_LOG: 1n << 7n,
  PRIORITY_SPEAKER: 1n << 8n,
  STREAM: 1n << 9n,
  VIEW_CHANNEL: 1n << 10n,
  SEND_MESSAGES: 1n << 11n,
  SEND_TTS_MESSAGES: 1n << 12n,
  MANAGE_MESSAGES: 1n << 13n,
  EMBED_LINKS: 1n << 14n,
  ATTACH_FILES: 1n << 15n,
  READ_MESSAGE_HISTORY: 1n << 16n,
  MENTION_EVERYONE: 1n << 17n,
  USE_EXTERNAL_EMOJIS: 1n << 18n,
  
  // Voice
  CONNECT: 1n << 20n,
  SPEAK: 1n << 21n,
  MUTE_MEMBERS: 1n << 22n,
  DEAFEN_MEMBERS: 1n << 23n,
  MOVE_MEMBERS: 1n << 24n,
  USE_VAD: 1n << 25n,
}

export const PERMISSION_NAMES = {
  [PERMISSIONS.ADMINISTRATOR]: 'Administrator',
  [PERMISSIONS.MANAGE_GUILD]: 'Server verwalten',
  [PERMISSIONS.MANAGE_CHANNELS]: 'Kanäle verwalten',
  [PERMISSIONS.VIEW_CHANNEL]: 'Kanal anzeigen',
  [PERMISSIONS.SEND_MESSAGES]: 'Nachrichten senden',
  [PERMISSIONS.READ_MESSAGE_HISTORY]: 'Nachrichtenverlauf',
  [PERMISSIONS.CONNECT]: 'Verbinden',
  [PERMISSIONS.SPEAK]: 'Sprechen',
}

// Helper to check if a bit is set
export function hasPermission(bitfieldStr, permissionBit) {
  const bf = BigInt(bitfieldStr || 0)
  return (bf & permissionBit) === permissionBit
}

export function addPermission(bitfieldStr, permissionBit) {
  const bf = BigInt(bitfieldStr || 0)
  return (bf | permissionBit).toString()
}

export function removePermission(bitfieldStr, permissionBit) {
  const bf = BigInt(bitfieldStr || 0)
  return (bf & ~permissionBit).toString()
}
