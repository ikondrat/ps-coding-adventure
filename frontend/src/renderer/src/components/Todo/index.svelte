<script lang="ts">
  import type { TodoItem } from '../../types'

  export let title: string
  export let updated_at: string
  export let state: TodoItem['state']

  export let onStatusChange: (newStatus: string) => void
  let status: string = state

  function handleStatusChange(event: Event) {
    const newStatus = (event.target as HTMLSelectElement).value
    status = newStatus
    alert('status updated')
    onStatusChange(newStatus)
  }
</script>

<div class="bg-white p-4 mb-2 rounded shadow">
  <h3 class="font-semibold mb-4">{title}</h3>
  <p class="text-gray-600">Last updated: {updated_at}</p>

  <select bind:value={status} class="mt-2" on:change={handleStatusChange}>
    <option value="TODO">TODO</option>
    <option value="Ongoing">Ongoing</option>
    <option value="Done">Done</option>
  </select>
</div>
