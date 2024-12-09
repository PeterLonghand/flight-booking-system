let flight1Id = -1;
let choosedSeats = [];
let currentPrices = [];
let ecoPrice = 0;
let busPrice = 0;

document.addEventListener("DOMContentLoaded", () => {
  flight_duration();

  // Получаем параметры из строки запроса
  const urlParams = new URLSearchParams(window.location.search);

  // Извлекаем flight1Id
  flight1Id = urlParams.get("flight1Id");
  console.log("Полученный flight1Id:", flight1Id);

  // Обращаемся к серверу, чтобы получить plane_id, связанный с flight1Id
  fetch(`/get-plane-id/${flight1Id}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении plane_id");
      }
      return response.json();
    })
    .then((data) => {
      const planeId = data.plane_id; // plane_id возвращается с сервера
      console.log("Полученный planeId:", planeId);

      // Теперь получаем данные о местах самолета
      return fetch(`/get-seat-map/${planeId}/`);
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении схемы мест");
      }
      return response.json();
    })
    .then((data) => {
      // Отрисовываем схему мест
      renderSeatMap(data.planeModel, data.seats, []);
    })
    .catch((error) => {
      console.error("Произошла ошибка:", error);
    });

  fetch(`/get-eco-price/${flight1Id}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении эконом-классовой цены");
      }
      return response.json();
    })
    .then((data) => {
      ecoPrice = data.eco_seat_cost;
    })
    .catch((error) => {
      console.error(
        "Произошла ошибка при получении эконом-классовой цены:",
        error
      );
    });

  fetch(`/get-bus-price/${flight1Id}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении бизнес-классовой цены");
      }
      return response.json();
    })
    .then((data) => {
      busPrice = data.bus_seat_cost;
    })
    .catch((error) => {
      console.error(
        "Произошла ошибка при получении бизнес-классовой цены:",
        error
      );
    });
});

///
///
///
///
///
let selectedSeat = null;

function handleSeatClick(seatElement) {
  // Проверяем, не занято ли место
  if (seatElement.classList.contains("occupied")) {
    alert("Это место уже занято.");
    return;
  }

  // Сбрасываем предыдущее выделение
  document.querySelectorAll(".seat.selected").forEach((seat) => {
    seat.classList.remove("selected");
  });

  // Выделяем новое место
  seatElement.classList.add("selected");
  selectedSeat = seatElement.dataset.seatId;
}

function updateBaseFare(seat, price) {
  // Обновление информации о выбранном месте
  /* if (seat && price !== undefined) {
    labelDiv.innerText = `Место: ${seat}`;
    valueDiv.innerText = price;
  } else {
    labelDiv.innerText = "Место:";
    valueDiv.innerText = "0";
  } */
}

function updateTotalFare() {
  // Обновление общей стоимости
}

function add_traveller() {
  console.log("я в add_traveller");
  if (!selectedSeat) {
    alert("Пожалуйста, выберите место для пассажира.");
    return false;
  }

  let div = document.querySelector(".add-traveller-div");
  let fname = div.querySelector("#fname");
  let lname = div.querySelector("#lname");
  let patronymic = div.querySelector("#patronymic"); // Новое поле отчества
  let gender = div.querySelectorAll(".gender");
  let gender_val = null;

  // Проверка имени
  if (fname.value.trim().length === 0) {
    alert("Пожалуйста, введите имя");
    return false;
  }

  // Проверка фамилии
  if (lname.value.trim().length === 0) {
    alert("Пожалуйста, введите фамилию");
    return false;
  }

  // Проверка отчества
  if (patronymic.value.trim().length === 0) {
    alert("Пожалуйста, введите отчество");
    return false;
  }

  // Проверка пола
  if (!gender[0].checked) {
    if (!gender[1].checked) {
      alert("Пожалуйста, выберите пол");
      return false;
    } else {
      gender_val = gender[1].value;
    }
  } else {
    gender_val = gender[0].value;
  }

  // Проверка выбранного места
  if (!selectedSeat) {
    alert("Пожалуйста, выберите место для пассажира.");
    return false;
  }

  let passengerCount = div.parentElement.querySelectorAll(
    ".each-traveller-div .each-traveller"
  ).length;

  let currentPrice = 0;

  //console.log("Selected seat:", selectedSeat);
  //console.log("Class : ", selectedSeat.charAt(0));
  if (selectedSeat.charAt(0) == "E") {
    console.log("я в Е");
    currentPrices.push(ecoPrice);
    currentPrice = ecoPrice;
  } else {
    console.log("я в Б");
    currentPrices.push(busPrice);
    currentPrice = busPrice;
  }
  console.log("currentPrices---", currentPrices);

  choosedSeats.push(selectedSeat);

  ///
  ///

  document.getElementById("default-base-fare").style.display = "none";

  let divprice = document.getElementById("row-base-fare");

  let price_row = `<div class="row base-fare" id="pricediv${selectedSeat}"><div class="base-fae-label">Место ${selectedSeat}</div><div class="base-fare-value">₽ <span>${currentPrice}</span></div></div>`;
  divprice.innerHTML += price_row;

  let totalValueDiv = document.querySelector(".total-fare-value span");
  let totalFare = 0;
  for (let i = 0; i < currentPrices.length; i++) {
    totalFare += currentPrices[i];
  }
  totalValueDiv.innerText = totalFare;

  ///
  ///

  // Добавляем пассажира
  let traveller = `<div class="row each-traveller">
                        <div>
                            <span class="traveller-name">${fname.value} ${
    lname.value
  } ${patronymic.value}</span><span>,</span>
                            <span class="traveller-gender">${gender_val.toUpperCase()}</span><span>,</span>
                            <span class="traveller-seat">${selectedSeat}</span>
                        </div>
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }FName" value="${fname.value}">
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }LName" value="${lname.value}">
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }Patronymic" value="${patronymic.value}">
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }Gender" value="${gender_val}">
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }Seat" value="${selectedSeat}">
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }Price" value="${currentPrice}">
                        <div class="delete-traveller">
                            <button class="btn" type="button" onclick="del_traveller(this)">
                                <svg width="1.1em" height="1.1em" viewBox="0 0 16 16" class="bi bi-x-circle" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                    <path fill-rule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                    <path fill-rule="evenodd" d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                                </svg>
                            </button>
                        </div>
                    </div>`;

  div.parentElement.querySelector(".each-traveller-div").innerHTML += traveller;
  div.parentElement.querySelector("#p-count").value = passengerCount + 1;
  div.parentElement.querySelector(".traveller-head h6 span").innerText =
    passengerCount + 1;
  div.parentElement.querySelector(".no-traveller").style.display = "none";

  // Очищаем поля ввода
  fname.value = "";
  lname.value = "";
  patronymic.value = "";
  gender.forEach((radio) => {
    radio.checked = false;
  });

  // Обновление цен
  let pcount = document.querySelector("#p-count").value;
  //let fare = document.querySelector("#basefare").value;
  /* if (parseInt(pcount) !== 0) {
    document.querySelector(".base-fare-value span").innerText =
      parseInt(fare) * parseInt(pcount);
    document.querySelector(".total-fare-value span").innerText =
      parseInt(fare) * parseInt(pcount);
  } */

  selectedSeat = null;

  // обновление схемы
  // После добавления пассажира и блокировки места
  fetch(`/get-plane-id/${flight1Id}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении plane_id");
      }
      return response.json();
    })
    .then((data) => {
      const planeId = data.plane_id; // plane_id возвращается с сервера
      console.log("Полученный planeId:", planeId);

      // Теперь получаем данные о местах самолета
      return fetch(`/get-seat-map/${planeId}/`);
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении схемы мест");
      }
      return response.json();
    })
    .then((data) => {
      // Отрисовываем схему мест
      renderSeatMap(data.planeModel, data.seats, choosedSeats);
    })
    .catch((error) => {
      console.error("Произошла ошибка:", error);
    });
  //updateSeatMap();
}

