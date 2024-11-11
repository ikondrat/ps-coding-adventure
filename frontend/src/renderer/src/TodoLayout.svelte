<script lang="ts">
  //   import { loginOrCreateUser } from './services/api'
  let userName = ''
  let isLoggedIn = false // Track the login state

  let todos = {
    todo: [
      { id: 1, title: 'First TODO', updatedAt: new Date() },
      { id: 2, title: 'Second TODO', updatedAt: new Date() },
      { id: 3, title: 'Third TODO', updatedAt: new Date() }
    ],
    ongoing: [],
    done: []
  }

  //   function addTodo() {
  //     // Logic to add a new todo
  //   }

  function login(): void {
    isLoggedIn = true
    userName = 'tester2'

    //loginOrCreateUser('teststs')
    // getUsers().then((users) => {
    //   console.log(users)
    // })
  }
</script>

<div class="flex">
  <div class="w-1/3 p-4">
    <h2 class="text-lg font-bold">TODO</h2>
    {#each todos.todo as todo}
      <div class="bg-white p-4 mb-2 rounded shadow">
        <h3 class="font-semibold">{todo.title}</h3>
        <p class="text-gray-600">Last updated: {todo.updatedAt.toLocaleString()}</p>
      </div>
    {/each}
  </div>
  <div class="w-1/3 p-4">
    <h2 class="text-lg font-bold">ONGOING</h2>
    <!-- ONGOING cards will be rendered here -->
  </div>
  <div class="w-1/3 p-4">
    <h2 class="text-lg font-bold">DONE</h2>
    <!-- DONE cards will be rendered here -->
  </div>
</div>

{#if !isLoggedIn}
  <div
    class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-gray-800 bg-opacity-50"
  >
    <div class="bg-white p-6 rounded shadow-md">
      <h2 class="text-lg font-bold">Login</h2>
      <input type="text" placeholder="Enter your name" bind:value={userName} class="border p-2" />
      <button on:click={login} class="bg-blue-500 text-white p-2 rounded">Login</button>
    </div>
  </div>
{/if}
