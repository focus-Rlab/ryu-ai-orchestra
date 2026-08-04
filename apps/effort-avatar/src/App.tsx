import { lazy, Suspense, useEffect, useMemo, useState } from 'react'
import { ABILITIES, calculateProgress, compositeAbilities, milestoneForLevel, upsertEntry } from './progression'
import { loadState, saveState } from './storage'
import type { Ability, AppState, Habit } from './types'

const AuraAvatar = lazy(() => import('./AuraAvatar').then((module) => ({ default: module.AuraAvatar })))

const LABELS: Record<Ability, { label: string; short: string; icon: string }> = {
  vitality: { label: '体力', short: 'VIT', icon: '◆' },
  intellect: { label: '知力', short: 'INT', icon: 'ϟ' },
  knowledge: { label: '知識', short: 'KNO', icon: '✦' },
}

const today = () => {
  const date = new Date()
  const offset = date.getTimezoneOffset()
  return new Date(date.getTime() - offset * 60_000).toISOString().slice(0, 10)
}

function App() {
  const [state, setState] = useState<AppState>(loadState)
  const [activeHabit, setActiveHabit] = useState<Habit | null>(null)
  const [showAdd, setShowAdd] = useState(false)
  const [minutes, setMinutes] = useState('')
  const [notice, setNotice] = useState('')
  const progress = useMemo(() => calculateProgress(state), [state])
  const composite = compositeAbilities(progress)
  const strongest = [...Object.values(progress)].sort((a, b) => b.level - a.level)[0]
  const hasEffort = Object.values(progress).some((item) => item.xp > 0)

  useEffect(() => saveState(state), [state])

  const record = (habit: Habit, completed: boolean, recordedMinutes = 0) => {
    setState((current) => ({
      ...current,
      entries: upsertEntry(current.entries, { habitId: habit.id, date: today(), completed, minutes: completed ? recordedMinutes : 0 }),
    }))
    setActiveHabit(null)
    setMinutes('')
    setNotice(completed ? `${habit.name}の努力が力に変わった` : `${habit.name}を未達として記録した`)
    window.setTimeout(() => setNotice(''), 2600)
  }

  const todayEntry = (habitId: string) => state.entries.find((entry) => entry.habitId === habitId && entry.date === today())

  return (
    <main className="app-shell">
      <section className="hero">
        <header className="topbar">
          <div>
            <p className="eyebrow">YOUR INNER FORCE</p>
            <h1>AURA</h1>
          </div>
          <button
            className="avatar-toggle"
            onClick={() => setState((current) => ({ ...current, avatarType: current.avatarType === 'masculine' ? 'feminine' : 'masculine' }))}
            aria-label="分身タイプを変更"
          >
            {state.avatarType === 'masculine' ? '男性型' : '女性型'}
          </button>
        </header>

        <Suspense fallback={<div className="avatar-loading" role="status">分身を呼び出しています…</div>}>
          <AuraAvatar avatarType={state.avatarType} progress={progress} />
        </Suspense>

        <div className="hero-status">
          <span className={`rank rank-${milestoneForLevel(strongest.level)}`}>{!hasEffort ? 'DORMANT' : milestoneForLevel(strongest.level) >= 25 ? 'RARE AURA' : 'AWAKENING'}</span>
          <h2>{!hasEffort ? 'オーラはまだ眠っている' : composite.length >= 2 ? '複合オーラ覚醒' : `${LABELS[strongest.ability].label}のオーラ`}</h2>
          <p>{!hasEffort ? '最初の努力を記録するとオーラが現れる' : composite.length >= 2 ? composite.map((ability) => LABELS[ability].label).join(' × ') : '今日の努力が、分身の力を形づくる'}</p>
        </div>
      </section>

      <section className="content">
        <div className="ability-grid" aria-label="能力レベル">
          {ABILITIES.map((ability) => {
            const item = progress[ability]
            return (
              <article className={`ability-card ${ability}`} key={ability}>
                <div className="ability-icon">{LABELS[ability].icon}</div>
                <div className="ability-copy">
                  <span>{LABELS[ability].short} / {LABELS[ability].label}</span>
                  <strong>Lv. {item.level}</strong>
                  <div className="progress-track"><i style={{ width: `${Math.round(item.levelProgress * 100)}%` }} /></div>
                </div>
              </article>
            )
          })}
        </div>

        <div className="section-title">
          <div><p className="eyebrow">DAILY QUESTS</p><h2>今日の努力</h2></div>
          <button className="add-button" onClick={() => setShowAdd(true)}>＋ 習慣</button>
        </div>

        <div className="habit-list">
          {state.habits.map((habit) => {
            const entry = todayEntry(habit.id)
            return (
              <article className={`habit-row ${entry ? (entry.completed ? 'complete' : 'missed') : ''}`} key={habit.id}>
                <div className={`habit-mark ${habit.ability}`}>{LABELS[habit.ability].icon}</div>
                <div className="habit-info">
                  <strong>{habit.name}</strong>
                  <span>{LABELS[habit.ability].label} · 目標 {habit.targetMinutes}分</span>
                </div>
                {entry ? (
                  <button className="recorded" onClick={() => setActiveHabit(habit)}>{entry.completed ? `${entry.minutes}分 ✓` : '未達'}</button>
                ) : (
                  <div className="habit-actions">
                    <button className="miss-button" onClick={() => record(habit, false)}>未達</button>
                    <button className="done-button" onClick={() => { setActiveHabit(habit); setMinutes(String(habit.targetMinutes)) }}>できた</button>
                  </div>
                )}
              </article>
            )
          })}
        </div>

        <p className="privacy-note">記録はこの端末のブラウザ内だけに保存されます。</p>
      </section>

      {notice && <div className="toast" role="status">{notice}</div>}

      {activeHabit && (
        <div className="modal-backdrop" onClick={() => setActiveHabit(null)}>
          <form className="bottom-sheet" onClick={(event) => event.stopPropagation()} onSubmit={(event) => { event.preventDefault(); record(activeHabit, true, Number(minutes)) }}>
            <div className="sheet-handle" />
            <p className="eyebrow">RECORD EFFORT</p>
            <h2>{activeHabit.name}は何分できた？</h2>
            <div className="minute-input"><input autoFocus inputMode="numeric" min="1" max="1440" required type="number" value={minutes} onChange={(event) => setMinutes(event.target.value)} /><span>分</span></div>
            <p className="input-hint">達成は自己申告。時間は成長量に反映され、1日120分まで加算されます。</p>
            <button className="primary-button" type="submit">努力を記録する</button>
            <button className="text-button" type="button" onClick={() => record(activeHabit, false)}>未達として記録</button>
          </form>
        </div>
      )}

      {showAdd && <AddHabit onClose={() => setShowAdd(false)} onAdd={(habit) => { setState((current) => ({ ...current, habits: [...current.habits, habit] })); setShowAdd(false) }} />}
    </main>
  )
}

