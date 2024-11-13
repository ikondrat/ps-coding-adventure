import type { User } from '@/types'

export const getSessionUser = (): User | null => {
  // Check if currentUser exists in session storage
  const storedUser = sessionStorage.getItem('currentUser')
  return storedUser ? (JSON.parse(storedUser) as User) : null // Return the user or null if not found
}
