document.addEventListener("DOMContentLoaded", function() {
    const toggleButtons = document.querySelectorAll('.checkbox');
    
    toggleButtons.forEach(function(button) {
        button.addEventListener('change', function() {
            const checkbox = button;
            if (checkbox.checked) {
                checkbox.value = 'yes';  // Set to 'yes' when checked
            } else {
                checkbox.value = 'no';  // Set to 'no' when unchecked
            }
        });
    });
});