import { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { compositeAbilities, milestoneForLevel, visualTierForLevel } from './progression'
import type { Ability, AbilityProgress, AvatarType } from './types'

interface Props {
  avatarType: AvatarType
  progress: Record<Ability, AbilityProgress>
}

const COLORS: Record<Ability, number> = {
  vitality: 0xff513d,
  intellect: 0x55a7ff,
  knowledge: 0x58e49b,
}

function bodyMaterial(color: number, emissive = 0x000000) {
  return new THREE.MeshStandardMaterial({ color, emissive, emissiveIntensity: 0.22, roughness: 0.52, metalness: 0.28 })
}

function addLimb(group: THREE.Group, radius: number, length: number, x: number, y: number, rotation: number) {
  const limb = new THREE.Mesh(new THREE.CapsuleGeometry(radius, length, 8, 14), bodyMaterial(0x121a30, 0x142a5b))
  limb.position.set(x, y, 0)
  limb.rotation.z = rotation
  group.add(limb)
}

function createAvatar(type: AvatarType) {
  const group = new THREE.Group()
  const suit = bodyMaterial(type === 'masculine' ? 0x182342 : 0x251b43, 0x173a7a)
  const skin = bodyMaterial(0xd7a47e)
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(type === 'masculine' ? 0.46 : 0.39, 1.05, 10, 18), suit)
  torso.position.y = 0.45
  torso.scale.x = type === 'masculine' ? 1.08 : 0.96
  group.add(torso)

  const head = new THREE.Mesh(new THREE.SphereGeometry(0.34, 24, 24), skin)
  head.position.y = 1.65
  group.add(head)
  const hair = new THREE.Mesh(new THREE.SphereGeometry(0.35, 20, 16, 0, Math.PI * 2, 0, Math.PI * 0.56), bodyMaterial(0x11121a))
  hair.position.y = 1.75
  group.add(hair)

  addLimb(group, 0.14, 0.75, -0.57, 0.42, -0.12)
  addLimb(group, 0.14, 0.75, 0.57, 0.42, 0.12)
  addLimb(group, 0.17, 0.82, -0.23, -0.77, 0.015)
  addLimb(group, 0.17, 0.82, 0.23, -0.77, -0.015)
  return group
}

function createParticles(abilities: Ability[], strength: number, milestone: number, visualTier: number) {
  const count = 120 + visualTier * 24 + milestone * 2
  const positions = new Float32Array(count * 3)
  const colors = new Float32Array(count * 3)
  const palette = abilities.length ? abilities : ['intellect' as Ability]
  const rareAccent = milestone >= 100 ? new THREE.Color(0xffffff) : milestone >= 50 ? new THREE.Color(0x9cf7ff) : milestone >= 25 ? new THREE.Color(0xffcf70) : null
  for (let index = 0; index < count; index += 1) {
    const angle = Math.random() * Math.PI * 2
    const radius = 0.72 + Math.random() * (0.75 + strength + visualTier * 0.035)
    const height = -1.5 + Math.random() * 3.7
    positions[index * 3] = Math.cos(angle) * radius
    positions[index * 3 + 1] = height
    positions[index * 3 + 2] = Math.sin(angle) * radius * 0.65
    const color = rareAccent && index % 5 === 0 ? rareAccent : new THREE.Color(COLORS[palette[index % palette.length]])
    colors[index * 3] = color.r
    colors[index * 3 + 1] = color.g
    colors[index * 3 + 2] = color.b
  }
  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
  const material = new THREE.PointsMaterial({
    size: (milestone >= 25 ? 0.055 : 0.036) + Math.min(visualTier, 10) * 0.0015,
    transparent: true,
    opacity: Math.min(0.95, strength),
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  })
  return new THREE.Points(geometry, material)
}

