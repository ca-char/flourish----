function deletePlant(plantId) {
  fetch("delete-plant", {
    method: "POST",
    body: JSON.stringify({ plantId: plantId }),
  }).then((_res) => {
    window.location.href = "/manage_library";
  });
}
