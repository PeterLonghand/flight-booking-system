document.addEventListener("DOMContentLoaded", () => {
  let check = [false, false, false, false, false, false, false];
  const submitButton = document.querySelector('input[type="submit"]');

  document.querySelectorAll(".inp").forEach((input) => {
    input.addEventListener("input", () => {
      if (input.classList.contains("username")) {
        check[0] =
          input.value.trim().length >= 4 && input.value.trim().length <= 36;
      }
      if (input.classList.contains("firstname")) {
        check[1] =
          input.value.trim().length >= 2 && input.value.trim().length <= 36;
      }
      if (input.classList.contains("lastname")) {
        check[2] =
          input.value.trim().length >= 2 && input.value.trim().length <= 36;
      }
      if (input.classList.contains("phonenumber")) {
        check[3] =
          input.value.trim().length >= 7 && input.value.trim().length <= 18;
      }
      if (input.classList.contains("email")) {
        check[4] =
          input.value.trim().length >= 5 && input.value.trim().length <= 64;
      }
      if (input.classList.contains("pswd")) {
        check[5] =
          input.value.trim().length >= 4 && input.value.trim().length <= 16;
        document.querySelector(".cpswd").value = "";
        check[6] = false; // reset confirmation validity
        document
          .querySelector(".cpswd")
          .parentElement.querySelector("span").innerText = "";
      }
      if (input.classList.contains("cpswd")) {
        if (input.value.trim().length !== 0) {
          if (input.value === document.querySelector(".pswd").value) {
            input.parentElement.querySelector("span").innerText = "";
            check[6] = true;
          } else {
            input.parentElement.querySelector("span").innerText =
              "Пароли должны совпадать";
            check[6] = false;
          }
        } else {
          check[6] = false;
        }
      }

      // Check all conditions and update button status
      const isValid = check.every((field) => field);
      submitButton.disabled = !isValid;
    });
  });

  // Initialize button disabled state at start
  submitButton.disabled = !check.every((field) => field);
});
