import createClient from 'openapi-fetch'

import type { paths } from '../../../types/api'

// declare fetcher for paths
const fetcher = Fetcher.for<paths>()

const client = createClient<paths>({ baseUrl: 'http://localhost:8000/' })

// global configuration
fetcher.configure({
  baseUrl: 'http://localhost:8000/docs'
})

export const getUsers = fetcher.path('/users/').method('get').create()
export const createUser = fetcher.path('/users/').method('post').create()
export const getUser = fetcher.path('/users/{user_id}').method('get').create()

export const loginOrCreateUser = async (user: string) => {
  const {
    data: { name },
    error
  } = await client.GET('/users/{user_id}', {
    params: {
      path: { user_id: user }
    }
  })

  if (error) {
    return error
  }
  if (name) {
    return name
  }
}

fetcher.path('/login-or-create-user/').method('post').create()
