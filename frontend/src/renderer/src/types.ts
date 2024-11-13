export type User = {
  name: string
  id: string
}

export type Board = {
  id: string
  name: string
  access_key: string
}

export type TodoItemState = 'TODO' | 'ONGOING' | 'DONE'

export type TodoItem = {
  id: string
  title: string
  state: TodoItemState
  updated_at?: string
  created_at?: string
}

export type ResultOrError<T, E = string> = {
  data?: T
  error?: E
}

export type AsyncResolver<I, T, E = string> = (value: I) => Promise<ResultOrError<T, E>>
