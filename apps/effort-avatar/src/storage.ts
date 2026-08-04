import { DEFAULT_STATE } from './progression'
import type { AppState } from './types'

const STORAGE_KEY = 'effort-avatar-state-v1'

export function loadState(): AppState {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return DEFAULT_STATE
    const parsed = JSON.parse(stored) as Partial<AppState>
    if (!Array.isArray(parsed.habits) || !Array.isArray(parsed.entries)) return DEFAULT_STATE
    return { ...DEFAULT_STATE, ...parsed }
  } catch {
    return DEFAULT_STATE
  }
}

export function saveState(state: AppState): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
}
