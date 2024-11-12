/* eslint-disable @typescript-eslint/explicit-function-return-type */
/* eslint-disable @typescript-eslint/no-unused-vars */
import createClient from 'openapi-fetch'

import type { paths } from '../../../types/api'
import type { User } from '@/types'

export const client = createClient<paths>({ baseUrl: 'http://localhost:8000/' })

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

export const getSessionUser = (): User | null => {
  // Check if currentUser exists in session storage
  const storedUser = sessionStorage.getItem('currentUser')
  return storedUser ? (JSON.parse(storedUser) as User) : null // Return the user or null if not found
}
