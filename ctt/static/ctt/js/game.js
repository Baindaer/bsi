document.getElementById("id_rithm").addEventListener("change", updateDuration);
document.getElementById("id_games").addEventListener("input", updateDuration);

  function updateDuration() {
    var rithmField = document.getElementById("id_rithm");
    var gamesField = document.getElementById("id_games");
    var durationField = document.getElementById("id_duration");

    // Obtén los valores de los campos
    var rithmValue = rithmField.value;
    var gamesValue = parseInt(gamesField.value);

    // Verifica si gamesValue es un número válido
    if (!isNaN(gamesValue)) {
      // Calcula la duración según las reglas proporcionadas
      var duration = 0;
      if (rithmValue === 'Blitz') {
        duration = gamesValue * 6;
      } else if (rithmValue === 'Rapid') {
        duration = gamesValue * 20;
      } else if (rithmValue === 'Bullet') {
        duration = gamesValue * 2;
      } else if (rithmValue === 'Classic') {
        duration = gamesValue * 60;
      }
      console.log(duration)
      // Actualiza el campo duration
      durationField.value = duration;
    } else {
      // Si gamesValue no es un número válido, deja el campo duration vacío
      durationField.value = "";
    }
  }