import { client } from './client'
import type { ResultOrError, TodoItem } from '@/types'

export const updateTodo = (todo): Promise<ResultOrError<TodoItem>> =>
  client.PUT('/todos/{todo_id}', {
    params: {
      path: {
        todo_id: todo.id
      }
    },
    body: {
      board_id: todo.board_id,
      user_id: todo.user_id,
      title: todo.title,
      state: todo.state
    }
  }) as Promise<ResultOrError<TodoItem>>
