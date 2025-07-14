<script lang="ts">
	let { children } = $props();
</script>

<h1 class="text-4xl text-center font-bold flex flex-col no-select">
    {@render children()}
</h1>