///
///
///
///
///

function flight_duration() {
  document.querySelectorAll(".duration").forEach((element) => {
    let timeString = element.dataset.value.trim();
    console.log("Raw time string:", timeString); // Логируем строку

    let hours = 0;
    let minutes = 0;

    // Проверим наличие чисел для часов и минут
    const hoursMatch = timeString.match(/(\d+)\s*(hours?|hrs?)/);
    const minutesMatch = timeString.match(/(\d+)\s*(minutes?|mins?)/);

    if (hoursMatch) {
      hours = hoursMatch[1]; // Извлекаем количество часов
      console.log("Hours found:", hours); // Логируем количество часов
    } else {
      console.log("No hours match");
    }

    if (minutesMatch) {
      minutes = minutesMatch[1]; // Извлекаем количество минут
      console.log("Minutes found:", minutes); // Логируем количество минут
    } else {
      console.log("No minutes match");
    }

    // Обновляем текст в элементе с нужным форматом
    element.innerText = `${hours}ч ${minutes}мин`;
  });
}

// function add_traveller() {
//   let div = document.querySelector(".add-traveller-div");
//   let fname = div.querySelector("#fname");
//   let lname = div.querySelector("#lname");
//   let patronymic = div.querySelector("#patronymic"); // Новое поле отчества
//   let gender = div.querySelectorAll(".gender");
//   let gender_val = null;