function createFlames(strength: number, visualTier: number) {
  const count = 28 + visualTier * 5
  const positions = new Float32Array(count * 3)
  const colors = new Float32Array(count * 3)
  for (let index = 0; index < count; index += 1) {
    const angle = (index / count) * Math.PI * 2
    const radius = 0.72 + (index % 4) * 0.12
    positions[index * 3] = Math.cos(angle) * radius
    positions[index * 3 + 1] = -1.45 + (index % 7) * 0.23
    positions[index * 3 + 2] = Math.sin(angle) * radius * 0.58
    const color = new THREE.Color(index % 3 === 0 ? 0xffd166 : index % 2 === 0 ? 0xff7b32 : 0xff3428)
    colors[index * 3] = color.r
    colors[index * 3 + 1] = color.g
    colors[index * 3 + 2] = color.b
  }
  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3))
  const material = new THREE.PointsMaterial({ size: 0.07 + strength * 0.035, transparent: true, opacity: 0.78, vertexColors: true, blending: THREE.AdditiveBlending, depthWrite: false })
  return new THREE.Points(geometry, material)
}

function createLightning() {
  const vertices: number[] = []
  for (let bolt = 0; bolt < 5; bolt += 1) {
    let previous = new THREE.Vector3(Math.cos(bolt) * 1.1, -1.25, Math.sin(bolt) * 0.55)
    for (let segment = 1; segment <= 8; segment += 1) {
      const next = new THREE.Vector3(
        Math.cos(bolt + segment * 0.3) * (1.05 + (segment % 2) * 0.17),
        -1.25 + segment * 0.4,
        Math.sin(bolt + segment * 0.26) * 0.62,
      )
      vertices.push(previous.x, previous.y, previous.z, next.x, next.y, next.z)
      previous = next
    }
  }
  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3))
  const material = new THREE.LineBasicMaterial({ color: 0x82c6ff, transparent: true, opacity: 0.38, blending: THREE.AdditiveBlending })
  return new THREE.LineSegments(geometry, material)
}

