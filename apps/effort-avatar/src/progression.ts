import type { Ability, AbilityProgress, AppState, Habit, HabitEntry } from './types'

export const XP_PER_LEVEL = 100
export const COMPLETION_XP = 20
export const XP_PER_MINUTE = 0.5
export const DAILY_MINUTE_CAP = 120
export const DECAY_XP_PER_MISSED_DAY = 5
export const COMPOSITE_AURA_LEVEL = 5

export const ABILITIES: Ability[] = ['vitality', 'intellect', 'knowledge']

export const DEFAULT_HABITS: Habit[] = [
  { id: 'workout', name: '筋トレ', ability: 'vitality', targetMinutes: 30, builtIn: true },
  { id: 'study', name: '勉強', ability: 'intellect', targetMinutes: 45, builtIn: true },
  { id: 'reading', name: '読書', ability: 'knowledge', targetMinutes: 20, builtIn: true },
]

export const DEFAULT_STATE: AppState = {
  avatarType: 'masculine',
  habits: DEFAULT_HABITS,
  entries: [],
}

const dayNumber = (date: string) => Math.floor(new Date(`${date}T00:00:00Z`).getTime() / 86_400_000)

export function experienceForEntry(entry: HabitEntry): number {
  if (!entry.completed) return 0
  const minutes = Math.min(Math.max(entry.minutes, 0), DAILY_MINUTE_CAP)
  return COMPLETION_XP + minutes * XP_PER_MINUTE
}

function decayForSingleHabit(entries: HabitEntry[]): { decay: number; recentMisses: number } {
  const byDate = new Map(entries.map((entry) => [entry.date, entry]))
  const dates = [...byDate.keys()].sort((a, b) => dayNumber(a) - dayNumber(b))
  let consecutiveMisses = 0
  let decay = 0

  let previousDay: number | null = null
  for (const date of dates) {
    const entry = byDate.get(date)!
    const currentDay = dayNumber(date)
    if (previousDay !== null && currentDay !== previousDay + 1) consecutiveMisses = 0
    if (entry.completed) {
      consecutiveMisses = 0
      previousDay = currentDay
      continue
    }
    consecutiveMisses += 1
    if (consecutiveMisses >= 2) decay += DECAY_XP_PER_MISSED_DAY
    previousDay = currentDay
  }

  return { decay, recentMisses: consecutiveMisses }
}

export function calculateProgress(state: AppState): Record<Ability, AbilityProgress> {
  return Object.fromEntries(
    ABILITIES.map((ability) => {
      const habitIds = new Set(state.habits.filter((habit) => habit.ability === ability).map((habit) => habit.id))
      const entries = state.entries.filter((entry) => habitIds.has(entry.habitId))
      const earned = entries.reduce((sum, entry) => sum + experienceForEntry(entry), 0)
      const decayResults = [...habitIds].map((habitId) => decayForSingleHabit(entries.filter((entry) => entry.habitId === habitId)))
      const decay = decayResults.reduce((sum, result) => sum + result.decay, 0)
      const recentMisses = Math.max(0, ...decayResults.map((result) => result.recentMisses))
      const xp = Math.max(0, earned - decay)
      const level = Math.floor(xp / XP_PER_LEVEL) + 1
      const levelProgress = (xp % XP_PER_LEVEL) / XP_PER_LEVEL
      const fatigue = Math.min(recentMisses * 0.2, 0.75)
      const auraStrength = xp === 0 ? 0 : Math.max(0.2, (0.45 + Math.min(level, 100) / 140) * (1 - fatigue))
      return [ability, { ability, xp, level, levelProgress, recentMisses, auraStrength }]
    }),
  ) as Record<Ability, AbilityProgress>
}

export function compositeAbilities(progress: Record<Ability, AbilityProgress>): Ability[] {
  return ABILITIES.filter((ability) => progress[ability].xp > 0 && progress[ability].level >= COMPOSITE_AURA_LEVEL)
}

export function visualTierForLevel(level: number): number {
  return Math.max(0, Math.floor(level / 10))
}

export function milestoneForLevel(level: number): 100 | 50 | 25 | 10 | 0 {
  if (level >= 100) return 100
  if (level >= 50) return 50
  if (level >= 25) return 25
  if (level >= 10) return 10
  return 0
}

export function upsertEntry(entries: HabitEntry[], next: HabitEntry): HabitEntry[] {
  return [...entries.filter((entry) => !(entry.habitId === next.habitId && entry.date === next.date)), next]
}
