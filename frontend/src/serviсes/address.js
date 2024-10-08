import {API_SERVER, URL_ADDRESSES} from "../config/constant.js";

export async function fetchAddresses(state) {
    const {tsoId, customerId} = state;

    let queries = tsoId !== null ? customerId !== null ? `?tso=${tsoId}&customer=${customerId}` : `?tso=${tsoId}` : ''

    const res = await fetch(`${API_SERVER}${URL_ADDRESSES}${queries}`)

    if (!res.ok) throw new Error('Failed to fetch addresses!')

    return res.json()
}