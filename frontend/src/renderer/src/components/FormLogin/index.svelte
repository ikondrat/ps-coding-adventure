<script lang="ts">
  import { signin } from '@/services/api'
  import type { User } from '../../types'
  export let onLogin: (user: User) => void
  let userName = ''
  let newTodoListName: string = ''
  let todoListAccessKey: string = ''
  let isCreatingNewList: boolean = false

  async function login(): Promise<void> {
    const result = await signin(userName)
    onLogin(result)
  }
</script>

<div
  class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-gray-800 bg-opacity-50"
>
  <div class="bg-white p-6 rounded shadow-md">
    <h2 class="text-lg font-bold mb-4">Signin/signup</h2>

    <p class="block mb-2">You almost ready to go, lets start from the login!</p>

    <label class="block mb-2">
      <input
        type="text"
        placeholder="Enter your name"
        bind:value={userName}
        class="border p-2 mb-4 w-full"
      />
    </label>

    <!-- <p class="block mb-2">Create new TODO list or use existing by access key</p>
    <label class="block mb-2">
      <input type="checkbox" bind:checked={isCreatingNewList} class="mr-2" />
      Create a new todo list
    </label>
    {#if isCreatingNewList}
      <input
        type="text"
        placeholder="Enter new list name"
        bind:value={newTodoListName}
        class="border p-2 mb-4 w-full"
      />
    {:else}
      <input
        type="text"
        placeholder="Enter access key"
        bind:value={todoListAccessKey}
        class="border p-2 mb-4 w-full"
      />
    {/if} -->

    <button on:click={login} class="bg-blue-500 text-white p-2 rounded w-full">Login</button>
  </div>
</div>
