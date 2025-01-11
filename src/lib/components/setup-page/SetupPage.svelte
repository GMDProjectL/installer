<script lang="ts">
	let { children } = $props();
</script>

<div class="w-full h-full flex flex-col justify-between items-center">
    {@render children()}
</div>