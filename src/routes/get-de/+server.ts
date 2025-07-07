// @ts-ignore
import type { RequestHandler } from './$types';


export const GET: RequestHandler = async () => {
    return new Response(String(JSON.stringify({de: process.env.XDG_CURRENT_DESKTOP?.toLowerCase()})));
};