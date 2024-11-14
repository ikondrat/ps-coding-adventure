import { render, screen, fireEvent } from '@testing-library/svelte'
import { vi } from 'vitest'
import TodoComponent from './index.svelte'
import { format } from 'date-fns'
import type { TodoItem } from '../../types'
import * as utils from '@/utils'

describe('TodoComponent', () => {
  const mockOnChange = vi.fn()

  const todo: TodoItem = {
    id: 1,
    title: 'Test Todo',
    state: 'TODO',
    updated_at: new Date().toISOString()
  }

  beforeEach(() => {
    vi.resetAllMocks() // Reset mocks before each test
  })

  test('renders the todo item with title, updated date, and state selector', () => {
    render(TodoComponent, {
      props: {
        todo,
        onChange: mockOnChange
      }
    })

    // Check if title is rendered
    expect(screen.getByText(todo.title)).toBeInTheDocument()

    // Check if the formatted updated date is displayed
    const formattedDate = format(new Date(todo.updated_at), 'PPpp')
    expect(screen.getByText(`updated: ${formattedDate}`)).toBeInTheDocument()

    // Check if all state options are rendered in the selector
    expect(screen.getByRole('option', { name: 'TODO' })).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'Ongoing' })).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'Done' })).toBeInTheDocument()
  })

  test('calls onChange with updated state when a valid state transition occurs', async () => {
    vi.spyOn(utils, 'isValidTransition').mockReturnValue(true) // Mock valid transition

    render(TodoComponent, {
      props: {
        todo,
        onChange: mockOnChange
      }
    })

    // Change the state to "ONGOING"
    const selectElement = screen.getByRole('combobox')
    await fireEvent.change(selectElement, { target: { value: 'ONGOING' } })

    // Verify that onChange was called with the updated state
    expect(mockOnChange).toHaveBeenCalledWith({
      ...todo,
      state: 'ONGOING',
      updated_at: expect.any(String) // Updated timestamp
    })
    expect(screen.queryByText('Invalid transition')).not.toBeInTheDocument()
  })

  test('displays an error message when an invalid state transition occurs', async () => {
    vi.spyOn(utils, 'isValidTransition').mockReturnValue(false) // Mock invalid transition

    render(TodoComponent, {
      props: {
        todo,
        onChange: mockOnChange
      }
    })

    // Attempt to change the state to "DONE"
    const selectElement = screen.getByRole('combobox')
    await fireEvent.change(selectElement, { target: { value: 'DONE' } })

    // Verify that onChange was not called due to invalid transition
    expect(mockOnChange).not.toHaveBeenCalled()
    // Verify that error message is displayed
    expect(screen.getByText('Invalid transition')).toBeInTheDocument()
  })
})
