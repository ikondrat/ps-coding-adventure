import type { ResultOrError, TodoItem } from '@/types'
import { client } from './client'

export const getBoardTodos = async (
  board_id: string
): Promise<ResultOrError<TodoItem[], string>> => {
  let resultOk: TodoItem[] | undefined = undefined
  let resultError: string | undefined = undefined

  try {
    const { data, error } = await client.GET('/boards/{board_id}/todos/', {
      params: {
        path: {
          board_id
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
