//function esc(element) {
//    document.addEventListener('keydown', event => {
//        if(event.key === 'Escape') {
//            element.style.display = 'none';
//        }
//    });
//    element.parentElement.querySelector('input[type=text]').addEventListener("blur", () => {
//        setTimeout(() => {
//            element.style.display = 'none';
//        },80);
//    });
//}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#flight-from").addEventListener("input", (event) => {
    flight_from(event);
  });

  document.querySelector("#flight-to").addEventListener("input", (event) => {
    flight_to(event);
  });

  document.querySelector("#flight-from").addEventListener("focus", (event) => {
    flight_from(event, true);
  });

  document.querySelector("#flight-to").addEventListener("focus", (event) => {
    flight_to(event, true);
  });

  document.querySelectorAll(".trip-type").forEach((type) => {
    type.onclick = trip_type;
  });
});

function showplaces(input) {
  const box = input.parentElement.querySelector(".places_box");
  if (box) {
    box.style.display = "block";
  }
}

function hideplaces(input) {
  let box = input.parentElement.querySelector(".places_box");
  setTimeout(() => {
    box.style.display = "none";
  }, 300);
}

function selectplace(option) {
  let input =
    option.parentElement.parentElement.querySelector("input[type=text]");
  input.value = option.dataset.value.toUpperCase();
  input.dataset.value = option.dataset.value;
}

function fetchPlaces(query, listSelector) {
  const list = document.querySelector(listSelector);
  const endpoint = query.length === 0 ? "all" : query;

  fetch("/query/places/" + endpoint)
    .then((response) => response.json())
    .then((places) => {
      list.innerHTML = "";
      places.forEach((element) => {
        let div = document.createElement("div");
        div.classList.add("places__list");
        div.setAttribute("onclick", "selectplace(this)");
        div.setAttribute("data-value", element.code);
        div.innerText = `${element.city} (${element.code})`;
        list.append(div);
      });
    })
    .catch((error) => console.error("Ошибка загрузки данных:", error));
}

function flight_from(event, focus = false) {
  let input = event.target;
  showplaces(input);
  if (!focus) {
    input.dataset.value = "";
  }
  fetchPlaces(input.value, "#places_from");
}

function flight_to(event, focus = false) {
  let input = event.target;
  showplaces(input);
  if (!focus) {
    input.dataset.value = "";
  }
  fetchPlaces(input.value, "#places_to");
}

////////////////////////////////////////////////////
/* 
function flight_to(event, focus = false) {
  let input = event.target;
  let list = document.querySelector("#places_to");
  showplaces(input);
  if (!focus) {
    input.dataset.value = "";
  }
  if (input.value.length > 0) {
    fetch("query/places/" + input.value)
      .then((response) => response.json())
      .then((places) => {
        list.innerHTML = "";
        places.forEach((element) => {
          let div = document.createElement("div");
          div.setAttribute("class", "each_places_to_list");
          div.classList.add("places__list");
          div.setAttribute("onclick", "selectplace(this)");
          div.setAttribute("data-value", element.code);
          div.innerText = `${element.city} (${element.code})`;
          list.append(div);
        });
      });
  }
}

function flight_from(event, focus = false) {
  let input = event.target;
  let list = document.querySelector("#places_from");
  showplaces(input);
  if (!focus) {
    input.dataset.value = "";
  }

  let query = input.value;
  if (query.length === 0) {
    query = "all"; // Если поле пустое, отправляем запрос для всех городов
  }

  fetch("/query/places/" + query)
    .then((response) => response.json())
    .then((places) => {
      list.innerHTML = "";
      places.forEach((element) => {
        let div = document.createElement("div");
        div.setAttribute("class", "each_places_from_list");
        div.classList.add("places__list");
        div.setAttribute("onclick", "selectplace(this)");
        div.setAttribute("data-value", element.code);
        div.innerText = `${element.city} (${element.code})`;
        list.append(div);
      });
    })
    .catch((error) => {
      console.error("Ошибка загрузки данных:", error);
    });
}
 */

///////////////////////////////////////////////////////////////////
/* function flight_from(event, focus = false) {
  let input = event.target;
  let list = document.querySelector("#places_from");
  showplaces(input);

  // Добавим проверку для отправки запроса при фокусе или вводе текста
  if (focus || input.value.length > 0) {
    fetch("/query/places/" + (focus ? "" : input.value)) // Пустой запрос при фокусе
      .then((response) => response.json())
      .then((places) => {
        list.innerHTML = "";
        places.forEach((element) => {
          let div = document.createElement("div");
          div.className = "each_places_from_list places__list";
          div.setAttribute("onclick", "selectplace(this)");
          div.setAttribute("data-value", element.code);
          div.innerText = `${element.city} (${element.code})`;
          list.append(div);
        });
      })
      .catch((error) => console.error("Ошибка загрузки данных:", error));
  }
}
 */
function trip_type() {
  document.querySelectorAll(".trip-type").forEach((type) => {
    if (type.checked) {
      if (type.value === "1") {
        document.querySelector("#return_date").value = "";
        document.querySelector("#return_date").disabled = true;
      } else if (type.value === "2") {
        document.querySelector("#return_date").disabled = false;
      }
    }
  });
}

function flight_search() {
  if (!document.querySelector("#flight-from").dataset.value) {
    alert("Please select flight origin.");
    return false;
  }
  if (!document.querySelector("#flight-to").dataset.value) {
    alert("Please select flight destination.");
    return false;
  }
  if (document.querySelector("#one-way").checked) {
    if (!document.querySelector("#depart_date").value) {
      alert("Please select departure date.");
      return false;
    }
  }
  if (document.querySelector("#round-trip").checked) {
    if (!document.querySelector("#depart_date").value) {
      alert("Please select departure date.");
      return false;
    }
    if (!document.querySelector("#return_date").value) {
      alert("Please select return date.");
      return false;
    }
  }
}
