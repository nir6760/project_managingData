
export const pages = ['Home', 'New Poll', 'Polls Results', 'Add Admin', 'FAQ', 'About'];
export const pagesUnAuth = ['Sign In'];
export const base64 = require('base-64');
export const utf8 = require('utf8');
export const wrap64ForSend = (str:string) => {
    const ready_str = base64.encode(utf8.encode(str));
    return ready_str;
}
export const extract64ForRecive = (str:string) => {
    const ready_str = base64.decode(utf8.decode(str));
    return ready_str;
}
