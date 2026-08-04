import { DEFAULT_STATE } from './progression'
import type { Ability, AppState, AvatarType, Habit, HabitEntry } from './types'

const STORAGE_KEY = 'effort-avatar-state-v1'
const ABILITIES = new Set<Ability>(['vitality', 'intellect', 'knowledge'])
const AVATAR_TYPES = new Set<AvatarType>(['masculine', 'feminine'])
const DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/

function isHabit(value: unknown): value is Habit {
  if (!value || typeof value !== 'object') return false
  const habit = value as Partial<Habit>
  return typeof habit.id === 'string'
    && typeof habit.name === 'string'
    && ABILITIES.has(habit.ability as Ability)
    && typeof habit.targetMinutes === 'number'
    && Number.isFinite(habit.targetMinutes)
    && habit.targetMinutes > 0
    && typeof habit.builtIn === 'boolean'
}

function isEntry(value: unknown): value is HabitEntry {
  if (!value || typeof value !== 'object') return false
  const entry = value as Partial<HabitEntry>
  return typeof entry.habitId === 'string'
    && typeof entry.date === 'string'
    && DATE_PATTERN.test(entry.date)
    && typeof entry.completed === 'boolean'
    && typeof entry.minutes === 'number'
    && Number.isFinite(entry.minutes)
    && entry.minutes >= 0
}

function isAppState(value: unknown): value is AppState {
  if (!value || typeof value !== 'object') return false
  const state = value as Partial<AppState>
  return AVATAR_TYPES.has(state.avatarType as AvatarType)
    && Array.isArray(state.habits)
    && state.habits.every(isHabit)
    && Array.isArray(state.entries)
    && state.entries.every(isEntry)
}

export function loadState(): AppState {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return DEFAULT_STATE
    const parsed: unknown = JSON.parse(stored)
    return isAppState(parsed) ? parsed : DEFAULT_STATE
  } catch {
    return DEFAULT_STATE
  }
}

export function saveState(state: AppState): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
}
