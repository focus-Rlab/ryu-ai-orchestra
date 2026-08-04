import { beforeEach, describe, expect, it } from 'vitest'
import { DEFAULT_STATE } from './progression'
import { loadState, saveState } from './storage'

const data = new Map<string, string>()

beforeEach(() => {
  data.clear()
  Object.defineProperty(globalThis, 'localStorage', {
    configurable: true,
    value: {
      getItem: (key: string) => data.get(key) ?? null,
      setItem: (key: string, value: string) => data.set(key, value),
    },
  })
})

describe('storage', () => {
  it('restores saved habits and entries after a fresh load', () => {
    const saved = {
      ...DEFAULT_STATE,
      entries: [{ habitId: 'study', date: '2026-08-04', completed: true, minutes: 45 }],
    }
    saveState(saved)
    expect(loadState()).toEqual(saved)
  })

  it('falls back safely when stored data is broken', () => {
    data.set('effort-avatar-state-v1', '{broken')
    expect(loadState()).toEqual(DEFAULT_STATE)
  })
})