export function AuraAvatar({ avatarType, progress }: Props) {
  const mountRef = useRef<HTMLDivElement>(null)
  const [webglFailed, setWebglFailed] = useState(false)

  useEffect(() => {
    const mount = mountRef.current
    if (!mount) return
    const width = mount.clientWidth
    const height = mount.clientHeight
    const scene = new THREE.Scene()
    scene.fog = new THREE.FogExp2(0x080b17, 0.1)
    const camera = new THREE.PerspectiveCamera(32, width / height, 0.1, 100)
    camera.position.set(0, 0.4, 7)

    let renderer: THREE.WebGLRenderer
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' })
      setWebglFailed(false)
    } catch {
      setWebglFailed(true)
      return
    }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.setSize(width, height)
    renderer.outputColorSpace = THREE.SRGBColorSpace
    mount.appendChild(renderer.domElement)

    scene.add(new THREE.HemisphereLight(0xa6c8ff, 0x120d22, 2.1))
    const keyLight = new THREE.DirectionalLight(0xffffff, 2.5)
    keyLight.position.set(3, 4, 4)
    scene.add(keyLight)

    const avatar = createAvatar(avatarType)
    avatar.position.y = -0.1
    scene.add(avatar)

    const active = compositeAbilities(progress)
    const strongest = [...Object.values(progress)].sort((a, b) => b.level - a.level)[0]
    const hasEffort = Object.values(progress).some((item) => item.xp > 0)
    const auraAbilities = !hasEffort ? [] : active.length >= 2 ? active : [strongest.ability]
    const averageStrength = auraAbilities.length ? auraAbilities.reduce((sum, ability) => sum + progress[ability].auraStrength, 0) / auraAbilities.length : 0
    const milestone = milestoneForLevel(strongest.level)
    const visualTier = visualTierForLevel(strongest.level)
    const particles = auraAbilities.length ? createParticles(auraAbilities, averageStrength, milestone, visualTier) : null
    if (particles) scene.add(particles)
    const lightning = auraAbilities.includes('intellect') ? createLightning() : null
    if (lightning) scene.add(lightning)
    const flames = auraAbilities.includes('vitality') ? createFlames(averageStrength, visualTier) : null
    if (flames) scene.add(flames)

    const rings = auraAbilities.map((ability, index) => {
      const geometry = new THREE.TorusGeometry(1.0 + index * 0.15, 0.018 + milestone / 5000, 8, 72)
      const material = new THREE.MeshBasicMaterial({ color: COLORS[ability], transparent: true, opacity: 0.25 + averageStrength * 0.36, blending: THREE.AdditiveBlending })
      const ring = new THREE.Mesh(geometry, material)
      ring.rotation.x = Math.PI / 2.4 + index * 0.16
      ring.position.y = -1.35 + index * 0.13
      scene.add(ring)
      return ring
    })

    const ground = auraAbilities.length ? new THREE.Mesh(
      new THREE.CircleGeometry(1.65, 64),
      new THREE.MeshBasicMaterial({ color: COLORS[strongest.ability], transparent: true, opacity: 0.08 + averageStrength * 0.1 }),
    ) : null
    if (ground) {
      ground.rotation.x = -Math.PI / 2
      ground.position.y = -1.65
      scene.add(ground)
    }

    let animationId = 0
    let contextAvailable = true
    const handleContextLost = (event: Event) => {
      event.preventDefault()
      contextAvailable = false
      cancelAnimationFrame(animationId)
      renderer.domElement.style.display = 'none'
      setWebglFailed(true)
    }
    renderer.domElement.addEventListener('webglcontextlost', handleContextLost)

    let frame = 0
    const animate = () => {
      if (!contextAvailable) return
      frame += 0.012
      avatar.position.y = -0.1 + Math.sin(frame * 1.35) * 0.035
      avatar.rotation.y = Math.sin(frame * 0.42) * 0.12
      if (particles) particles.rotation.y += 0.0025 + averageStrength * 0.002
      if (flames) {
        flames.rotation.y += 0.004
        flames.scale.y = 0.92 + Math.abs(Math.sin(frame * 4.5)) * (0.18 + averageStrength * 0.1)
      }
      if (lightning) {
        lightning.rotation.y -= 0.005
        ;(lightning.material as THREE.LineBasicMaterial).opacity = 0.18 + Math.abs(Math.sin(frame * 5.2)) * 0.34 * averageStrength
      }
      if (particles) {
        const positions = particles.geometry.attributes.position as THREE.BufferAttribute
        for (let index = 0; index < positions.count; index += 1) {
          let y = positions.getY(index) + 0.004 + averageStrength * 0.004
          if (y > 2.25) y = -1.5
          positions.setY(index, y)
        }
        positions.needsUpdate = true
      }
      rings.forEach((ring, index) => {
        ring.rotation.z += (index % 2 ? -1 : 1) * (0.003 + averageStrength * 0.003)
        const pulse = 1 + Math.sin(frame * 2 + index) * 0.035
        ring.scale.setScalar(pulse)
      })
      renderer.render(scene, camera)
      animationId = requestAnimationFrame(animate)
    }
    animate()

    const resize = () => {
      if (!mount) return
      const nextWidth = mount.clientWidth
      const nextHeight = mount.clientHeight
      camera.aspect = nextWidth / nextHeight
      camera.updateProjectionMatrix()
      renderer.setSize(nextWidth, nextHeight)
    }
    window.addEventListener('resize', resize)
    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener('resize', resize)
      renderer.domElement.removeEventListener('webglcontextlost', handleContextLost)
      renderer.dispose()
      scene.traverse((object) => {
        if (object instanceof THREE.Mesh || object instanceof THREE.Points || object instanceof THREE.LineSegments) {
          object.geometry.dispose()
          if (Array.isArray(object.material)) object.material.forEach((material) => material.dispose())
          else object.material.dispose()
        }
      })
      if (renderer.domElement.parentNode === mount) mount.removeChild(renderer.domElement)
    }
  }, [avatarType, progress])

  return <div className="avatar-canvas" ref={mountRef} aria-label="能力に応じて変化する3D分身">{webglFailed && <div className="webgl-fallback" role="img" aria-label="3D表示の代替分身"><div className={`fallback-avatar ${avatarType}`} /><strong>3D表示を利用できません</strong><span>記録と能力成長はそのまま利用できます。</span></div>}</div>
}
