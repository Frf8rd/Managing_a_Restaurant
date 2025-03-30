window.addEventListener("scroll", function() {
    let navbar = document.querySelector(".navbar");
    if (window.scrollY > 50) { 
        navbar.classList.add("navbar-scrolled");
    } else {
        navbar.classList.remove("navbar-scrolled");
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Elemente UI
    const profileIcon = document.getElementById("profile");
    const dropdownMenu = document.getElementById("dropdown-menu");
    const addProductBtn = document.getElementById("add-product-btn");
    const addProductModal = document.getElementById("add-product-modal");
    const editProductModal = document.getElementById("edit-product-modal");
    const addProductForm = document.getElementById("add-product-form");
    const editProductForm = document.getElementById("edit-product-form");
    const productContainer = document.getElementById("product-container");
    const closeButtons = document.querySelectorAll(".close");
    const cancelAddBtn = document.getElementById("cancel-add");
    const cancelEditBtn = document.getElementById("cancel-edit");
    
    // Funcții pentru modals
    function openModal(modal) {
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
    }
    
    function closeModal(modal) {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }
    
    // Dropdown menu
    if (profileIcon && dropdownMenu) {
        profileIcon.addEventListener("click", function(event) {
            event.stopPropagation();
            dropdownMenu.classList.toggle("active");
        });

        document.addEventListener("click", function(event) {
            if (!profileIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.remove("active");
            }
        });
    }
    
    // Add product
    if (addProductBtn) {
        addProductBtn.addEventListener("click", function() {
            openModal(addProductModal);
            dropdownMenu.classList.remove("active");
        });
    }
    
    // Close buttons
    closeButtons.forEach(button => {
        button.addEventListener("click", function() {
            const modal = this.closest(".modal");
            closeModal(modal);
        });
    });
    
    // Cancel buttons
    if (cancelAddBtn) {
        cancelAddBtn.addEventListener("click", function() {
            closeModal(addProductModal);
            addProductForm.reset();
        });
    }
    
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener("click", function() {
            closeModal(editProductModal);
        });
    }
    
    // Close modals on outside click
    window.addEventListener("click", function(event) {
        if (event.target === addProductModal) {
            closeModal(addProductModal);
        }
        if (event.target === editProductModal) {
            closeModal(editProductModal);
        }
    });
    
    // Add product form
    if (addProductForm) {
        addProductForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const formData = new FormData();
            formData.append('name', document.getElementById("name").value);
            formData.append('description', document.getElementById("description").value);
            formData.append('price', document.getElementById("price").value);
            formData.append('image', document.getElementById("image").files[0]);

            fetch("/dashboard", {
                method: "POST",
                body: formData
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                closeModal(addProductModal);
                addProductForm.reset();
                location.reload();
            })
            .catch(error => {
                console.error("Error adding product:", error);
                alert("A apărut o eroare la adăugarea produsului: " + error.message);
            });
        });
    }
    
    // Delete product
    if (productContainer) {
        productContainer.addEventListener("click", function(event) {
            if (event.target.classList.contains("delete-btn")) {
                if (confirm("Ești sigur că vrei să ștergi acest produs?")) {
                    const id = event.target.getAttribute("data-id");

                    fetch("/dashboard", {
                        method: "DELETE",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ id: id })
                    })
                    .then(response => {
                        if (!response.ok) throw new Error('Network response was not ok');
                        return response.json();
                    })
                    .then(data => {
                        const productCard = document.getElementById("product-" + id);
                        if (productCard) productCard.remove();
                    })
                    .catch(error => {
                        console.error("Error deleting product:", error);
                        alert("A apărut o eroare la ștergerea produsului: " + error.message);
                    });
                }
            }
        });
    }
    
    // Edit product modal
    if (productContainer) {
        productContainer.addEventListener("click", function(event) {
            if (event.target.classList.contains("edit-btn")) {
                const button = event.target;
                const id = button.getAttribute("data-id");
                const name = button.getAttribute("data-name");
                const description = button.getAttribute("data-description");
                const price = button.getAttribute("data-price");
                const imageUrl = button.getAttribute("data-image");
                
                document.getElementById("edit-id").value = id;
                document.getElementById("edit-name").value = name;
                document.getElementById("edit-description").value = description;
                document.getElementById("edit-price").value = price;
                document.getElementById("edit-existing-image").value = imageUrl;
                
                openModal(editProductModal);
            }
        });
    }
    
    // Edit product form
    if (editProductForm) {
        editProductForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const formData = new FormData();
            formData.append('id', document.getElementById("edit-id").value);
            formData.append('name', document.getElementById("edit-name").value);
            formData.append('description', document.getElementById("edit-description").value);
            formData.append('price', document.getElementById("edit-price").value);
            formData.append('existing_image', document.getElementById("edit-existing-image").value);

            const newImage = document.getElementById("edit-image").files[0];
            if (newImage) formData.append('image', newImage);

            fetch("/dashboard", {
                method: "PUT",
                body: formData
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                const productCard = document.getElementById("product-" + data.id);
                if (productCard) {
                    productCard.querySelector(".product-title").textContent = data.name || document.getElementById("edit-name").value;
                    productCard.querySelector(".product-description").textContent = data.description || document.getElementById("edit-description").value;
                    productCard.querySelector(".price").textContent = "$" + (data.price || document.getElementById("edit-price").value);
                    if (data.image_url) {
                        productCard.querySelector(".product-image").src = "/static/uploads/" + data.image_url;
                    }
                }
                closeModal(editProductModal);
            })
            .catch(error => {
                console.error("Error updating product:", error);
                alert("A apărut o eroare la actualizarea produsului: " + error.message);
            });
        });
    }
});