
document.addEventListener('DOMContentLoaded', function () {


    const addAttemptForm = document.getElementById('addAttemptForm');

    addAttemptForm.addEventListener('submit', function (event) {
        event.preventDefault();

        // Obtener los datos del formulario
        const formData = new FormData(this);

        // Realizar una solicitud AJAX para enviar los datos
        fetch('/training/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de tener la función getCookie definida
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Si la operación fue exitosa, puedes realizar acciones adicionales si es necesario
                    console.log('Intento agregado con éxito');
                    // Cerrar el modal
                    const modal = new bootstrap.Modal(document.getElementById('addAttemptModal'));
                    modal.hide();
                    // Recargar la página o realizar acciones adicionales
                    location.reload();
                } else {
                    // Manejar errores si es necesario
                    console.error('Error al agregar el intento');
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
            });
    });

    // Función para obtener el valor de la cookie CSRF
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }


    const deleteButtons = document.querySelectorAll('.delete-training');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const trainingId = this.getAttribute('data-id');
            const confirmDelete = confirm('Are you sure you want to delete this workout?');

            if (confirmDelete) {
                // Obtener el tipo de entrenamiento
                const trainingType = this.closest('li').classList[2]; // Clase que indica el tipo

                // Enviar solicitud de eliminación a través de AJAX
                fetch(`/delete_training/?id=${trainingId}&type=${trainingType}`, {
                    method: 'DELETE', // o 'POST' según la configuración de tu backend
                })
                    .then(response => response.json())
                    .then(data => {
                        // Manejar la respuesta del servidor
                        if (data.success) {
                            // Actualizar la interfaz de usuario sin recargar la página
                            const listItem = this.closest('li');
                            listItem.remove(); // o implementa la lógica que desees para actualizar la interfaz
                        } else {
                            alert('Failed to delete workout.');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
        });
    });


    var addAttemptModal = new bootstrap.Modal(document.getElementById('addAttemptModal'));

    // Manejar el evento show.bs.modal
    addAttemptModal._element.addEventListener('show.bs.modal', function (event) {
        var triggerButton = event.relatedTarget;
        var tacticId = triggerButton.getAttribute('data-id');

        // Establecer el valor del campo "Tactic" en el formulario
        var tacticField = document.getElementById('id_tactic');
        tacticField.value = tacticId;
    });

    addAttemptModal._element.addEventListener('shown.bs.modal', function () {
        const scoreInput = document.getElementById('id_score');  // Ajusta el ID según tu formulario
        scoreInput.focus();
    });


});


function toggleDeleteButton(element) {
    const deleteButton = element.querySelector('.delete-training');
    const tacticBtn = element.querySelector('.tactic-btn');
    const addButton = element.querySelector('.add-attempt');
    deleteButton.style.display = (deleteButton.style.display === 'none' || deleteButton.style.display === '') ? 'block' : 'none';
    tacticBtn.style.display = (tacticBtn.style.display === 'none' || tacticBtn.style.display === '') ? 'flex' : 'none';
    if (addButton) {
        addButton.style.display = (addButton.style.display === 'none' || addButton.style.display === '') ? 'block' : 'none';

    }
}
