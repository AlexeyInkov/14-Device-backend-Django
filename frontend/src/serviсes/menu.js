import {API_SERVER, URL_MENU} from "../config/constant.js";

export async function fetchMenu() {

    const res = await fetch(`${API_SERVER}${URL_MENU}`)

    if (!res.ok) throw new Error('Failed to fetch menu!')

    return res.json()
}