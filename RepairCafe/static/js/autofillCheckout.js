document.getElementById("demo-autofill").addEventListener("click", function () {
    const formData = {
        "id_Q1": "Through a friend",
        "id_Q2": "Online search",
        "id_Q3": "It was great! I learned a lot.",
        "id_Q4Extra": "Basic electronics repair",
        "id_Q5Extra": "John Smith john@gmail.com",
        "id_Q6": "Community event",
        "id_Q7": "Laptop",
        "id_Q8": "Dell",
        "id_Q9": "Inspiron 15",
        "id_Q10": "Broken hinge",
        "id_Q11Extra": "",
        "id_Q12Extra": "It belonged to my dad.",
        "id_Q13Extra": "It makes my life more comfortable.",
        "id_Q15": "£500",
        "id_Q16": "Yes, I feel more confident now.",
        "id_Q17": "Wonderful! Everyone was helpful.",
        "id_Q18": "Longer opening hours would be great.",
        "id_Q19": "yes i did",
        "id_Q19Extra": "I met someone who shares my interests.",
        "id_Q20": "Yes, absolutely!"
    };

    // Loop through the formData object and fill the corresponding input fields
    for (const [fieldId, value] of Object.entries(formData)) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.value = value;  // Set the value of the text input field
        }
    }
});

