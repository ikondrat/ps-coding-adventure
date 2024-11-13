import type { Board } from '@/types'

export const getSessionBoard = (): Board | null => {
  // Check if currentUser exists in session storage
  const storedBoard = sessionStorage.getItem('currentBoard')
  return storedBoard ? (JSON.parse(storedBoard) as Board) : null // Return the user or null if not found
}
