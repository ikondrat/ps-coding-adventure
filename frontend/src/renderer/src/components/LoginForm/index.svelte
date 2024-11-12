<script lang="ts">
  export let title: string
  export let onLogin: () => void
  let userName = ''
  let selectedList: string = 'Drama'
  let newListName: string = ''
  let isCreatingNewList: boolean = false

  function login(): void {
    onLogin()
  }
</script>

<h2 class="text-lg font-bold mb-4">Login {title}</h2>

<label class="block mb-2">
  <input type="checkbox" bind:checked={isCreatingNewList} class="mr-2" />
  Create a new todo list
</label>

{#if isCreatingNewList}
  <input
    type="text"
    placeholder="Enter new list name"
    bind:value={newListName}
    class="border p-2 mb-4"
  />
{:else}
  <select bind:value={selectedList} class="border p-2 mb-4 w-full">
    <option value="Drama">Drama</option>
    <option value="Fire">Fire</option>
    <option value="Urgent">Urgent</option>
  </select>
{/if}

<label class="block mb-2">
  <input type="text" placeholder="Enter your name" bind:value={userName} class="border p-2 mb-4" />
</label>

<button on:click={login} class="bg-blue-500 text-white p-2 rounded w-full">Login</button>
