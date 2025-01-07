document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("confirmationModal");
    const modalDetails = document.getElementById("modal-item-details");
    const acceptForm = modal.querySelector("form");

    // Function to open the modal
    window.openModal = function (url, itemName, itemCategory, repairNumber) {
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

    // Function to close the modal
    const closeModal = () => {
        modal.style.display = "none";
    };

    // Attach event listeners to close buttons
    modal.querySelector(".close").addEventListener("click", closeModal);
    document.getElementById("cancel-btn").addEventListener("click", closeModal);

    // Close modal when clicking outside it
    window.addEventListener("click", event => {
        if (event.target === modal) {
            closeModal();
        }
    });
});
