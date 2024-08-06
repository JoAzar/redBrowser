function showSearchForm(formId) {
    // Oculta todos los formularios de búsqueda
    document.querySelectorAll('.search-form').forEach(form => form.style.display = 'none');
    
    // Muestra el formulario seleccionado
    document.getElementById(formId).style.display = 'block';
}

document.getElementById('search-button').addEventListener('click', function() {
    var query = document.getElementById('search-input').value;
    if (query) {
        window.location.href = 'https://duckduckgo.com/?q=' + encodeURIComponent(query);
    }
});

document.getElementById('search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        var query = document.getElementById('search-input').value;
        if (query) {
            window.location.href = 'https://duckduckgo.com/?q=' + encodeURIComponent(query);
        }
    }
});
document.getElementById('search-button2').addEventListener('click', function() {
    var query = document.getElementById('search-input2').value;
    if (query) {
        window.location.href = 'https://google.com/search?q=' + encodeURIComponent(query);

    }
});

document.getElementById('search-input2').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        var query = document.getElementById('search-input2').value;
        if (query) {
            window.location.href = 'https://google.com/search?q=' + encodeURIComponent(query);
        }
    }
});

document.getElementById('search-button3').addEventListener('click', function() {
    var query = document.getElementById('search-input3').value;
    if (query) {
        window.location.href = 'https://www.bing.com/?q=' + encodeURIComponent(query);
    }
});

document.getElementById('search-input3').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        var query = document.getElementById('search-input3').value;
        if (query) {
            window.location.href = 'https://www.bing.com/?q=' + encodeURIComponent(query);
        }
    }
});

// Función para mostrar el formulario de búsqueda seleccionado
function showSearchForm(formId) {
    // Oculta todos los formularios de búsqueda
    var forms = document.querySelectorAll('.search-form');
    forms.forEach(function(form) {
        form.style.display = 'none';
    });

    // Muestra el formulario de búsqueda seleccionado
    var selectedForm = document.getElementById(formId);
    selectedForm.style.display = 'block';
}

// Mostrar el primer formulario por defecto (opcional)
document.addEventListener('DOMContentLoaded', function() {
    showSearchForm('search-form'); // Muestra DuckDuckGo por defecto
});