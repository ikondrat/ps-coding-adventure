import type { User } from '@/types'
import { client } from './client'

export const signin = async (name: string): Promise<User> => {
  // Check if currentUser exists in session storage
  const storedUser = sessionStorage.getItem('currentUser')
  if (storedUser) {
    return JSON.parse(storedUser) as User // Return the stored user
  }

  const { data } = await client.POST('/signin', {
    body: {
      name
    }
  })

  // Store the user in session storage
  sessionStorage.setItem('currentUser', JSON.stringify(data))

  return data as User
}
