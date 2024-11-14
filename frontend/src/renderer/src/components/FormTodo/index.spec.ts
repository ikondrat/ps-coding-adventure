import { render, screen, fireEvent } from '@testing-library/svelte'
import userEvent from '@testing-library/user-event'
import AddTodo from './index.svelte'
import { vi } from 'vitest'

describe('AddTodo Component', () => {
  const mockOnSubmit = vi.fn()

  beforeEach(() => {
    vi.resetAllMocks() // Clear mocks before each test
  })

  test('renders the Add TODO form with title and placeholder text', () => {
    render(AddTodo, {
      props: {
        onSubmit: mockOnSubmit,
        error: ''
      }
    })

    // Check if the title is rendered
    expect(screen.getByText('Add TODO')).toBeInTheDocument()

    // Check if the input field with placeholder text is rendered
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument()

    // Check if the "add" button is rendered
    expect(screen.getByRole('button', { name: 'add' })).toBeInTheDocument()
  })

  test('displays error message when error prop is provided', () => {
    render(AddTodo, {
      props: {
        onSubmit: mockOnSubmit,
        error: 'This is an error message'
      }
    })

    // Check if the error message is displayed inside AlertError component
    expect(screen.getByText('This is an error message')).toBeInTheDocument()
  })

  test('calls onSubmit with todo text when add button is clicked', async () => {
    render(AddTodo, {
      props: {
        onSubmit: mockOnSubmit,
        error: ''
      }
    })

    // Type a todo text into the input field
    const todoInput = screen.getByPlaceholderText('Enter text')
    await userEvent.type(todoInput, 'Buy groceries')

    // Click the "add" button
    const addButton = screen.getByRole('button', { name: 'add' })
    await fireEvent.click(addButton)

    // Check if onSubmit is called with the typed text
    expect(mockOnSubmit).toHaveBeenCalledWith('Buy groceries')
  })

  test('calls onSubmit with todo text when Enter key is pressed', async () => {
    render(AddTodo, {
      props: {
        onSubmit: mockOnSubmit,
        error: ''
      }
    })

    // Type a todo text into the input field and press Enter
    const todoInput = screen.getByPlaceholderText('Enter text')
    await userEvent.type(todoInput, 'Finish homework{enter}')

    // Check if onSubmit is called with the typed text when Enter is pressed
    expect(mockOnSubmit).toHaveBeenCalledWith('Finish homework')
  })
})
