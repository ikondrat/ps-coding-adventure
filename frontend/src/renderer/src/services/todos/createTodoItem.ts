import type { AsyncResolver, TodoItem } from '@/types'
import { getSessionBoard } from './getSessionBoard'
import { getSessionUser } from './getSessionUser'
import { client } from './client'

export const createTodoItem: AsyncResolver<string, TodoItem> = async function (title) {
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
        state: 'TODO',
        state_details: ''
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
