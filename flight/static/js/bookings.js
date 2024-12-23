function popup(element) {
  let ref = element.dataset.ref;
  document.querySelector("#cancel_ticket_btn").dataset.ref = ref;
  document.querySelector(".popup").style.display = "block";
}

function remove_popup() {
  document.querySelector(".popup").style.display = "none";
  document.querySelector("#cancel_ticket_btn").dataset.ref = "";
}

function cancel_tkt() {
  const cancelButton = document.getElementById("cancel_ticket_btn");
  const popupText = document.querySelector(
    "#small-popup div:first-child strong"
  );
  let ref = document.querySelector("#cancel_ticket_btn").dataset.ref;
  let formData = new FormData();
  formData.append("ref", ref);
  fetch("ticket/cancel", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((response) => {
      if (response.success === true) {
        remove_popup();
        document.querySelector(`[id='${ref}'] .ticket-action-div`).innerHTML =
          "";
        document.querySelector(
          `[id='${ref}'] .status-div`
        ).innerHTML = `<div class="red">CANCELLED</div>`;
        document.querySelector(`[id='${ref}'] .booking-date-div`).innerHTML =
          "";
      } else {
        // Изменяем текст в всплывающем окне
        popupText.textContent =
          "Бронирование невозможно отменить, до вылета осталось менее 6 часов";

        // Прячем кнопку "Отменить"
        cancelButton.style.display = "none";
        //alert("Бронирование успешно не отменено!");
        // Если отмена невозможна
        //remove_popup();
        //openPopup("warning-popup");
      }
    });
}
// Открыть всплывающее окно
function openPopup(popupId) {
  document.getElementById(popupId).classList.remove("hidden");
}

// Закрыть всплывающее окно
function closePopup(popupId) {
  document.getElementById(popupId).classList.add("hidden");
}

function show_warning_popup(message) {
  const warningPopup = document.createElement("div");
  warningPopup.classList.add("popup");
  warningPopup.innerHTML = `
        <div class="small-popup">
            <div style="margin-bottom: 10px; font-size: 1.1em;"><strong>${message}</strong></div>
            <div class="popup-actions">
                <button class="btn btn-light" onclick="remove_warning_popup()">Закрыть</button>
            </div>
        </div>
    `;
  document.body.appendChild(warningPopup);
}

function remove_warning_popup() {
  const warningPopup = document.querySelector(".popup");
  if (warningPopup) warningPopup.remove();
}
