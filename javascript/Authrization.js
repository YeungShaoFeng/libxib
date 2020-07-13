const CryptoJS = require('./CryptoJS');

let Auth = () => CryptoJS.AES.encrypt(Date.now() + "\b\xa7", "650219").toString();
let DeAuth = (cipher) => CryptoJS.AES.decrypt(cipher, "650219").toString();
console.log(DeAuth("U2FsdGVkX19J+8LXbY5dXxh0m6/8j6PS3c3GKLa5hQUXhDv3SaalVbaZgwq1QUCp"))