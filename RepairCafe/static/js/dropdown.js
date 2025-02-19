document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.dropdown-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const ticketForm = e.target.closest('.ticket-form');
            const dropdownContent = ticketForm.querySelector('.dropdown-content');
            const icon = button.querySelector('svg');
            
            button.classList.toggle('open');
            
            dropdownContent.classList.toggle('active');
            
            if (dropdownContent.classList.contains('active')) {
                dropdownContent.style.maxHeight = dropdownContent.scrollHeight + 'px';
            } else {
                dropdownContent.style.maxHeight = '0';
            }
        });
    });

});