<script lang="ts">
  import FormLogin from '@/components/LoginForm/index.svelte'
  import Layout from '@/components/Layout/index.svelte'
  import Welcome from '@/components/Welcome/index.svelte'
  import TodoList from '@/components/TodoList/index.svelte'
  let showLogin = false

  let isAuthorised = false

  function showModal(): void {
    showLogin = true
  }

  function onLogin(): void {
    isAuthorised = true
    showLogin = false
  }
</script>

{#if isAuthorised}
  <TodoList />
{:else}
  <Layout>
    <Welcome onContinue={showModal} />
  </Layout>
{/if}

{#if showLogin}
  <div
    class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-gray-800 bg-opacity-50"
  >
    <div class="bg-white p-6 rounded shadow-md">
      <FormLogin title={'test'} {onLogin} />
    </div>
  </div>
{/if}
