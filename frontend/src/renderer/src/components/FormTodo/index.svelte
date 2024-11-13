<script lang="ts">
  import { handleEnter } from '@/utils'
  import AlertError from '../AlertError/index.svelte'
  export let onSubmit: (text: string) => void
  let todoText = ''
  export let error = ''

  function addTodo(): void {
    onSubmit(todoText)
  }
</script>

<div
  class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-gray-800 bg-opacity-50"
>
  <div class="bg-white p-6 rounded shadow-md">
    <h2 class="text-lg font-bold mb-4">Add TODO</h2>

    <label class="block mb-2">
      <input
        type="text"
        placeholder="Enter text"
        bind:value={todoText}
        on:keydown={handleEnter(addTodo)}
        class="border p-2 mb-4 w-full"
      />
    </label>
    {#if error}
      <div class="block mb-2">
        <AlertError>
          {error}
        </AlertError>
      </div>
    {/if}

    <button on:click={addTodo} class="bg-blue-500 text-white p-2 rounded w-full">add</button>
  </div>
</div>
