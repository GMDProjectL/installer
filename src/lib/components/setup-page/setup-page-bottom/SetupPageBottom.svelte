<script lang="ts">
	let { children } = $props();
</script>

<div class="w-full justify-end flex">
    <div class="w-full font-medium flex justify-between gap-5">
        {@render children()}
    </div>
</div>
