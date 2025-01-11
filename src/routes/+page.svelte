<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, installInfo,
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom
    } from "$lib";
    import { goto } from "$app/navigation";
</script>


<SetupPage>
    <SetupPageTitle>
        { getString($installInfo.language, "welcome") }
        <span class="text-base mt-4 text-zinc-400 font-normal">
            { getString($installInfo.language, "welcome-description") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-between items-center flex-col px-20 w-full gap-10">
        <h2 class="text-2xl font-semibold text-center flex w-full gap-4 justify-center items-center">
            <Icon icon="material-symbols:language" width="30" height="30" />
            { getString($installInfo.language, "language-tip") }
        </h2>

        <div class="w-96 flex flex-col gap-5 h-40 overflow-y-auto p-2">
            {#each ["en", "ru"] as lang}
                <GDLButton on:click={() => {
                    $installInfo.language = lang;
                }}>
                    <span class={$installInfo.language == lang ? "font-bold" : "font-normal"}>
                        { getString(lang, "name") }
                    </span>
                </GDLButton>
            {/each}
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on:click={() => window.close()}>
            { getString($installInfo.language, "quit") }
        </GDLButton>
        <GDLButton secondary on:click={() => goto("/introduce-yourself")}>
            { getString($installInfo.language, "begin") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>