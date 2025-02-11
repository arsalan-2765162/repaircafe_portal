document.addEventListener("DOMContentLoaded", function () {
    // Add event listeners to each li element to simulate radio button click
    const listItems = document.querySelectorAll('.inc-form li');
    listItems.forEach(function(item) {
        item.addEventListener('click', function() {
            // Find the radio input inside the clicked li and check it
            const radioInput = item.querySelector('input[type="radio"]');
            if (radioInput) {
                radioInput.checked = true;
                // Optionally, you can trigger the change event if necessary
                radioInput.dispatchEvent(new Event('change'));
            }
        });
    });

    const modal = document.getElementById("confirmationModal");
    const modalIncomplete = document.getElementById("incompleteModal");
    const modalDetails = document.getElementById("modal-item-details");
    const acceptForm = modal.querySelector("form");

    // Function to open the modal
    window.openModal = function (url, itemName, itemCategory, repairNumber) {
        modalDetails.innerHTML = `
            <strong>Repair #:</strong> ${repairNumber}<br>
            <strong>Item Name:</strong> ${itemName}<br>
            <strong>Category:</strong> ${itemCategory}
        `;
        acceptForm.setAttribute("action", url);
        modal.style.display = "flex";
    };

    window.openIncompleteModal = function (url, itemName, itemCategory, repairNumber) {
        modalDetails.innerHTML = `
            <strong>Repairrrr #:</strong> ${repairNumber}<br>
            <strong>Item Name:</strong> ${itemName}<br>
            <strong>Category:</strong> ${itemCategory}
        `;
        acceptForm.setAttribute("action", url);
        modalIncomplete.style.display = "flex";
    };

    window.openCompleteModal = function (url, itemName, itemCategory, repairNumber) {
        console.log("Button clicked!"); // Debugging log
        console.log("Repair Details:", { url, itemName, itemCategory, repairNumber });
        console.log(modal)
        // Update modal details
        modalDetails.innerHTML = `
            <strong>Repair #:</strong> ${repairNumber}<br>
            <strong>Item Name:</strong> ${itemName}<br>
            <strong>Category:</strong> ${itemCategory}
        `;
        acceptForm.setAttribute("action", url);
        // Show the modal
        modal.style.display = "flex";
    };

    // New function for PAT testing modal
    window.openPATResultModal = function (url, itemName, itemCategory, repairNumber, itemDescription) {
        console.log("openPATResultModal called with:", {
            url, 
            itemName, 
            itemCategory, 
            repairNumber, 
            itemDescription
        });

        // Use the same form and modal as other modals
        modalDetails.innerHTML = `
            <strong>Item:</strong> ${itemName}<br>
            <strong>Category:</strong> ${itemCategory}<br>
            <strong>Repair Number:</strong> ${repairNumber}<br>
            <strong>Description:</strong> ${itemDescription}
        `;

        // Set form action to the complete PAT test URL
        acceptForm.setAttribute("action", url);

        // Show modal
        modal.style.display = "flex";
    };

    // Function to close the modal
    const closeModal = () => {
        modal.style.display = "none";
        modalIncomplete.style.display = "none";
    };

    // Attach event listeners to close buttons
    if (modal) modal.querySelector(".close").addEventListener("click", closeModal);
    if (modalIncomplete) modalIncomplete.querySelector(".close").addEventListener("click", closeModal);

    const cancelButtons = document.querySelectorAll(".cancel-btn");
    console.log("Detected Cancel Buttons:", cancelButtons); // Debugging

    cancelButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent form submission (if inside a form)
            closeModal();
            console.log("Cancel Button Clicked"); // Debugging
        });
    });
   
    // Specific PAT test result buttons
    const patResultButtons = document.querySelectorAll('button[name="test_result"]');
    patResultButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const form = this.closest('form');
            const url = form.getAttribute('action');
            const testResult = this.value;

            console.log("PAT Test Result Button Clicked");
            console.log("Form URL:", url);
            console.log("Test Result:", testResult);

            form.submit();
        });
    });

    // Close modal when clicking outside it
    window.addEventListener("click", event => {
        if(modal){
            if (event.target === modal) {
                closeModal();
            }
        }
        if(modalIncomplete){
            if (event.target === modalIncomplete) {
                closeModal();
            }
        }
    });
});