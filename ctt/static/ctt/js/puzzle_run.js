

document.addEventListener('DOMContentLoaded', function () {
  // Función para mostrar u ocultar los campos de score según el tipo de puzzle
  function toggleScoreFields() {
    const puzzleField = document.getElementById('id_puzzle');
    const scoreFields = ['id_score_1', 'id_score_2', 'id_score_3'];

    // Oculta todos los campos de score
    scoreFields.forEach(field => {
      const scoreField = document.getElementById(field);
      if (scoreField) {
        scoreField.parentElement.style.display = 'none';
      }
    });

    // Muestra los campos de score según la lógica deseada
    if (puzzleField.value === 'Daily Challenge') {
      document.getElementById('id_score_1').parentElement.style.display = 'block';
    } else if (puzzleField.value === 'Puzzle Storm' || puzzleField.value === 'Puzzle Racer') {
      scoreFields.forEach(field => {
        const scoreField = document.getElementById(field);
        if (scoreField) {
          scoreField.parentElement.style.display = 'block';
        }
      });
    }
  }

  // Muestra u oculta los campos de score al cargar la página
  toggleScoreFields();

  // Agrega un evento de cambio al campo de puzzle para actualizar dinámicamente los campos de score
  document.getElementById('id_puzzle').addEventListener('change', toggleScoreFields);
});

document.getElementById("id_puzzle").addEventListener("change", function() {
  var durationField = document.getElementById("id_duration");
  // Si el tipo de puzzle es 'aimchess', establecer el valor predeterminado a 5
  if (this.value === 'Puzzle Storm') {
    durationField.value = 9;
  } else if (this.value === 'Puzzle Racer') {
      durationField.value = 6;
  } else if (this.value === 'Aimchess Routine') {
      durationField.value = 12;
  } else if (this.value === 'Daily Challenge') {
      durationField.value = 10;
  } else if (this.value === 'Focus Workout') {
      durationField.value = 8;
  } else {
    // Restaurar el valor predeterminado si no es 'aimchess'
    durationField.value = '';
  }
});