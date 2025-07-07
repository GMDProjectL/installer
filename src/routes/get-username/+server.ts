// @ts-ignore
import type { RequestHandler } from './$types';
import { userInfo } from 'os';

export const GET: RequestHandler = async () => {
    return new Response(String(JSON.stringify({username: userInfo().username})));
};