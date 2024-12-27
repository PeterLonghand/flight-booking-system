document.addEventListener("DOMContentLoaded", () => {
  const editButton = document.getElementById("edit-button");
  const saveButton = document.getElementById("save-button");
  const form = document.getElementById("account-form");
  const inputs = document.querySelectorAll(".inp");
  const passwordGroups = document.querySelectorAll(".password-group");

  // Initial values for validation
  let check = {
    username: true,
    firstname: true,
    lastname: true,
    patronymic: true,
    phonenumber: true,
    email: true,
    password: true,
    confirmation: true,
  };

  // Store initial values
  const initialValues = {};
  inputs.forEach((input) => {
    if (
      !input.classList.contains("pswd") &&
      !input.classList.contains("cpswd")
    ) {
      initialValues[input.name] = input.value;
    }
  });

  editButton.addEventListener("click", () => {
    // Enable all inputs
    inputs.forEach((input) => {
      input.disabled = false;
    });

    // Show password fields
    passwordGroups.forEach((group) => {
      group.style.display = "block";
    });

    // Toggle buttons
    editButton.style.display = "none";
    saveButton.style.display = "block";
  });

  // Validation functions
  const validateInput = (input) => {
    if (input.classList.contains("username")) {
      check.username =
        /^[a-zA-Zа-яА-Я0-9_]+$/.test(input.value.trim()) &&
        input.value.trim().length >= 4 &&
        input.value.trim().length <= 36;
      showError(
        input,
        check.username,
        "Логин должен содержать 4-36 символов (латиница, кириллица, цифры и _)"
      );
    }
    if (input.classList.contains("firstname")) {
      check.firstname =
        /^[a-zA-Zа-яА-Я]+$/.test(input.value.trim()) &&
        input.value.trim().length >= 2 &&
        input.value.trim().length <= 36;
      showError(
        input,
        check.firstname,
        "Имя должно содержать 2-36 символов (латиница или кириллица)"
      );
    }
    if (input.classList.contains("lastname")) {
      check.lastname =
        /^[a-zA-Zа-яА-Я]+$/.test(input.value.trim()) &&
        input.value.trim().length >= 2 &&
        input.value.trim().length <= 36;
      showError(
        input,
        check.lastname,
        "Фамилия должна содержать 2-36 символов (латиница или кириллица)"
      );
    }
    if (input.classList.contains("patronymic")) {
      check.patronymic =
        input.value.trim().length === 0 ||
        (/^[a-zA-Zа-яА-Я]+$/.test(input.value.trim()) &&
          input.value.trim().length >= 3 &&
          input.value.trim().length <= 36);
      showError(
        input,
        check.patronymic,
        "Отчество должно содержать 3-36 символов (латиница или кириллица)"
      );
    }
    if (input.classList.contains("phonenumber")) {
      check.phonenumber =
        /^\+?\d+$/.test(input.value.trim()) &&
        input.value.trim().length >= 7 &&
        input.value.trim().length <= 18;
      showError(
        input,
        check.phonenumber,
        "Номер телефона должен содержать 7-18 цифр и может начинаться с +"
      );
    }
    if (input.classList.contains("email")) {
      check.email =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim()) &&
        input.value.trim().length >= 5 &&
        input.value.trim().length <= 64;
      showError(
        input,
        check.email,
        "Электронная почта должна содержать 5-64 символов"
      );
    }
    if (input.classList.contains("pswd")) {
      const passwordValue = input.value.trim();
      check.password =
        passwordValue.length === 0 ||
        (passwordValue.length >= 4 && passwordValue.length <= 16);
      showError(input, check.password, "Пароль должен содержать 4-16 символов");

      // Reset confirmation field
      const confirmInput = document.querySelector(".cpswd");
      confirmInput.value = "";
      check.confirmation = true;
      showError(confirmInput, true, "");
    }
    if (input.classList.contains("cpswd")) {
      const passwordInput = document.querySelector(".pswd");
      const passwordValue = passwordInput.value.trim();
      const confirmValue = input.value.trim();

      check.confirmation =
        confirmValue.length === 0 ||
        (passwordValue.length > 0 && confirmValue === passwordValue);
      showError(input, check.confirmation, "Пароли должны совпадать");
    }

    // Enable save button if all checks pass and at least one field is changed
    const isValid = Object.values(check).every((val) => val);
    const isChanged = Array.from(inputs).some((input) => {
      if (input.classList.contains("pswd")) {
        return input.value.trim().length > 0;
      }
      return input.value !== initialValues[input.name];
    });

    saveButton.disabled = !(isValid && isChanged);
  };

  const showError = (input, isValid, message) => {
    const errorMessage = input.nextElementSibling;
    if (!isValid) {
      errorMessage.style.display = "block";
      errorMessage.textContent = message;
    } else {
      errorMessage.style.display = "none";
    }
  };

  // Add input validation listeners
  inputs.forEach((input) => {
    input.addEventListener("input", () => validateInput(input));
  });
});
