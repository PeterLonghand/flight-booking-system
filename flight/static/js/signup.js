document.addEventListener("DOMContentLoaded", () => {
  let check = [false, false, false, false, false, false, false];
  document.querySelectorAll(".inp").forEach((input) => {
    input.addEventListener("input", () => {
      if (input.classList.contains("usrname")) {
        check[0] = input.value.trim().length !== 0;
      }
      if (input.classList.contains("fname")) {
        check[1] = input.value.trim().length !== 0;
      }
      if (input.classList.contains("lname")) {
        check[2] = input.value.trim().length !== 0;
      }
      if (input.classList.contains("phonenumber")) {
        check[3] = input.value.trim().length !== 0;
      }
      if (input.classList.contains("email")) {
        check[4] = input.value.trim().length !== 0;
      }
      if (input.classList.contains("pswd")) {
        document.querySelector(".cpswd").value = "";
        document
          .querySelector(".cpswd")
          .parentElement.querySelector("span").innerText = "";
        check[6] = false;
        check[5] = input.value.trim().length !== 0;
      }
      if (input.classList.contains("cpswd")) {
        if (input.value.trim().length !== 0) {
          if (input.value !== document.querySelector(".pswd").value) {
            input.parentElement.querySelector("span").innerText =
              "Пароли должны совпадать";
            check[6] = false;
          } else {
            input.parentElement.querySelector("span").innerText = "";
            check[6] = true;
          }
        } else {
          check[6] = false;
        }
      }

      let isValid = check.every((field) => field);
      document.querySelector('input[type="submit"]').disabled = !isValid;
    });
  });
});
