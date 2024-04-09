
document.addEventListener('DOMContentLoaded', function () {
  // Función para mostrar u ocultar los campos de score según el tipo de puzzle
  function toggleScoreFields() {
    const trainingSetField = document.getElementById('id_training_set');
    const scoreFields = ['id_score', 'id_exercises', 'id_performance'];

    // Oculta todos los campos de score
    scoreFields.forEach(field => {
      const scoreField = document.getElementById(field);
      if (scoreField) {
        scoreField.parentElement.style.display = 'none';
      }
    });

    // Muestra los campos de score según la lógica deseada
    var allowedOptions = ['Standard', 'Endgame', 'Woodpecker'];
    if (trainingSetField.value === 'Daily Challenge') {
      document.getElementById('id_score').parentElement.style.display = 'block';
    } else if (allowedOptions.includes(trainingSetField.value)) {
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
  document.getElementById('id_training_set').addEventListener('change', toggleScoreFields);
});


document.getElementById("id_exercises").addEventListener("input", function() {
    // Obtén el valor del campo de ejercicios
    var exercisesValue = parseFloat(this.value);

    // Verifica si el valor es un número válido
    if (!isNaN(exercisesValue)) {
      // Calcula la duración multiplicando por 2
      var durationField = document.getElementById("id_duration");
      durationField.value = exercisesValue * 2;
    } else {
      // Si el valor no es un número válido, deja el campo de duración vacío
      document.getElementById("id_duration").value = "";
    }
  });

  document.getElementById("id_training_set").addEventListener("change", function() {
    var durationField = document.getElementById("id_duration");
    if (this.value === 'Puzzle Storm') {
      durationField.value = 4;
    } else if (this.value === 'Puzzle Racer') {
        durationField.value = 2;
    } else if (this.value === 'Aimchess Routine') {
        durationField.value = 12;
    } else if (this.value === 'Daily Challenge') {
        durationField.value = 10;
    } else if (this.value === 'Focus Workout') {
        durationField.value = 8;
    } else {
      durationField.value = 2;
    }
  });