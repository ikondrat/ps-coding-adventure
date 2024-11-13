import { describe, it, expect, beforeEach, vi } from 'vitest'
import type { User, Board, TodoItem } from '@/types'
import { client } from '../todos/client'
import { getBoardTodos } from '../todos/getBoardTodos'
import { getCurrentUserBoard } from '../todos/getCurrentUserBoard'
import { getSessionUser } from '../todos/getSessionUser'
import { signin } from '../todos/signin'

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
      .mockResolvedValue({ data: [{ id: 'board1', name: 'Test Board' }] })

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

  // New test for getBoardTodos
  it('getBoardTodos should return an error if no board or user is in sessionStorage', async () => {
    const result = await getBoardTodos()
    expect(result.error).toBe('User must be signed in and have a board to get todos.')
  })

  it('getBoardTodos should return todos if user and board are present in sessionStorage', async () => {
    const user: User = { id: '1', name: 'Test User' }
    const board: Board = { id: 'board1', name: 'Test Board', access_key: 'board1' }
    const todos: TodoItem[] = [
      { id: 'todo1', title: 'Test Todo', board_id: board.id, state: 'TODO' }
    ]

    window.sessionStorage.setItem('currentUser', JSON.stringify(user))
    window.sessionStorage.setItem('currentBoard', JSON.stringify(board))

    const mockGet = vi.spyOn(client, 'GET').mockResolvedValue({ data: todos })

    const result = await getBoardTodos()
    expect(result.data).toEqual(todos)
    expect(result.error).toBeUndefined()

    mockGet.mockRestore()
  })

  it('getBoardTodos should return an error message if API call fails', async () => {
    const user: User = { id: '1', name: 'Test User' }
    const board: Board = { id: 'board1', name: 'Test Board', access_key: 'board1' }

    window.sessionStorage.setItem('currentUser', JSON.stringify(user))
    window.sessionStorage.setItem('currentBoard', JSON.stringify(board))

    const mockGet = vi.spyOn(client, 'GET').mockImplementation(() => {
      throw new Error('API error')
    })

    const result = await getBoardTodos()
    expect(result.data).toBeUndefined()
    expect(result.error).toBe('Error: API error')

    mockGet.mockRestore()
  })
})
