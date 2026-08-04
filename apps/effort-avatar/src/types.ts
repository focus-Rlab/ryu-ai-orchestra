export type Ability = 'vitality' | 'intellect' | 'knowledge'
export type AvatarType = 'masculine' | 'feminine'

export interface Habit {
  id: string
  name: string
  ability: Ability
  targetMinutes: number
  builtIn: boolean
}

export interface HabitEntry {
  habitId: string
  date: string
  completed: boolean
  minutes: number
}

export interface AppState {
  avatarType: AvatarType
  habits: Habit[]
  entries: HabitEntry[]
}

export interface AbilityProgress {
  ability: Ability
  xp: number
  level: number
  levelProgress: number
  recentMisses: number
  auraStrength: number
}
