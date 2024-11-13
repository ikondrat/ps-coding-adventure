/* eslint-disable @typescript-eslint/explicit-function-return-type */
/* eslint-disable @typescript-eslint/no-unused-vars */
import createClient from 'openapi-fetch'

import type { paths } from '../../../types/api'
import type { User } from '@/types'
import type { Board, TodoItem } from '../types'

export const client = createClient<paths>({ baseUrl: 'http://localhost:8000/' })

export const signin = async (name: string): Promise<User> => {
  // Check if currentUser exists in session storage
  const storedUser = sessionStorage.getItem('currentUser')
  if (storedUser) {
    return JSON.parse(storedUser) as User // Return the stored user
  }

  const { data } = await client.POST('/signin', {
    body: {
      name
    }
  })

  // Store the user in session storage
  sessionStorage.setItem('currentUser', JSON.stringify(data))

  return data as User
}

export const getCurrentUserBoard = async (): Promise<Board | null> => {
  const user = getSessionUser()
  let result: Board | undefined

  const storedBoard = getSessionBoard()

  if (storedBoard) {
    return storedBoard
  }
  try {
    const { data } = await client.GET('/users/{user_id}/boards', {
      params: {
        path: {
          user_id: user.id
        }
      }
    })
    result = data as unknown as Board
  } catch (e) {
    // it means there is no board
    result = undefined
  }

  return result
}

export const getSessionUser = (): User | null => {
  // Check if currentUser exists in session storage
  const storedUser = sessionStorage.getItem('currentUser')
  return storedUser ? (JSON.parse(storedUser) as User) : null // Return the user or null if not found
}

export const getSessionBoard = (): Board | null => {
  // Check if currentUser exists in session storage
  const storedBoard = sessionStorage.getItem('currentBoard')
  return storedBoard ? (JSON.parse(storedBoard) as Board) : null // Return the user or null if not found
}

// Join or create a board
export const joinOrCreateBoard = async (boardName: string): Promise<Board> => {
  const storedBoard = sessionStorage.getItem('currentBoard')
  if (storedBoard) {
    return JSON.parse(storedBoard) as User // Return the stored user
  }

  const user = getSessionUser()
  if (!user) {
    throw new Error('User must be signed in to join or create a board.')
  }

  let result: Board | undefined
  try {
    // Attempt to join the existing board
    const { data, error } = await client.GET(`/boards/{access_key}`, {
      params: {
        path: {
          access_key: boardName
        }
      }
    })
    if (error) {
      throw new Error(error.detail)
    }
    result = data as Board // Return the existing board
  } catch (e) {
    // If the board does not exist, create a new one
    const { data } = await client.POST('/boards/', {
      body: {
        name: boardName,
        access_key: boardName,
        user_id: user.id // Assuming the API requires userId to create a board
      }
    })
    result = data as Board // Return the newly created board
  }

  // Store the user in session storage
  sessionStorage.setItem('currentBoard', JSON.stringify(result))

  return result
}

type ResultOrError<T> = {
  data?: T
  error?: string
}

export const createTodoItem = async function (title: string): Promise<ResultOrError<TodoItem>> {
  const board = getSessionBoard()
  let resultOK: TodoItem | undefined = undefined
  let resultError: string | undefined = undefined

  const user = getSessionUser()

  try {
    if (!user) {
      throw new Error('User must be signed in to join or create a board.')
    }
    if (!board) {
      throw new Error('User needs to have a board to add a todo.')
    }
    const { data, error } = await client.POST('/todos/', {
      body: {
        board_id: board.id,
        user_id: user.id,
        title,
        state: 'TODO'
      }
    })

    if (error) {
      throw new Error('Failed to add todo: ' + error)
    }

    resultOK = data as TodoItem
  } catch (e) {
    resultError = String(e)
  }

  return {
    data: resultOK,
    error: resultError
  }
}
