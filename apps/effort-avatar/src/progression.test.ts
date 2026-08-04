import { describe, expect, it } from 'vitest'
import { COMPOSITE_AURA_LEVEL, DAILY_MINUTE_CAP, DECAY_XP_PER_MISSED_DAY, DEFAULT_STATE, calculateProgress, compositeAbilities, experienceForEntry, milestoneForLevel, upsertEntry, visualTierForLevel } from './progression'
import type { AppState, HabitEntry } from './types'

const entry = (habitId: string, date: string, completed: boolean, minutes = 0): HabitEntry => ({ habitId, date, completed, minutes })

describe('progression', () => {
  it('rewards both completion and time while capping time-based XP', () => {
    const normal = experienceForEntry(entry('study', '2026-08-01', true, 60))
    const capped = experienceForEntry(entry('study', '2026-08-01', true, 500))
    expect(normal).toBeGreaterThan(20)
    expect(capped).toBe(experienceForEntry(entry('study', '2026-08-01', true, DAILY_MINUTE_CAP)))
  })

  it('does not decay after one miss and decays gently after the second consecutive miss', () => {
    const baseEntries = [entry('workout', '2026-08-01', true, 120)]
    const once: AppState = { ...DEFAULT_STATE, entries: [...baseEntries, entry('workout', '2026-08-02', false)] }
    const twice: AppState = { ...DEFAULT_STATE, entries: [...once.entries, entry('workout', '2026-08-03', false)] }
    expect(calculateProgress(once).vitality.xp).toBe(80)
    expect(calculateProgress(twice).vitality.xp).toBe(80 - DECAY_XP_PER_MISSED_DAY)
    expect(calculateProgress(twice).vitality.auraStrength).toBeLessThan(calculateProgress(once).vitality.auraStrength)
  })

  it('resets consecutive misses when effort resumes', () => {
    const state: AppState = { ...DEFAULT_STATE, entries: [
      entry('reading', '2026-08-01', false),
      entry('reading', '2026-08-02', false),
      entry('reading', '2026-08-03', true, 30),
    ] }
    expect(calculateProgress(state).knowledge.recentMisses).toBe(0)
  })

  it('does not treat separated missed dates as consecutive days', () => {
    const state: AppState = { ...DEFAULT_STATE, entries: [
      entry('workout', '2026-08-01', true, 120),
      entry('workout', '2026-08-02', false),
      entry('workout', '2026-08-05', false),
    ] }
    expect(calculateProgress(state).vitality.xp).toBe(80)
    expect(calculateProgress(state).vitality.recentMisses).toBe(1)
  })

  it('keeps every aura dormant before the first effort', () => {
    const progress = calculateProgress(DEFAULT_STATE)
    expect(Object.values(progress).every((item) => item.auraStrength === 0)).toBe(true)
    expect(compositeAbilities(progress)).toEqual([])
  })

  it('tracks decay independently when multiple habits grow the same ability', () => {
    const state: AppState = {
      ...DEFAULT_STATE,
      habits: [...DEFAULT_STATE.habits, { id: 'run', name: 'ランニング', ability: 'vitality', targetMinutes: 20, builtIn: false }],
      entries: [
        entry('workout', '2026-08-01', true, 30),
        entry('workout', '2026-08-02', true, 30),
        entry('run', '2026-08-01', false),
        entry('run', '2026-08-02', false),
      ],
    }
    expect(calculateProgress(state).vitality.xp).toBe(65)
    expect(calculateProgress(state).vitality.recentMisses).toBe(2)
  })

  it('unlocks a composite aura when two abilities reach the threshold', () => {
    const entries: HabitEntry[] = []
    for (let day = 1; day <= COMPOSITE_AURA_LEVEL * 2 + 1; day += 1) {
      const date = `2026-07-${String(day).padStart(2, '0')}`
      entries.push(entry('workout', date, true, 120), entry('study', date, true, 120))
    }
    const abilities = compositeAbilities(calculateProgress({ ...DEFAULT_STATE, entries }))
    expect(abilities).toContain('vitality')
    expect(abilities).toContain('intellect')
  })

  it('uses the confirmed milestone tiers', () => {
    expect(milestoneForLevel(9)).toBe(0)
    expect(milestoneForLevel(10)).toBe(10)
    expect(milestoneForLevel(25)).toBe(25)
    expect(milestoneForLevel(50)).toBe(50)
    expect(milestoneForLevel(100)).toBe(100)
  })

  it('changes the visual tier every ten levels', () => {
    expect(visualTierForLevel(9)).toBe(0)
    expect(visualTierForLevel(10)).toBe(1)
    expect(visualTierForLevel(19)).toBe(1)
    expect(visualTierForLevel(20)).toBe(2)
  })

  it('replaces the same habit and date instead of duplicating it', () => {
    const original = [entry('study', '2026-08-03', false)]
    const updated = upsertEntry(original, entry('study', '2026-08-03', true, 45))
    expect(updated).toHaveLength(1)
    expect(updated[0]).toMatchObject({ completed: true, minutes: 45 })
  })
})
