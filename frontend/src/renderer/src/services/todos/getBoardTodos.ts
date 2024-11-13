import type { ResultOrError, TodoItem } from '@/types'
import { getSessionBoard } from './getSessionBoard'
import { getSessionUser } from './getSessionUser'
import { client } from './client'

export const getBoardTodos = async (): Promise<ResultOrError<TodoItem[], string>> => {
  const board = getSessionBoard()
  const user = getSessionUser()

  let resultOk: TodoItem[] | undefined = undefined
  let resultError: string | undefined = undefined

  if (!board || !user) {
    return {
      data: undefined,
      error: 'User must be signed in and have a board to get todos.'
    }
  }

  try {
    const { data, error } = await client.GET('/boards/{board_id}/todos/', {
      params: {
        path: {
          board_id: board.id
        }
      }
    })

    if (error) {
      resultError = error.detail.toString()
    }
    resultOk = data
  } catch (e) {
    resultError = e.toString()
  }

  return {
    data: resultOk,
    error: resultError
  }
}
