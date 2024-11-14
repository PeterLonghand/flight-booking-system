document.addEventListener("DOMContentLoaded", () => {
  let check = [false, false, false, true, false, false, false, false]; // check[3] для отчества изначально true
  const submitButton = document.querySelector('input[type="submit"]');

  document.querySelectorAll(".inp").forEach((input) => {
    input.addEventListener("input", () => {
      if (input.classList.contains("username")) {
        check[0] =
          /^[a-zA-Zа-яА-Я0-9_]+$/.test(input.value.trim()) &&
          input.value.trim().length >= 4 &&
          input.value.trim().length <= 36;
        input.nextElementSibling.innerText = check[0]
          ? ""
          : "Логин должен содержать 4-36 символов (латиница, кириллица, цифры и _)";
      }
      if (input.classList.contains("firstname")) {
        check[1] =
          /^[a-zA-Zа-яА-Я]+$/.test(input.value.trim()) &&
          input.value.trim().length >= 2 &&
          input.value.trim().length <= 36;
        input.nextElementSibling.innerText = check[1]
          ? ""
          : "Имя должно содержать 2-36 символов (латиница или кириллица)";
      }
      if (input.classList.contains("lastname")) {
        check[2] =
          /^[a-zA-Zа-яА-Я]+$/.test(input.value.trim()) &&
          input.value.trim().length >= 2 &&
          input.value.trim().length <= 36;
        input.nextElementSibling.innerText = check[2]
          ? ""
          : "Фамилия должна содержать 2-36 символов (латиница или кириллица)";
      }
      if (input.classList.contains("patronymic")) {
        check[3] =
          input.value.trim().length === 0 || // Разрешить пустое поле отчества
          (/^[a-zA-Zа-яА-Я]+$/.test(input.value.trim()) &&
            input.value.trim().length >= 3 &&
            input.value.trim().length <= 36);
        input.nextElementSibling.innerText = check[3]
          ? ""
          : "Отчество должно содержать 3-36 символов (латиница или кириллица)";
      }
      if (input.classList.contains("phonenumber")) {
        check[4] =
          /^\+?\d+$/.test(input.value.trim()) &&
          input.value.trim().length >= 7 &&
          input.value.trim().length <= 18;
        input.nextElementSibling.innerText = check[4]
          ? ""
          : "Номер телефона должен содержать 7-18 цифр и может начинаться с +";
      }
      if (input.classList.contains("email")) {
        check[5] =
          /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim()) &&
          input.value.trim().length >= 5 &&
          input.value.trim().length <= 64;
        input.nextElementSibling.innerText = check[5]
          ? ""
          : "Электронная почта должна содержать 5-64 символов";
      }
      if (input.classList.contains("pswd")) {
        check[6] =
          input.value.trim().length >= 4 && input.value.trim().length <= 16;
        input.nextElementSibling.innerText = check[6]
          ? ""
          : "Пароль должен содержать 4-16 символов";

        // Очистить предупреждение при вводе нового пароля
        document.querySelector(".cpswd").value = "";
        check[7] = false;
        document.querySelector(".cpswd").nextElementSibling.innerText = "";
      }
      if (input.classList.contains("cpswd")) {
        if (input.value.trim().length !== 0) {
          check[7] = input.value === document.querySelector(".pswd").value;
          input.nextElementSibling.innerText = check[7]
            ? ""
            : "Пароли должны совпадать";
        } else {
          check[7] = false;
        }
      }

      const isValid = check.every((field) => field);
      submitButton.disabled = !isValid;
    });
  });

  submitButton.disabled = !check.every((field) => field);
});

/* 
document.getElementById("registerForm").addEventListener("input", function () {
  const username = document.getElementById("username").value;
  const firstname = document.getElementById("firstname").value;
  const surname = document.getElementById("surname").value;
  const phonenumber = document.getElementById("phonenumber").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  // Поле отчества не обязательно
  const isValid =
    username && firstname && surname && phonenumber && email && password;

  document.getElementById("registerButton").disabled = !isValid;
});
 */
/* document.addEventListener("DOMContentLoaded", () => {
  let check = [false, false, false, false, false, false, false];
  const submitButton = document.querySelector('input[type="submit"]');

  document.querySelectorAll(".inp").forEach((input) => {
    input.addEventListener("input", () => {
      let errorMessage = input.parentElement.querySelector(".error-message");
      let isValid = false;

      
      if (input.classList.contains("username")) {
        isValid = /^[a-zA-Zа-яА-Я0-9_]{4,36}$/.test(input.value.trim());
        errorMessage.innerText =
          "Логин должен содержать от 4 до 36 символов латиницы или кириллицы, цифры и знак нижнего подчеркивания";
      }
      if (input.classList.contains("firstname")) {
        isValid = /^[a-zA-Zа-яА-Я]{2,36}$/.test(input.value.trim());
        errorMessage.innerText =
          "Имя должно содержать от 2 до 36 символов латиницы или кириллицы";
      }
      if (input.classList.contains("lastname")) {
        isValid = /^[a-zA-Zа-яА-Я]{2,36}$/.test(input.value.trim());
        errorMessage.innerText =
          "Фамилия должна содержать от 2 до 36 символов латиницы или кириллицы";
      }
      if (input.classList.contains("phonenumber")) {
        isValid = /^\+?\d{7,18}$/.test(input.value.trim());
        errorMessage.innerText =
          "Номер телефона должен содержать от 7 до 18 символов и включать цифры и знак плюса.";
      }
      if (input.classList.contains("email")) {
        isValid = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/.test(
          input.value.trim()
        );
        errorMessage.innerText = "Введите корректный адрес электронной почты.";
      }
      if (input.classList.contains("pswd")) {
        isValid =
          input.value.trim().length >= 4 && input.value.trim().length <= 16;
        errorMessage.innerText = "Пароль должен содержать от 4 до 16 символов.";
      }
      if (input.classList.contains("cpswd")) {
        isValid = input.value.trim() === document.querySelector(".pswd").value;
        errorMessage.innerText = "Пароли должны совпадать.";
      }

      
      if (!isValid) {
        errorMessage.style.display = "block";
      } else {
        errorMessage.style.display = "none";
      }

      check[Array.from(input.classList).indexOf(input.classList.value)] =
        isValid;
      const isFormValid = check.every((field) => field);
      submitButton.disabled = !isFormValid;
    });
  });

  // Инициализация состояния кнопки отправки
  submitButton.disabled = !check.every((field) => field);
}); */

/* document.addEventListener("DOMContentLoaded", () => {
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
 */
