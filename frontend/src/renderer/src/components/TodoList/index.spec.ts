import { render, screen, fireEvent } from '@testing-library/svelte'
import { vi } from 'vitest'
import BoardComponent from './index.svelte'
import * as joinOrCreateBoard from '@/services/todos/joinOrCreateBoard'
import * as getBoardTodos from '@/services/todos/getBoardTodos'
import * as createTodoItem from '@/services/todos/createTodoItem'
import * as updateTodo from '@/services/todos/updateTodo'
import type { TodoItem } from '../../types'

describe('BoardComponent', () => {
  const mockTodo: TodoItem = {
    id: 1,
    title: 'Test Todo',
    state: 'TODO',
    updated_at: new Date().toISOString()
  }
  const mockBoard = {
    id: 'board-id',
    name: 'My Test Board',
    access_key: 'test-access-key'
  }

  beforeEach(() => {
    vi.resetAllMocks()
  })

  test('renders with "No Board Found" message when no board exists', () => {
    render(BoardComponent)

    expect(screen.getByText('No Board Found')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Enter board name')).toBeInTheDocument()
  })

  test('creates or joins a board and displays it', async () => {
    vi.spyOn(joinOrCreateBoard, 'joinOrCreateBoard').mockResolvedValue(mockBoard)
    vi.spyOn(getBoardTodos, 'getBoardTodos').mockResolvedValue({ data: [mockTodo], error: null })

    render(BoardComponent)

    const boardInput = screen.getByPlaceholderText('Enter board name')
    await fireEvent.input(boardInput, { target: { value: 'Test Board' } })
    const proceedButton = screen.getByRole('button', { name: 'Proceed' })
    await fireEvent.click(proceedButton)

    expect(screen.getByText('TODO')).toBeInTheDocument()
  })

  test('displays an error message if fetching todos fails', async () => {
    vi.spyOn(joinOrCreateBoard, 'joinOrCreateBoard').mockResolvedValue(mockBoard)
    vi.spyOn(getBoardTodos, 'getBoardTodos').mockResolvedValue({
      data: null,
      error: 'Failed to load todos'
    })

    render(BoardComponent)

    const proceedButton = screen.getByRole('button', { name: 'Proceed' })
    await fireEvent.click(proceedButton)

    expect(await screen.findByText('Failed to load todos')).toBeInTheDocument()
  })

  test.skip('adds a new todo item to the board', async () => {
    vi.spyOn(createTodoItem, 'createTodoItem').mockResolvedValue({ data: mockTodo, error: null })

    render(BoardComponent, { currentBoard: mockBoard })

    const addButton = screen.getByRole('button', { name: 'Add TODO' })
    await fireEvent.click(addButton)

    const todoInput = screen.getByPlaceholderText('Enter text')
    await fireEvent.input(todoInput, { target: { value: 'New Todo' } })
    const submitButton = screen.getByRole('button', { name: 'add' })
    await fireEvent.click(submitButton)

    expect(await screen.findByText('New Todo')).toBeInTheDocument()
  })

  test.skip('displays an error when adding a todo fails', async () => {
    vi.spyOn(createTodoItem, 'createTodoItem').mockResolvedValue({
      data: null,
      error: 'Failed to create todo'
    })

    render(BoardComponent, { currentBoard: mockBoard })

    const addButton = screen.getByRole('button', { name: 'Add TODO' })
    await fireEvent.click(addButton)

    const submitButton = screen.getByRole('button', { name: 'add' })
    await fireEvent.click(submitButton)

    expect(await screen.findByText('Failed to create todo')).toBeInTheDocument()
  })

  test.skip('updates todo item state', async () => {
    const updatedTodo = { ...mockTodo, state: 'DONE' }
    vi.spyOn(updateTodo, 'updateTodo').mockResolvedValue({ data: updatedTodo, error: null })

    render(BoardComponent, { currentBoard: mockBoard, todos: [mockTodo] })

    const todoSelect = screen.getByRole('combobox')
    await fireEvent.change(todoSelect, { target: { value: 'DONE' } })

    expect(await screen.findByText('DONE')).toBeInTheDocument()
  })

  test.skip('copies the access key to the clipboard', async () => {
    Object.assign(navigator, {
      clipboard: {
        writeText: vi.fn()
      }
    })

    render(BoardComponent, { currentBoard: mockBoard })

    const copyButton = screen.getByTitle('Copy access key')
    await fireEvent.click(copyButton)

    expect(navigator.clipboard.writeText).toHaveBeenCalledWith(mockBoard.access_key)
  })
})
