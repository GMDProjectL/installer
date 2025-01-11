<script lang="ts">
	let { children } = $props();
</script>

<h1 class="text-4xl text-center font-bold flex flex-col">
    {@render children()}
</h1>