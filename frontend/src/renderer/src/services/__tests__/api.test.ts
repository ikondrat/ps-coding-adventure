import { client } from '../api'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { signin, getCurrentUserBoard, getSessionUser } from '../api'
import type { User } from '@/types'

// Mock the sessionStorage
const mockSessionStorage = (() => {
  let store: { [key: string]: string } = {}
  return {
    getItem(key: string) {
      return store[key] || null
    },
    setItem(key: string, value: string) {
      store[key] = value
    },
    clear() {
      store = {}
    }
  }
})()

Object.defineProperty(window, 'sessionStorage', {
  value: mockSessionStorage
})

describe('API Service Tests', () => {
  beforeEach(() => {
    // Clear sessionStorage before each test
    window.sessionStorage.clear()
  })

  it('signin should return user from sessionStorage if exists', async () => {
    const user: User = { id: '1', name: 'Test User' }
    window.sessionStorage.setItem('currentUser', JSON.stringify(user))

    const result = await signin('Test User')
    expect(result).toEqual(user)
  })

  it('signin should store user in sessionStorage if not exists', async () => {
    const user: User = { id: '1', name: 'Test User' }
    const mockPost = vi.spyOn(client, 'POST').mockResolvedValue({ data: user })

    const result = await signin('Test User')
    expect(result).toEqual(user)
    expect(window.sessionStorage.getItem('currentUser')).toEqual(JSON.stringify(user))

    mockPost.mockRestore()
  })

  it('getSessionUser should return user from sessionStorage', () => {
    const user: User = { id: '1', name: 'Test User' }
    window.sessionStorage.setItem('currentUser', JSON.stringify(user))

    const result = getSessionUser()
    expect(result).toEqual(user)
  })

  it('getSessionUser should return null if no user in sessionStorage', () => {
    const result = getSessionUser()
    expect(result).toBeNull()
  })

  it('getCurrentUserBoard should return board for the user', async () => {
    const user: User = { id: '1', name: 'Test User' }
    window.sessionStorage.setItem('currentUser', JSON.stringify(user))

    const mockGet = vi
      .spyOn(client, 'GET')
      .mockResolvedValue({ data: { id: 'board1', name: 'Test Board' } })

    const result = await getCurrentUserBoard()
    expect(result).toEqual({ id: 'board1', name: 'Test Board' })

    mockGet.mockRestore()
  })

  it('getCurrentUserBoard should return undefined if no board found', async () => {
    const user: User = { id: '1', name: 'Test User' }
    window.sessionStorage.setItem('currentUser', JSON.stringify(user))

    const mockGet = vi.spyOn(client, 'GET').mockImplementation(() => {
      throw new Error('No board found')
    })

    const result = await getCurrentUserBoard()
    expect(result).toBeUndefined()

    mockGet.mockRestore()
  })
})