//   // Проверка имени
//   if (fname.value.trim().length === 0) {
//     alert("Пожалуйста, введите имя");
//     return false;
//   }

//   // Проверка фамилии
//   if (lname.value.trim().length === 0) {
//     alert("Пожалуйста, введите фамилию");
//     return false;
//   }

//   // Проверка отчества
//   if (patronymic.value.trim().length === 0) {
//     alert("Пожалуйста, введите отчество");
//     return false;
//   }

//   // Проверка пола
//   if (!gender[0].checked) {
//     if (!gender[1].checked) {
//       alert("Пожалуйста, выберите пол");
//       return false;
//     } else {
//       gender_val = gender[1].value;
//     }
//   } else {
//     gender_val = gender[0].value;
//   }

//   // Проверка выбранного места
//   if (!selectedSeat) {
//     alert("Пожалуйста, выберите место для пассажира.");
//     return false;
//   }

//   let passengerCount = div.parentElement.querySelectorAll(
//     ".each-traveller-div .each-traveller"
//   ).length;

//   // Добавляем пассажира
//   let traveller = `<div class="row each-traveller">
//                         <div>
//                             <span class="traveller-name">${fname.value} ${
//     lname.value
//   } ${patronymic.value}</span><span>,</span>
//                             <span class="traveller-gender">${gender_val.toUpperCase()}</span>
//                         </div>
//                         <input type="hidden" name="passenger${
//                           passengerCount + 1
//                         }FName" value="${fname.value}">
//                         <input type="hidden" name="passenger${
//                           passengerCount + 1
//                         }LName" value="${lname.value}">
//                         <input type="hidden" name="passenger${
//                           passengerCount + 1
//                         }Patronymic" value="${patronymic.value}">
//                         <input type="hidden" name="passenger${
//                           passengerCount + 1
//                         }Gender" value="${gender_val}">
//                         <input type="hidden" name="passenger${
//                           passengerCount + 1
//                         }Seat" value="${selectedSeat}">
//                         <div class="delete-traveller">
//                             <button class="btn" type="button" onclick="del_traveller(this)">
//                                 <svg width="1.1em" height="1.1em" viewBox="0 0 16 16" class="bi bi-x-circle" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
//                                     <path fill-rule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
//                                     <path fill-rule="evenodd" d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
//                                 </svg>
//                             </button>
//                         </div>
//                     </div>`;

