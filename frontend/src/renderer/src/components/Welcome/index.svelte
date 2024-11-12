<script lang="ts">
  export let onContinue: () => void
</script>

<h2 class="text-balance text-3xl font-semibold tracking-tight text-white sm:text-4xl">
  TODO lists.
</h2>
<p class="mt-6 text-pretty text-lg/8 text-gray-300">
  You almost ready to go, lets start from the login!
</p>
<div class="mt-10 flex items-center justify-center gap-x-6 lg:justify-start">
  <a
    href="#"
    on:click={onContinue}
    class="rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
    >Login</a
  >
</div>
