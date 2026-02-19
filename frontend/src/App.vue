<template>
  <div class="app-layout">
    <nav class="sidebar">
      <div class="sidebar__logo">
        <span class="logo-icon">🛡️</span>
        <span class="logo-text">Role Master</span>
      </div>
      <ul class="nav-list">
        <li>
          <RouterLink to="/" class="nav-link" active-class="nav-link--active">
            <span class="nav-icon">🏠</span>
            <span>Dashboard</span>
          </RouterLink>
        </li>
        <li>
          <RouterLink to="/roles" class="nav-link" active-class="nav-link--active">
            <span class="nav-icon">🎭</span>
            <span>Rollen</span>
          </RouterLink>
        </li>
        <li>
          <RouterLink to="/categories" class="nav-link" active-class="nav-link--active">
            <span class="nav-icon">📂</span>
            <span>Kategorien</span>
          </RouterLink>
        </li>
        <li>
          <RouterLink to="/channels" class="nav-link" active-class="nav-link--active">
            <span class="nav-icon">💬</span>
            <span>Kanäle</span>
          </RouterLink>
        </li>
      </ul>
    </nav>
    <div class="content-area">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style>
/* ── Design Tokens ─────────────────────────────────── */
:root {
  --color-bg-dark:    #23272a;
  --color-bg-sidebar: #2c2f33;
  --color-bg-content: #36393f;
  --color-accent:     #7289da;
  --color-accent-hover: #677bc4;
  --color-text-primary:   #ffffff;
  --color-text-secondary: #b9bbbe;
  --color-text-muted:     #72767d;
  --color-border:    #202225;
  --color-hover:     rgba(114, 137, 218, 0.1);

  font-family: 'gg sans', 'Noto Sans', 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  color: var(--color-text-primary);
  background: var(--color-bg-content);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body { background: var(--color-bg-dark); }

/* ── App Layout ────────────────────────────────────── */
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ── Sidebar ───────────────────────────────────────── */
.sidebar {
  width: 72px;
  background: var(--color-bg-dark);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem 0;
  gap: 0.5rem;
  border-right: 1px solid var(--color-border);
  flex-shrink: 0;
}

.sidebar__logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
}

.logo-icon { font-size: 1.75rem; }

.logo-text {
  font-size: 0.5rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--color-text-muted);
}

.nav-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  width: 100%;
  padding: 0 0.5rem;
}

.nav-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem;
  border-radius: 8px;
  text-decoration: none;
  color: var(--color-text-secondary);
  font-size: 0.6rem;
  font-weight: 600;
  transition: background 0.15s, color 0.15s;
}

.nav-link:hover, .nav-link--active {
  background: var(--color-accent);
  color: #fff;
}

.nav-icon { font-size: 1.25rem; }

/* ── Content area ──────────────────────────────────── */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--color-bg-content);
}
</style>
