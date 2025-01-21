document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("demo-autofill2").addEventListener("click", function () {
        const formData = {
            "id_firstName": "Jane",
            "id_lastName": "Doe",
            "id_emailPhone": "jane.doe@example.com",
            "id_postCode": "G12",
            "id_itemName": "Toaster",
            "id_itemDescription": "Doesn't heat up",
        };

        // Loop through formData and populate the fields
        for (const [fieldId, value] of Object.entries(formData)) {
            const field = document.getElementById(fieldId);
            if (field) {
                field.value = value; // Set the value of the input field
            }
        }
    });
});