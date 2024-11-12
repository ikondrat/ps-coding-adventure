/* eslint-disable @typescript-eslint/explicit-function-return-type */
/* eslint-disable @typescript-eslint/no-unused-vars */
import createClient, { type Middleware } from 'openapi-fetch'

import type { paths } from '../../../types/api'
import type { User } from '@/types'

export const client = createClient<paths>({ baseUrl: 'http://localhost:8000/' })

export const signin = async (name: string): Promise<User> => {
  const { data } = await client.POST('/signin', {
    body: {
      name
    }
  })

  return data as User
}
// const myMiddleware: Middleware = {
//   async onRequest({ request }) {
//     // set "foo" header
//     request.headers.set('foo', 'bar')
//     return request
//   },
//   async onResponse({ request, response, options }) {
//     const { body, ...resOptions } = response
//     // change status of response
//     return new Response(body, { ...resOptions, status: 200 })
//   }
// }

// client.use(myMiddleware)
