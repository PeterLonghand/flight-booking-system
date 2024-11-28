document.addEventListener("DOMContentLoaded", () => {
  // Получаем параметры из строки запроса
  const urlParams = new URLSearchParams(window.location.search);

  // Извлекаем flight1Id
  const flight1Id = urlParams.get("flight1Id");
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
      renderSeatMap(data.planeModel, data.seats);
    })
    .catch((error) => {
      console.error("Произошла ошибка:", error);
    });
});
