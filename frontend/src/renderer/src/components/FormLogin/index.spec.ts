import { render, screen, fireEvent } from '@testing-library/svelte'
import userEvent from '@testing-library/user-event'
import Login from './index.svelte'
import { vi } from 'vitest'
import * as signin from '@/services/todos/signin'

describe('Login Component', () => {
  const mockOnLogin = vi.fn()

  beforeEach(() => {
    // Clear the mock before each test
    vi.resetAllMocks()
  })

  test('renders the login form with title and placeholder text', () => {
    render(Login, {
      props: {
        onLogin: mockOnLogin
      }
    })

    // Check if title is rendered
    expect(screen.getByText('Signin/signup')).toBeInTheDocument()

    // Check if input field placeholder is correct
    expect(screen.getByPlaceholderText('Enter your name')).toBeInTheDocument()

    // Check if login button is rendered
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument()
  })

  test('calls onLogin with user when login button is clicked', async () => {
    const mockedSignin = vi.spyOn(signin, 'signin')
    render(Login, {
      props: {
        onLogin: vi.fn()
      }
    })

    // Type a username into the input field
    const usernameInput = screen.getByPlaceholderText('Enter your name')
    await userEvent.type(usernameInput, 'testuser')

    // Click the login button
    const loginButton = screen.getByRole('button', { name: 'Login' })
    await fireEvent.click(loginButton)

    // Check if signin function is called and onLogin is invoked
    expect(mockedSignin).toHaveBeenCalled()
  })

  test('calls login function when Enter key is pressed in the input field', async () => {
    const mockedSignin = vi.spyOn(signin, 'signin')
    render(Login, {
      props: {
        onLogin: vi.fn()
      }
    })

    const usernameInput = screen.getByPlaceholderText('Enter your name')
    await userEvent.type(usernameInput, 'testuser{enter}')

    expect(mockedSignin).toHaveBeenCalled()
  })
})
