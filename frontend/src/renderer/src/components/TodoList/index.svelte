<script lang="ts">
  import { onMount } from 'svelte'
  import Todo from '@/components/Todo/index.svelte'

  import type { Board } from '../../types'
  import { getCurrentUserBoard, joinOrCreateBoard } from '../../services/api'

  let boardName = ''
  let todos = {
    todo: [
      { id: 1, title: 'First TODO', updatedAt: new Date() },
      { id: 2, title: 'Second TODO', updatedAt: new Date() },
      { id: 3, title: 'Third TODO', updatedAt: new Date() }
    ],
    ongoing: [],
    done: []
  }

  let currentBoard: Board | undefined

  onMount(async () => {
    // Use onMount to fetch the board
    currentBoard = await getCurrentUserBoard() // Await the async function
  })

  function addTodo() {
    alert('add todo')
  }

  async function handleBoardAction() {
    const result = await joinOrCreateBoard(boardName)
    debugger
  }
</script>

{#if currentBoard}
  <header class="text-2xl font-bold mb-4">TODO List: {currentBoard.name}</header>
  <div class="flex">
    <div class="w-1/3 p-4">
      <h2 class="text-lg font-bold">TODO</h2>
      <button on:click={addTodo} class="bg-blue-500 text-white p-2 rounded">Add TODO</button>
      {#each todos.todo as todo, index}
        <Todo title={todo.title} updated={todo.updatedAt.toLocaleString()} data-index={index} />
      {/each}
    </div>
    <div class="w-1/3 p-4">
      <h2 class="text-lg font-bold">ONGOING</h2>
      {#each todos.ongoing as todo, index}
        <Todo title={todo.title} updated={todo.updatedAt.toLocaleString()} data-index={index} />
      {/each}
    </div>
    <div class="w-1/3 p-4">
      <h2 class="text-lg font-bold">DONE</h2>
      {#each todos.done as todo, index}
        <Todo title={todo.title} updated={todo.updatedAt.toLocaleString()} data-index={index} />
      {/each}
    </div>
  </div>
{:else}
  <div class="flex flex-col items-center">
    <h2 class="text-lg font-bold mb-4">No Board Found</h2>
    <p class="mb-4">
      Enter a name for your board. You can create a new board or open an existing one by this name.
    </p>
    <input
      type="text"
      placeholder="Enter board name"
      bind:value={boardName}
      class="border p-2 mb-2"
    />
    <button on:click={handleBoardAction} class="bg-blue-500 text-white p-2 rounded">Proceed</button>
  </div>
{/if}
