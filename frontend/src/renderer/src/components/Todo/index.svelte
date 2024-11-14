<script lang="ts">
  import { format } from 'date-fns'
  import { isValidTransition } from '@/utils'
  import type { TodoItem, TodoState } from '../../types'

  export let todo: TodoItem
  export let onChange: (todo: TodoItem) => void

  let todoError = ''
  let state_details = ''
  const updatedAt = format(new Date(todo.updated_at), 'PPpp')

  function handleStatusChange(event: Event): void {
    const prevState = todo.state
    const newState = (event.target as HTMLSelectElement).value as TodoState

    if (isValidTransition(prevState, newState)) {
      if (newState === 'DONE') {
        state_details = window.prompt('Enter details for the completed task')
      }
      todoError = ''
      onChange({
        ...todo,
        state: newState,
        state_details,
        updated_at: new Date().toISOString() // update timestamp
      })
    } else {
      todoError = 'Invalid transition'
    }
  }
</script>

<div class="bg-white p-4 mb-2 rounded shadow">
  <h3 class="font-semibold mb-4">{todo.title}</h3>
  {#if todoError}
    <p class="text-red-500">{todoError}</p>
  {/if}
  <p class="text-gray-600">updated: {updatedAt}</p>

  <select class="mt-2" on:change={handleStatusChange}>
    <option value="TODO" selected={todo.state === 'TODO'}>TODO</option>
    <option value="ONGOING" selected={todo.state === 'ONGOING'}>Ongoing</option>
    <option value="DONE" selected={todo.state === 'DONE'}>Done</option>
  </select>

  {#if todo.state_details}
    <p class="text-gray-600">State details: {todo.state_details}</p>
  {/if}
</div>
