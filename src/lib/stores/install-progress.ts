import { writable } from "svelte/store";

type InstallationProgress = {
    progress: number,
    total: number
}

let installProgress = writable<InstallationProgress>({
    progress: 0,
    total: 33
});

export default installProgress;
export type { InstallationProgress };