import type { Board } from '@/types'
import { getSessionUser } from './getSessionUser'
import { getSessionBoard } from './getSessionBoard'
import { client } from './client'

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
    result = data[0] as unknown as Board

    // Store the user in session storage
    sessionStorage.setItem('currentBoard', JSON.stringify(result))
  } catch (e) {
    // it means there is no board
    result = undefined
  }

  return result
}
