document.addEventListener("DOMContentLoaded", function () {
    const chk = document.getElementById("chk");
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");
    const emailInputRegister = document.getElementById("email");
    const usernameInput = document.getElementById("username");
    const passwordInputRegister = document.getElementById("password");
    const emailInputLogin = document.getElementById("loginEmail");
    const passwordInputLogin = document.getElementById("loginPassword");

    // Schimbă între Login și Register
    chk.addEventListener("change", function () {
        if (chk.checked) {
            history.pushState(null, "", "/login");
        } else {
            history.pushState(null, "", "/register");
        }
    });

    // Funcție pentru trimiterea datelor către backend
    async function handleAuth(event, isLogin) {
        event.preventDefault();

        const email = isLogin ? emailInputLogin.value.trim() : emailInputRegister.value.trim();
        const password = isLogin ? passwordInputLogin.value.trim() : passwordInputRegister.value.trim();
        const username = isLogin ? null : usernameInput.value.trim();

        if (!email || !password || (!isLogin && !username)) {
            alert("Toate câmpurile sunt obligatorii!");
            return;
        }

        const endpoint = isLogin ? "/login" : "/register";
        const data = isLogin ? { email, password } : { username, email, password };

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message || "Eroare necunoscută!");
            }

            if (isLogin) {
                localStorage.setItem("token", result.access_token);
                alert("Autentificare reușită!");
                setTimeout(() => window.location.href = "/", 1000);
            } else {
                alert("Înregistrare reușită! Acum te poți autentifica.");
                chk.checked = true;
                history.pushState(null, "", "/login");
            }
        } catch (error) {
            alert(error.message);
        }
    }

    registerForm.addEventListener("submit", (event) => handleAuth(event, false));
    loginForm.addEventListener("submit", (event) => handleAuth(event, true));
});
