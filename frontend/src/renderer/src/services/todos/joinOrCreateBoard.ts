import type { Board } from '@/types'
import { getSessionUser } from './getSessionUser'
import { client } from './client'

// Join or create a board
export const joinOrCreateBoard = async (boardName: string): Promise<Board> => {
  const storedBoard = sessionStorage.getItem('currentBoard')
  if (storedBoard) {
    return JSON.parse(storedBoard)
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
      throw new Error(error.detail.toString())
    }
    result = data as Board
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
