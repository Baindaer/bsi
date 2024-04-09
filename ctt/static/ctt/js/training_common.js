
document.addEventListener('DOMContentLoaded', function () {
    var lastDate = localStorage.getItem('lastDate');
    if (lastDate) {
    document.getElementById('id_date').value = lastDate;
    }
    const deleteButtons = document.querySelectorAll('.delete-training');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const trainingId = this.getAttribute('data-id');
            const confirmDelete = confirm('Are you sure you want to delete this workout?');

            if (confirmDelete) {
                // Obtener el tipo de entrenamiento
                console.log(this.closest('li').classList)
                const trainingType = this.closest('li').classList[2]; // Clase que indica el tipo

                // Redirigir a la vista de eliminación con el ID y el tipo
                window.location.href = `/delete_training/?id=${trainingId}&type=${trainingType}`;
            }
        });
    });
});


document.getElementById('id_date').addEventListener('change', function () {
    localStorage.setItem('lastDate', this.value);
});


function toggleDeleteButton(element) {
    const deleteButton = element.querySelector('.delete-training');
    deleteButton.style.display = (deleteButton.style.display === 'none' || deleteButton.style.display === '') ? 'block' : 'none';
}