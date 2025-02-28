document.addEventListener("DOMContentLoaded", function() {
    const subCategoryField = document.querySelector("#id_sub_category");
    const fashionTypeField = document.querySelector("#id_fashion_type");

    const fashionTypeOptions = {
        "Shirt": ["Short Sleeve", "Long Sleeve", "Short Crop"],
        "Outerwear": ["Jacket", "Cardigan", "Sweaters", "Hoodie"],
        "Bottom": ["Pants", "Skirt", "Shorts"]
    };

    function updateFashionTypes() {
        const selectedSubCategory = subCategoryField.value;
        fashionTypeField.innerHTML = "";

        if (fashionTypeOptions[selectedSubCategory]) {
            fashionTypeOptions[selectedSubCategory].forEach(type => {
                let option = new Option(type, type);
                fashionTypeField.add(option);
            });
        }
    }

    if (subCategoryField) {
        subCategoryField.addEventListener("change", updateFashionTypes);
        updateFashionTypes();  // Initialize the field on page load
    }
});