//   div.parentElement.querySelector(".each-traveller-div").innerHTML += traveller;
//   div.parentElement.querySelector("#p-count").value = passengerCount + 1;
//   div.parentElement.querySelector(".traveller-head h6 span").innerText =
//     passengerCount + 1;
//   div.parentElement.querySelector(".no-traveller").style.display = "none";

//   // Очищаем поля ввода
//   fname.value = "";
//   lname.value = "";
//   patronymic.value = "";
//   gender.forEach((radio) => {
//     radio.checked = false;
//   });

//   // Обновление цен
//   let pcount = document.querySelector("#p-count").value;
//   let fare = document.querySelector("#basefare").value;
//   if (parseInt(pcount) !== 0) {
//     document.querySelector(".base-fare-value span").innerText =
//       parseInt(fare) * parseInt(pcount);
//     document.querySelector(".total-fare-value span").innerText =
//       parseInt(fare) * parseInt(pcount);
//   }

//   // Устанавливаем выбранное место как занятое (красное)
//   const selectedSeatElement = document.querySelector(
//     `.seat[data-seat="${selectedSeat}"]`
//   );
//   if (selectedSeatElement) {
//     selectedSeatElement.classList.add("occupied"); // Добавляем класс "occupied" для выделения
//     selectedSeatElement.style.backgroundColor = "red"; // Можно также применить стиль напрямую
//   }
// }

