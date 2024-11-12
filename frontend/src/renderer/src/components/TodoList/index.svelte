<script lang="ts">
  import Todo from '@/components/Todo/index.svelte'
  let todos = {
    todo: [
      { id: 1, title: 'First TODO', updatedAt: new Date() },
      { id: 2, title: 'Second TODO', updatedAt: new Date() },
      { id: 3, title: 'Third TODO', updatedAt: new Date() }
    ],
    ongoing: [],
    done: []
  }

  function addTodo() {
    alert('add todo')
  }
</script>

<header class="text-2xl font-bold mb-4">TODO List:</header>

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
