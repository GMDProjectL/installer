<script lang="ts">
	import '../app.css';
	let { children } = $props();

	import { onNavigate } from '$app/navigation';
    import GdlGlow from '$lib/components/bg-glow/GDLGlow.svelte';

	import { installationPage } from '$lib';

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});

</script>

<div class="h-screen text-gray-300 p-10">
	{@render children()}
</div>

<div class="fixed pointer-events-none bottom-2 w-full scale-150 text-white">
	<div class="flex justify-center">
		{#each Array(7) as _, i}
			<i class={
				i != $installationPage
				? "opacity-50"
				: "opacity-100"
			}>•</i>
		{/each}
	</div>
</div>

<GdlGlow />