/*
function add_traveller() {
  let div = document.querySelector(".add-traveller-div");
  let fname = div.querySelector("#fname");
  let lname = div.querySelector("#lname");
  let patronymic = div.querySelector("#patronymic"); // Новое поле отчества
  let gender = div.querySelectorAll(".gender");
  let gender_val = null;

  // Проверка имени
  if (fname.value.trim().length === 0) {
    alert("Пожалуйста, введите имя");
    return false;
  }

  // Проверка фамилии
  if (lname.value.trim().length === 0) {
    alert("Пожалуйста, введите фамилию");
    return false;
  }

  // Проверка отчества
  if (patronymic.value.trim().length === 0) {
    alert("Пожалуйста, введите отчество");
    return false;
  }

  // Проверка пола
  if (!gender[0].checked) {
    if (!gender[1].checked) {
      alert("Пожалуйста, выберите пол");
      return false;
    } else {
      gender_val = gender[1].value;
    }
  } else {
    gender_val = gender[0].value;
  }

  let passengerCount = div.parentElement.querySelectorAll(
    ".each-traveller-div .each-traveller"
  ).length;

  // Добавляем пассажира
  let traveller = `<div class="row each-traveller">
                        <div>
                            <span class="traveller-name">${fname.value} ${
    lname.value
  } ${patronymic.value}</span><span>,</span>
                            <span class="traveller-gender">${gender_val.toUpperCase()}</span>
                        </div>
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }FName" value="${fname.value}">
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }LName" value="${lname.value}">
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }Patronymic" value="${patronymic.value}">
                        <input type="hidden" name="passenger${
                          passengerCount + 1
                        }Gender" value="${gender_val}">
                        <div class="delete-traveller">
                            <button class="btn" type="button" onclick="del_traveller(this)">
                                <svg width="1.1em" height="1.1em" viewBox="0 0 16 16" class="bi bi-x-circle" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                    <path fill-rule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                    <path fill-rule="evenodd" d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                                </svg>
                            </button>
                        </div>
                    </div>`;
  div.parentElement.querySelector(".each-traveller-div").innerHTML += traveller;
  div.parentElement.querySelector("#p-count").value = passengerCount + 1;
  div.parentElement.querySelector(".traveller-head h6 span").innerText =
    passengerCount + 1;
  div.parentElement.querySelector(".no-traveller").style.display = "none";

  // Очищаем поля ввода
  fname.value = "";
  lname.value = "";
  patronymic.value = "";
  gender.forEach((radio) => {
    radio.checked = false;
  });

  // Обновление цен
  let pcount = document.querySelector("#p-count").value;
  let fare = document.querySelector("#basefare").value;
  if (parseInt(pcount) !== 0) {
    document.querySelector(".base-fare-value span").innerText =
      parseInt(fare) * parseInt(pcount);
    document.querySelector(".total-fare-value span").innerText =
      parseInt(fare) * parseInt(pcount);
  }
}
*/
function del_traveller(btn) {
  let traveller = btn.parentElement.parentElement;
  console.log("бип", traveller);
  let tvl = btn.parentElement.parentElement.parentElement.parentElement;
  let cnt = tvl.querySelector("#p-count");
  cnt.value = parseInt(cnt.value) - 1;
  tvl.querySelector(".traveller-head h6 span").innerText = cnt.value;
  if (parseInt(cnt.value) <= 0) {
    tvl.querySelector(".no-traveller").style.display = "block";
    document.getElementById("default-base-fare").style.display = "block";
  }
  seatCodeCode = traveller.querySelector(
    'input[name^="passenger"][name$="Seat"]'
  ).value;
  console.log("Код места:", seatCodeCode);
  traveller.remove();

  let pcount = document.querySelector("#p-count").value;
  //let fare = document.querySelector("#basefare").value;
  // let fee = document.querySelector("#fee").value;
  /* if (parseInt(pcount) !== 0) {
    document.querySelector(".base-fare-value span").innerText =
      parseInt(fare) * parseInt(pcount);
    document.querySelector(".total-fare-value span").innerText =
      parseInt(fare) * parseInt(pcount);
  } */

  // Находим индекс элемента seatValue
  let indexof = choosedSeats.indexOf(seatCodeCode);
  console.log("индексОф", indexof);

  let lastPriceDiv = document.getElementById(`pricediv${seatCodeCode}`);
  lastPriceDiv.remove();
  // Если элемент найден, удаляем его
  if (indexof > -1) {
    choosedSeats.splice(indexof, 1);
    currentPrices.splice(indexof, 1);
  }

  selectedSeat = null;
  ///
  ///
  ///
  ///
  ///
  ///
  let totalValueDiv = document.querySelector(".total-fare-value span");
  let totalFare = 0;
  for (let i = 0; i < currentPrices.length; i++) {
    totalFare += currentPrices[i];
  }
  totalValueDiv.innerText = totalFare;
  // обновление схемы
  // После добавления пассажира и блокировки места
  fetch(`/get-plane-id/${flight1Id}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении plane_id");
      }
      return response.json();
    })
    .then((data) => {
      const planeId = data.plane_id; // plane_id возвращается с сервера
      console.log("Полученный planeId:", planeId);

      // Теперь получаем данные о местах самолета
      return fetch(`/get-seat-map/${planeId}/`);
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении схемы мест");
      }
      return response.json();
    })
    .then((data) => {
      // Отрисовываем схему мест
      renderSeatMap(data.planeModel, data.seats, choosedSeats);
    })
    .catch((error) => {
      console.error("Произошла ошибка:", error);
    });
}

function book_submit() {
  let pcount = document.querySelector("#p-count");
  if (parseInt(pcount.value) > 0) {
    return true;
  }
  alert("Пожалуйста, добавьте хотя бы одного пассажира.");
  return false;
}

function updateSeatMap() {
  const travellers = document.querySelectorAll(".each-traveller");
  console.log("путешественники: ", travellers);
  const choosedSeats = Array.from(travellers).map((traveller) => {
    return traveller.querySelector(`input[name*="Seat"]`).value;
  });

  fetch(`/get-plane-id/${flight1Id}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении plane_id");
      }
      return response.json();
    })
    .then((data) => {
      const planeId = data.plane_id;

      return fetch(`/get-seat-map/${planeId}/`);
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Ошибка при получении схемы мест");
      }
      return response.json();
    })
    .then((data) => {
      // Передаем массив временно занятых мест
      renderSeatMap(data.planeModel, data.seats, choosedSeats);
    })
    .catch((error) => {
      console.error("Произошла ошибка:", error);
    });
}

