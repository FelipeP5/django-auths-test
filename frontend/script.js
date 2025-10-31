// Cookies não salvam no navegador, mas o postman retorna direito

'use strict'

const url = "http://127.0.0.1:8000/";
const btn = document.querySelector("#restrito");
const loginBtn = document.querySelector("#login");
const body = {
    username: "usuario5",
    password: "12345",
    email: "usuario5@mail.com"
}
const loginInfo = {
    username: "pesoa",
    password: "12345",
    email: "kaputco@enterprise.com"
}

btn.addEventListener("click", pegar);
loginBtn.addEventListener("click", logar);

async function pegar() {
    const accessToken = await cookieStore.get("access_token"); 
    const promise = await fetch(`${url}user/`, {
        headers: {
            "Content-Type":"application/json",
            "Authorization":`Bearer ${accessToken}`,
        },
        method: "get",
        // body: JSON.stringify(body)
    });
    const info = await promise.json()
    console.log(info);
}

async function logar() {
    const enviar = await fetch(`${url}login/`, {
        headers: {
            "Content-Type":"application/json",
        },
        method: "post",
        body: JSON.stringify(loginInfo),
    })
    .then(res => res.json())
    .catch(e => console.error(e));
    let token = await setTimeout(CookieStore.get("access_token"), 1000);
    console.log(token);
}