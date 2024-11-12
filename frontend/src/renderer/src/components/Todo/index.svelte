<script lang="ts">
  export let title: string
  export let updatedAt: string
  export let onStatusChange: (newStatus: string) => void
  let status: string = 'TODO'

  function handleStatusChange(event: Event) {
    const newStatus = (event.target as HTMLSelectElement).value
    status = newStatus
    alert('status updated')
    onStatusChange(newStatus)
  }
</script>

<div class="bg-white p-4 mb-2 rounded shadow">
  <h3 class="font-semibold">{title}</h3>
  <p class="text-gray-600">Last updated: {updatedAt}</p>

  <select bind:value={status} class="mt-2" on:change={handleStatusChange}>
    <option value="TODO">TODO</option>
    <option value="Ongoing">Ongoing</option>
    <option value="Done">Done</option>
  </select>
</div>