// // // // /// / / / // / /
function renderSeatMap(planeModel, seats, choosedSeats) {
  const seatMap = document.getElementById("seat-map");
  seatMap.innerHTML = ""; // Очистим старую схему, если она была

  const classSection = document.createElement("div");
  classSection.className = "class-section";

  // Отрисовка мест для бизнес-класса
  if (planeModel.row_length_bus > 0) {
    const businessClassRows = renderHorizontalRows(
      "B",
      planeModel.row_length_bus,
      planeModel.rows_left_bus,
      planeModel.rows_middle_bus,
      planeModel.rows_right_bus,
      seats,
      choosedSeats
    );
    classSection.appendChild(businessClassRows);
  }

  // Проход между классами
  classSection.appendChild(createAisle());

  // Отрисовка мест для эконом-класса
  if (planeModel.row_length_eco > 0) {
    const economyClassRows = renderHorizontalRows(
      "E",
      planeModel.row_length_eco,
      planeModel.rows_left_eco,
      planeModel.rows_middle_eco,
      planeModel.rows_right_eco,
      seats,
      choosedSeats
    );
    classSection.appendChild(economyClassRows);
  }

  seatMap.appendChild(classSection);
}

function renderHorizontalRows(
  prefix,
  rowLength,
  leftColumns,
  middleColumns,
  rightColumns,
  seats,
  choosedSeats
) {
  const rowsContainer = document.createElement("div");
  rowsContainer.className = "rows-container";

  // Рисуем все ряды вдоль длины (горизонтально)
  for (let row = 0; row < rowLength; row++) {
    const rowDiv = document.createElement("div");
    rowDiv.className = "row-row ";

    // Левые места
    addSeats(
      rowDiv,
      prefix,
      row,
      leftColumns,
      "A".charCodeAt(0),
      seats,
      choosedSeats
    );

    // Проход/средние места
    if (middleColumns > 0) {
      rowDiv.appendChild(createAisle());
      addSeats(
        rowDiv,
        prefix,
        row,
        middleColumns,
        "A".charCodeAt(0) + leftColumns,
        seats,
        choosedSeats
      );
    }

    // Правые места
    rowDiv.appendChild(createAisle());
    addSeats(
      rowDiv,
      prefix,
      row,
      rightColumns,
      "A".charCodeAt(0) + leftColumns + middleColumns,
      seats,
      choosedSeats
    );

    rowsContainer.appendChild(rowDiv);
  }

  return rowsContainer;
}

function addSeats(
  rowDiv,
  prefix,
  row,
  numColumns,
  startCharCode,
  seats,
  choosedSeats
) {
  for (let col = 0; col < numColumns; col++) {
    const seatCode = `${prefix}${row}${String.fromCharCode(
      startCharCode + col
    )}`;
    const seat = seats.find((s) => s.address === seatCode);

    const seatDiv = document.createElement("div");
    seatDiv.className = "seat";
    seatDiv.textContent = seatCode;

    if (seat && !seat.available) {
      // Место занято
      seatDiv.classList.add("occupied");
    } else if (choosedSeats.includes(seatCode)) {
      // Место временно занято (выбрано другим пассажиром)
      seatDiv.classList.add("choosed");
    } else {
      // Место доступно
      seatDiv.classList.add("available");
      seatDiv.addEventListener("click", () =>
        toggleSeatSelection(seatDiv, seatCode)
      );
    }

    rowDiv.appendChild(seatDiv);
  }
}

function createAisle() {
  const aisleDiv = document.createElement("div");
  aisleDiv.className = "aisle";
  return aisleDiv;
}

function toggleSeatSelection(seatDiv, address) {
  const selectedSeats = document.querySelectorAll(".seat.selected");
  if (selectedSeats.length > 0 && selectedSeats[0] !== seatDiv) {
    selectedSeats[0].classList.remove("selected");
  }

  seatDiv.classList.toggle("selected");
  selectedSeat = seatDiv.classList.contains("selected") ? address : null;
  console.log("Selected seat:", address);
}
