<script lang="ts">
  import { onMount } from 'svelte'
  import Todo from '../Todo/index.svelte'
  import FormTodo from '../FormTodo/index.svelte'

  import type { Board, TodoItem } from '../../types'
  import { createTodoItem } from '@/services/todos/createTodoItem'
  import { getCurrentUserBoard } from '@/services/todos/getCurrentUserBoard'
  import { joinOrCreateBoard } from '@/services/todos/joinOrCreateBoard'
  import { getBoardTodos } from '@/services/todos/getBoardTodos'
  import { updateTodo } from '@/services/todos/updateTodo'

  let boardName = ''
  let showAddTodoForm = false
  let addTodoError = ''

  let todos: TodoItem[] = []

  let currentBoard: Board | undefined
  let boardError: string | undefined = undefined

  onMount(async () => {
    // Use onMount to fetch the board
    currentBoard = await getCurrentUserBoard()

    if (currentBoard) {
      const { data, error } = await getBoardTodos(currentBoard.id)

      if (error) {
        boardError = error
      } else {
        todos = [...data]
      }
    }
  })

  function handleAddButtonClick(): void {
    showAddTodoForm = !showAddTodoForm
  }

  async function handleAddTodoSubmit(text: string): Promise<void> {
    const { data, error } = await createTodoItem(text)

    if (error) {
      addTodoError = error
      return
    } else {
      todos = [...todos, data]
      showAddTodoForm = false
    }
  }

  async function handleBoardAction(): Promise<void> {
    currentBoard = await joinOrCreateBoard(boardName)
    if (currentBoard) {
      const { data, error } = await getBoardTodos(currentBoard.id)

      if (error) {
        boardError = error
      } else {
        todos = [...data]
      }
    }
  }

  async function handleTodoChange(todo: TodoItem): Promise<void> {
    const { error } = await updateTodo({
      ...todo
    })
    if (error) {
      boardError = error
      return
    }
    todos = [...todos.filter((t) => t.id !== todo.id), todo]
  }

  function handleClipboardCopy(text: string): void {
    navigator.clipboard.writeText(text)
  }
</script>

{#if currentBoard}
  <div class="flex">
    <div class="w-full p-4">
      <!-- Changed from w-1/3 to w-1/2 -->
      <header class="text-2xl text-left mb-4">
        Your board: <span class="font-bold">&#171;{currentBoard.name}&#187;</span>
        <div class="text-sm text-gray-500">
          Key to share board: {currentBoard.access_key}
          <button
            on:click={() => {
              handleClipboardCopy(currentBoard.access_key)
            }}
            title="Copy access key"
            class="ml-2"
          >
            📋
          </button>
        </div>
      </header>
    </div>
    {#if boardError}
      <div class="w-full p-4">
        <p class="text-red-500">{boardError}</p>
      </div>
    {/if}
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
