<div
  class="relative isolate overflow-hidden bg-gray-900 h-screen px-6 pt-16 shadow-2xl sm:px-16 md:pt-24 lg:flex lg:gap-x-20 lg:px-24 lg:pt-0 lg:items-center"
>
  <svg
    viewBox="0 0 1024 1024"
    class="absolute left-1/2 top-1/2 -z-10 h-[64rem] w-[64rem] -translate-y-1/2 [mask-image:radial-gradient(closest-side,white,transparent)] sm:left-full sm:-ml-80 lg:left-1/2 lg:ml-0 lg:-translate-x-1/2 lg:translate-y-0"
    aria-hidden="true"
  >
    <circle
      cx="512"
      cy="512"
      r="512"
      fill="url(#759c1415-0410-454c-8f7c-9a820de03641)"
      fill-opacity="0.7"
    />
    <defs>
      <radialGradient id="759c1415-0410-454c-8f7c-9a820de03641">
        <stop stop-color="#7775D6" />
        <stop offset="1" stop-color="#E935C1" />
      </radialGradient>
    </defs>
  </svg>
  <div class="mx-auto max-w-md text-center lg:mx-0 lg:flex-auto lg:py-32 lg:text-left">
    <slot></slot>
  </div>
</div>
