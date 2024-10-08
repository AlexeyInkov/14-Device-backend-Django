import {API_SERVER, URL_DEVICES} from "../config/constant.js";

export async function fetchDevices(state) {
    const {meteringUnitId} = state;

    let queries = meteringUnitId !== null ? `?metering_unit=${meteringUnitId}` : ""

    if (meteringUnitId === null ) return [{}]

    const res = await fetch(`${API_SERVER}${URL_DEVICES}${queries}`)

    if (!res.ok) throw new Error('Failed to fetch addresses!')

    return res.json()
}