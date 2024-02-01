
// JavaScript para establecer y obtener la última fecha registrada desde localStorage
document.addEventListener('DOMContentLoaded', function () {
    var lastDate = localStorage.getItem('lastDate');
    if (lastDate) {
    document.getElementById('id_date').value = lastDate;
    }
});

document.getElementById('id_date').addEventListener('change', function () {
    localStorage.setItem('lastDate', this.value);
});
