<script lang="ts">
    import Icon from "@iconify/svelte";
    import { 
        getString, globalLanguage, 
        GDLButton, SetupPage, SetupPageTitle, SetupPageBottom, GDLInput,
        installInfo
    } from "$lib";
    import Swal from "sweetalert2";
    import { goto } from "$app/navigation";


    $: canGoFurther = !(
        $installInfo.username == "" ||
        $installInfo.computerName == "" ||
        $installInfo.password == "" ||
        $installInfo.password2 == "" ||
        $installInfo.password != $installInfo.password2);
        
    
</script>


<SetupPage>
    <SetupPageTitle>
        <span class="flex items-center gap-3">
            <Icon icon="ic:baseline-account-circle" width="40" height="40" />
            { getString($globalLanguage, "introduce-yourself") }
        </span>
    </SetupPageTitle>

    <div class="flex justify-between items-center flex-col px-20 w-full gap-10">
        <div class="w-96 flex flex-col gap-5 overflow-y-auto p-2">
            <div>
                <span class="flex gap-2">
                    <Icon icon="material-symbols-light:person-outline-rounded" width="24" height="24" />
                    { getString($globalLanguage, "username") }:
                </span>
                <GDLInput bind:value={$installInfo.username} inputType="text" placeholder="relative" />
            </div>
            <div>
                <span class="flex gap-2">
                    <Icon icon="mdi-light:monitor" width="24" height="24" />
                    { getString($globalLanguage, "computer-name") }:
                </span>
                <GDLInput bind:value={$installInfo.computerName} inputType="text" placeholder="relatives-pc" />
            </div>
            <div>
                <span class="flex gap-2">
                    <Icon icon="mdi:password" width="24" height="24" />
                    { getString($globalLanguage, "password") }:
                </span>
                <GDLInput bind:value={$installInfo.password} inputType="password" placeholder="••••••••••••••••" />
            </div>
            <div>
                <span class="flex gap-2">
                    <Icon icon="mdi:password" width="24" height="24" />
                    { getString($globalLanguage, "password-2") }:
                </span>
                <GDLInput bind:value={$installInfo.password2} inputType="password" placeholder="••••••••••••••••" />
            </div>
        </div>
    </div>

    <SetupPageBottom>
        <GDLButton on:click={() => history.back()}>
            { getString($globalLanguage, "back") }
        </GDLButton>
        <GDLButton secondary disabled={!canGoFurther} on:click={() => {
            if (!canGoFurther) {
                Swal.fire({
                    title: getString($globalLanguage, "introduce-error"),
                    text: getString($globalLanguage, "introduce-error-explaination"),
                    icon: 'error',
                    background: '#222',
                    color: 'white',
                    confirmButtonColor: '#333',
                    timer: 3000
                });
                return;
            }
            goto("/location");
        }}>
            { getString($globalLanguage, "next") }
        </GDLButton>
    </SetupPageBottom>
</SetupPage>