function AddHabit({ onClose, onAdd }: { onClose: () => void; onAdd: (habit: Habit) => void }) {
  const [name, setName] = useState('')
  const [targetMinutes, setTargetMinutes] = useState('20')
  const [ability, setAbility] = useState<Ability>('vitality')
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <form className="bottom-sheet" onClick={(event) => event.stopPropagation()} onSubmit={(event) => {
        event.preventDefault()
        onAdd({ id: `custom-${Date.now()}`, name: name.trim(), targetMinutes: Number(targetMinutes), ability, builtIn: false })
      }}>
        <div className="sheet-handle" />
        <p className="eyebrow">CREATE QUEST</p>
        <h2>自由な習慣を追加</h2>
        <label className="field-label">習慣名<input required maxLength={30} placeholder="例：英会話" value={name} onChange={(event) => setName(event.target.value)} /></label>
        <label className="field-label">目標時間<input required inputMode="numeric" min="1" max="1440" type="number" value={targetMinutes} onChange={(event) => setTargetMinutes(event.target.value)} /></label>
        <fieldset className="ability-picker"><legend>育てる能力（オーラ属性）</legend>{ABILITIES.map((item) => <label className={ability === item ? `selected ${item}` : item} key={item}><input type="radio" name="ability" value={item} checked={ability === item} onChange={() => setAbility(item)} /><span>{LABELS[item].icon}</span>{LABELS[item].label}</label>)}</fieldset>
        <button className="primary-button" type="submit">習慣を追加する</button>
      </form>
    </div>
  )
}

export default App
