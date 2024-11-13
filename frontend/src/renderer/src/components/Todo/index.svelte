<script lang="ts">
  import type { TodoItem, TodoItemState } from '../../types'

  export let todo: TodoItem

  export let onChange: (todo: TodoItem) => void

  function handleStatusChange(event: Event): void {
    onChange({
      ...todo,
      state: (event.target as HTMLSelectElement).value as TodoItemState
    })
  }
</script>

<div class="bg-white p-4 mb-2 rounded shadow">
  <h3 class="font-semibold mb-4">{todo.title}</h3>
  <p class="text-gray-600">Last updated: {todo.updated_at}</p>

  <select bind:value={todo.state} class="mt-2" on:change={handleStatusChange}>
    <option value="TODO">TODO</option>
    <option value="ONGOING">Ongoing</option>
    <option value="DONE">Done</option>
  </select>
</div>
