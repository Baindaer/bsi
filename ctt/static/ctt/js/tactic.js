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