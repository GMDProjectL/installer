import type { PageServerLoad } from './$types';

export const load = (async ({url}) => {
    console.log((url.searchParams.get("update") ?? false) ? 'Update page' : 'Install page');
    return {
        isUpdate: url.searchParams.get("update") ?? false
    };
}) satisfies PageServerLoad;