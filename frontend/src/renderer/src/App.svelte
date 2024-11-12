<script lang="ts">
  import FormLogin from '@/components/FormLogin/index.svelte'
  import Layout from '@/components/Layout/index.svelte'
  import Welcome from '@/components/Welcome/index.svelte'
  import TodoList from '@/components/TodoList/index.svelte'
  import type { User } from './types'

  let currentUser: User | null = null

  function onLogin(authorizedUser: User): void {
    currentUser = authorizedUser
  }
</script>

<Layout>
  {#if !currentUser}
    <Welcome />
    <FormLogin {onLogin} />
  {:else}
    {#if currentUser}
      <h1>Hello, {currentUser.name}</h1>
    {/if}
    <TodoList />
  {/if}
</Layout>
