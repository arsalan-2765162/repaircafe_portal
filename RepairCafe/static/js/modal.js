document.addEventListener("DOMContentLoaded", function () {
    let isRedirecting = false;

    // Add event listeners to each li element to simulate radio button click
    const listItems = document.querySelectorAll('.inc-form li');
    listItems.forEach(function(item) {
        item.addEventListener('click', function() {
            const radioInput = item.querySelector('input[type="radio"]');
            if (radioInput) {
                radioInput.checked = true;
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
        sessionStorage.setItem("openModalRepairNumber", repairNumber);
        sessionStorage.setItem("openModalType", "confirmation"); 

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
        modalDetails.innerHTML = `
            <strong>Repair #:</strong> ${repairNumber}<br>
            <strong>Item Name:</strong> ${itemName}<br>
            <strong>Category:</strong> ${itemCategory}
        `;
        acceptForm.setAttribute("action", url);
        modal.style.display = "flex";
    };

    window.openPATResultModal = function (url, itemName, itemCategory, repairNumber, itemDescription) {

        modalDetails.innerHTML = `
            <strong>Item:</strong> ${itemName}<br>
            <strong>Category:</strong> ${itemCategory}<br>
            <strong>Repair Number:</strong> ${repairNumber}<br>
            <strong>Description:</strong> ${itemDescription}
        `;
        acceptForm.setAttribute("action", url);
        modal.style.display = "flex";
    };

    const closeModal = () => {
        if(modal) {
            modal.style.display = "none";
        }
        if(modalIncomplete) {
            modalIncomplete.style.display = "none";
        }
        sessionStorage.removeItem("openModalRepairNumber");
        sessionStorage.removeItem("openModalType");
    };

    if (modal) modal.querySelector(".close").addEventListener("click", closeModal);
    if (modalIncomplete) modalIncomplete.querySelector(".close").addEventListener("click", closeModal);

    const cancelButtons = document.querySelectorAll(".cancel-btn");
    cancelButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); 
            closeModal();
        });
    });

    // PAT test result buttons
    const patResultButtons = document.querySelectorAll('button[name="test_result"]');
    patResultButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const form = this.closest('form');
            const url = form.getAttribute('action');
            const testResult = this.value;


            form.submit();
        });
    });

    // Close modal when clicking outside
    window.addEventListener("click", event => {
        if(modal && event.target === modal) {
            closeModal();
        }
        if(modalIncomplete && event.target === modalIncomplete) {
            closeModal();
        }
    });

    // Handle form submission
    acceptForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const actionUrl = acceptForm.getAttribute("action");
        redirectToRepairItem(actionUrl);
    });

    // Redirection function
    function redirectToRepairItem(url) {
        isRedirecting = true;
        document.body.style.cursor = "wait";
        window.location.href = url;
    }

    // Check session storage on load
    window.onload = function () {
        const repairNumber = sessionStorage.getItem("openModalRepairNumber");
        const modalType = sessionStorage.getItem("openModalType");

        if (repairNumber && modalType) {
            const ticketElement = document.querySelector(
                `.ticket-form[data-repair-number="${repairNumber}"]`
            );
            if (ticketElement) {
                const itemName = ticketElement.querySelector("h2:nth-child(1)").textContent.split(": ")[1];
                const itemCategory = ticketElement.querySelector("h2:nth-child(3)").textContent.split(": ")[1];
                const url = `/accept_ticket/${repairNumber}/`;

                if (modalType === "confirmation") {
                    openModal(url, itemName, itemCategory, repairNumber);
                }
            }
            sessionStorage.removeItem("openModalRepairNumber");
            sessionStorage.removeItem("openModalType");
        }
    };
});