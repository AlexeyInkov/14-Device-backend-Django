export const DEBUG = import.meta.env.VITE_DEBUG==="true" || false;
export const BASENAME = ''; // не добавляйте '/' в конце BASENAME
export const BASE_TITLE = import.meta.env.VITE_VITE_BASE_TITLE;
export const IP_SERVER = import.meta.env.VITE_IP_SERVER;
export const BASE_URL = import.meta.env.VITE_BASE_URL;
export const API_SERVER = (import.meta.env.PROD ? '/api' : 'http://127.0.0.1:8000');
export const URL_MENU = import.meta.env.VITE_URL_MENU;
export const URL_ADDRESSES = import.meta.env.VITE_URL_ADDRESSES;
export const URL_DEVICES = import.meta.env.VITE_URL_DEVICES;
export const HEADERS_ADDRESS = {
    'id': '№ п/п',
    'customer': 'Абонент',
    'address': 'Адрес',
    'itp': 'ИТП',
    'tso': 'Теплоснабжающая организация',
    'service_organization': 'Обслуживающая организация'
}
export const HEADERS_DEVICE = {
    'id': '№ п/п',
    'installation_point': 'Место установки',
    'type_of_file': 'Тип',
    'factory_number': 'Зав. №'
}
export const HEADERS_VERIFICATION = {
    "id": '№ п/п',
    "organization": "Поверитель",
    "verification_date": "Дата поверки",
    "valid_date": "Поверка до",
    "is_actual": "Актуальна",
    "is_delete": "Будет удалена"
}