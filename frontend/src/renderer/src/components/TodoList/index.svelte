<script lang="ts">
  import { onMount } from 'svelte'
  import Todo from '../Todo/index.svelte'
  import FormTodo from '../FormTodo/index.svelte'

  import type { Board, TodoItem } from '../../types'
  import { createTodoItem, getCurrentUserBoard, joinOrCreateBoard } from '../../services/api'

  let boardName = ''
  let showAddTodoForm = false
  let addTodoError = ''

  let todos: TodoItem[] = []

  let currentBoard: Board | undefined

  onMount(async () => {
    // Use onMount to fetch the board
    currentBoard = await getCurrentUserBoard()
  })

  function handleAddButtonClick() {
    showAddTodoForm = !showAddTodoForm
  }

  async function handleAddTodoSubmit(text: string) {
    const { data, error } = await createTodoItem(text)

    if (error) {
      addTodoError = error
      return
    } else {
      todos = [...todos, data]
      showAddTodoForm = false
    }
  }

  async function handleBoardAction() {
    const result = await joinOrCreateBoard(boardName)
  }

  async function handleTodoChange(todo: TodoItem) {
    debugger
    todos = [...todos.filter((t) => t.id !== todo.id), todo]
  }
</script>

{#if currentBoard}
  <div class="flex">
    <div class="w-full p-4">
      <!-- Changed from w-1/3 to w-1/2 -->
      <header class="text-2xl font-bold mb-4">TODO List: {currentBoard.name}</header>
    </div>
    <div class="w-1/2 p-4">
      <button on:click={handleAddButtonClick} class="bg-blue-500 text-white p-2 rounded"
        >Add TODO</button
      >
      {#if showAddTodoForm}
        <FormTodo onSubmit={handleAddTodoSubmit} error={addTodoError} />
      {/if}
    </div>
    <!-- Removed the DONE section for a two-column layout -->
  </div>

  <div class="flex">
    <div class="w-1/3 p-4">
      <h2 class="text-lg font-bold">TODO</h2>
      {#each todos.filter((todo) => todo.state === 'TODO') as todo}
        <Todo {todo} onChange={handleTodoChange} />
      {/each}
    </div>
    <div class="w-1/3 p-4">
      <h2 class="text-lg font-bold">ONGOING</h2>
      {#each todos.filter((todo) => todo.state === 'ONGOING') as todo}
        <Todo {todo} onChange={handleTodoChange} />
      {/each}
    </div>
    <div class="w-1/3 p-4">
      <h2 class="text-lg font-bold">DONE</h2>
      {#each todos.filter((todo) => todo.state === 'DONE') as todo}
        <Todo {todo} onChange={handleTodoChange} />
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
