<script lang="ts">
	let { children, secondary = false, disabled = false, on_click } = $props();
</script>

<!-- svelte-ignore event_directive_deprecated -->
<!-- svelte-ignore a11y_invalid_attribute -->
<button class={
    "gdl-btn p-3 rounded-md w-full"
    + " text-center active:translate-y-1 transition-all flex justify-center items-center outline-0" 
    + (secondary && !disabled
        ? " bg-white hover:bg-zinc-100 active:bg-zinc-400 text-black opacity-80" 
        : " bg-zinc-800 hover:bg-zinc-700 active:bg-zinc-800")
    + (disabled ? " text-zinc-600" : "")
    }
    on:click|preventDefault={
        () => {
            on_click();
        }
    }>
        {@render children()}
</button>

<style>
    .gdl-btn {
        @apply select-none;
        transition-duration: 400ms;
    }
</style>