<script lang="ts">
	let { inputType, value = $bindable(), placeholder = "" } = $props();
</script>

<!-- svelte-ignore event_directive_deprecated -->
<input
    class={
        "gdl-input p-3 rounded-md w-full bg-zinc-800 text-white outline-0 mt-3"
    }
    type={inputType} bind:value={value} {placeholder} />