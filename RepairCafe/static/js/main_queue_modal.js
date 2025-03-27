document.addEventListener("DOMContentLoaded", function () {
    let isRedirecting = false;

    const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    const mainQueueSocket = new WebSocket(
        protocol + window.location.host + '/ws/main_queue/'
    );

    mainQueueSocket.onmessage = function (e) {
        if (isRedirecting) {
            return;
        }

        const data = JSON.parse(e.data);

        location.reload(); // Reload the page on queue update
    };


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
    const patModal = document.getElementById("patTestModal");

    



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

    window.openPatModal = function (url, itemName, itemCategory, repairNumber) {
        
        const patModalDetails = document.getElementById("pat-modal-item-details");
        const patTestForm = document.getElementById("pat-test-form");
        const rejectPatForm = document.getElementById("reject-pat-form");
    
        patModalDetails.innerHTML = `
            <strong>Repair #:</strong> ${repairNumber}<br>
            <strong>Item Name:</strong> ${itemName}<br>
            <strong>Category:</strong> ${itemCategory}
        `;
        
        // Set action URLs for both forms
        patTestForm.setAttribute("action", url);
        rejectPatForm.setAttribute("action", url);
        
        patModal.style.display = "flex";
    };


    const closeModal = () => {
        if(modal){
            modal.style.display = "none";
        }
        if(modalIncomplete){
            modalIncomplete.style.display = "none";
        }

        if(patModal){
            patModal.style.display = "none";
        }
        sessionStorage.removeItem("openModalRepairNumber");
        sessionStorage.removeItem("openModalType");
    };


    if (modal) modal.querySelector(".close").addEventListener("click", closeModal);
    if (modalIncomplete) modalIncomplete.querySelector(".close").addEventListener("click", closeModal);
    if (patModal) patModal.querySelector(".close").addEventListener("click", closeModal);

    const cancelButtons = document.querySelectorAll(".cancel-btn");


    cancelButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); 
            closeModal();
        });
    });

   
    // Close modal when clicking outside it
    window.addEventListener("click", event => {
        if (modal && event.target === modal) closeModal();
        if (modalIncomplete && event.target === modalIncomplete) closeModal();
        if (patModal && event.target === patModal) closeModal();
    })

    

acceptForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission
    const actionUrl = acceptForm.getAttribute("action");
    redirectToRepairItem(actionUrl); // Call the redirect function
});

// Redirection function
function redirectToRepairItem(url) {
    isRedirecting = true; 
    document.body.style.cursor = "wait"; 
    window.location.href = url; 
}

function checkSessionAndOpenModal() {
    const repairNumber = sessionStorage.getItem("openModalRepairNumber");
    const modalType = sessionStorage.getItem("openModalType");

    if (repairNumber && modalType) {
       
        const ticketElement = document.querySelector(
            `.ticket-form[data-repair-number="${repairNumber}"]`
        );

        if (ticketElement) {
            const itemName = ticketElement.querySelector("h2:nth-child(1)").textContent.split(": ")[1];
            const itemCategory = ticketElement.querySelector("h2:nth-child(3)").textContent.split(": ")[1];
            const url = `/RepairCafe/repair_ticket/${repairNumber}/`;

            openModal(url, itemName, itemCategory, repairNumber);
        } else {
            sessionStorage.removeItem("openModalRepairNumber");
            sessionStorage.removeItem("openModalType");
        }
    } 
}

    checkSessionAndOpenModal();

});

