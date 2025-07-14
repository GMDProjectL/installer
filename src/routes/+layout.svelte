<script lang="ts">
	import '../app.css';

	import { onNavigate } from '$app/navigation';
    import GdlGlow from '$lib/components/bg-glow/GDLGlow.svelte';

	import { installationPage, getInstallationProgress, installProgress } from '$lib';
    import { onMount } from 'svelte';
	
	let { children } = $props();

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});

	onMount(() => {
		const timeout = setInterval(async() => {
			const instprog = await getInstallationProgress();

			if (instprog.progress > 0) {
				$installProgress.progress = instprog.progress;
				$installProgress.total = instprog.total;
			}

		}, 1000);

		return () => {
			clearInterval(timeout);
		}
	});

</script>

<div class="h-screen text-gray-300 p-10">
	{@render children()}
</div>

<div class="fixed pointer-events-none bottom-2 w-full scale-150 text-white">
	<div class="flex justify-center no-select">
		{#if $installProgress.progress > 0 }
			<b class="scale-50">{Math.min(Math.round($installProgress.progress / $installProgress.total * 100), 100)}%</b>
		{:else}
			{#each Array(8) as _, i}
				<i class={
					i != $installationPage
					? "opacity-50"
					: "opacity-100"
				}>•</i>
			{/each}
		{/if}
	</div>
</div>

<GdlGlow />