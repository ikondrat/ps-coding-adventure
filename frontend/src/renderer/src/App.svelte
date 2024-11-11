<script lang="ts">
  let todos = {
    todo: [
      { id: 1, title: 'First TODO', updatedAt: new Date() },
      { id: 2, title: 'Second TODO', updatedAt: new Date() },
      { id: 3, title: 'Third TODO', updatedAt: new Date() }
    ],
    ongoing: [],
    done: []
  }

  let showModal = false // State to control modal visibility
  let newTitle = '' // Declare newTitle to hold the input value

  function openModal() {
    showModal = true // Function to open the modal
  }

  function closeModal() {
    showModal = false // Function to close the modal
  }

  function addTodo(newTitle) {
    const newTodo = { id: todos.todo.length + 1, title: newTitle, updatedAt: new Date() }
    todos.todo.push(newTodo)
    closeModal() // Close modal after adding
  }

  function handleDragStart(event, index, state) {
    event.dataTransfer.setData('text/plain', JSON.stringify({ index, state }))
  }

  function handleDrop(event, targetState) {
    const { index, state } = JSON.parse(event.dataTransfer.getData('text/plain'))
    if (state !== targetState) {
      let movedTodo
      if (state === 'todo') {
        movedTodo = todos.todo.splice(index, 1)[0]
      } else if (state === 'ongoing') {
        movedTodo = todos.ongoing.splice(index, 1)[0]
      } else if (state === 'done') {
        movedTodo = todos.done.splice(index, 1)[0]
      }
      if (targetState === 'todo') {
        todos.todo.push(movedTodo)
      } else if (targetState === 'ongoing') {
        todos.ongoing.push(movedTodo)
      } else if (targetState === 'done') {
        todos.done.push(movedTodo)
      }
    }
  }
</script>

<div class="flex">
  <div class="w-1/3 p-4">
    <h2 class="text-lg font-bold">TODO</h2>
    <button on:click={openModal} class="bg-blue-500 text-white p-2 rounded">Add TODO</button>
    {#each todos.todo as todo, index}
      <div
        class="bg-white p-4 mb-2 rounded shadow"
        draggable="true"
        on:dragstart={(event) => handleDragStart(event, index, 'todo')}
        on:drop={(event) => handleDrop(event, 'todo')}
        on:dragover={(event) => handleDrop(event, 'todo')}
        data-index={index}
      >
        <h3 class="font-semibold">{todo.title}</h3>
        <p class="text-gray-600">Last updated: {todo.updatedAt.toLocaleString()}</p>
      </div>
    {/each}
  </div>
  <div class="w-1/3 p-4">
    <h2 class="text-lg font-bold">ONGOING</h2>
    {#each todos.ongoing as todo, index}
      <div
        class="bg-white p-4 mb-2 rounded shadow"
        draggable="true"
        on:dragstart={(event) => handleDragStart(event, index, 'ongoing')}
        on:drop={(event) => handleDrop(event, 'ongoing')}
        on:dragover={(event) => event.preventDefault()}
        data-index={index}
      >
        <h3 class="font-semibold">{todo.title}</h3>
        <p class="text-gray-600">Last updated: {todo.updatedAt.toLocaleString()}</p>
      </div>
    {/each}
  </div>
  <div class="w-1/3 p-4">
    <h2 class="text-lg font-bold">DONE</h2>
    {#each todos.done as todo, index}
      <div
        class="bg-white p-4 mb-2 rounded shadow"
        draggable="true"
        on:dragstart={(event) => handleDragStart(event, index, 'done')}
        on:drop={(event) => handleDrop(event, 'done')}
        on:dragover={(event) => event.preventDefault()}
        data-index={index}
      >
        <h3 class="font-semibold">{todo.title}</h3>
        <p class="text-gray-600">Last updated: {todo.updatedAt.toLocaleString()}</p>
      </div>
    {/each}
  </div>
</div>

{#if showModal}
  <!-- Modal for adding new TODO -->
  <div class="modal">
    <div class="modal-content">
      <span class="close" on:click={closeModal}>&times;</span>
      <h2>Add New TODO</h2>
      <input type="text" bind:value={newTitle} placeholder="Enter TODO title" />
      <button on:click={() => addTodo(newTitle)}>Add</button>
    </div>
  </div>
{/if}
