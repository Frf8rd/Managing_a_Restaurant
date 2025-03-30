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
    
    // Funcție pentru afișarea/ascunderea meniului dropdown
    if (profileIcon && dropdownMenu) {
        profileIcon.addEventListener("click", function(event) {
            event.stopPropagation();
            dropdownMenu.classList.toggle("active");
        });

        // Închide meniul când utilizatorul dă click în afara lui
        document.addEventListener("click", function(event) {
            if (!profileIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.remove("active");
            }
        });
    }
    
    // Funcții pentru modals
    function openModal(modal) {
        modal.style.display = "block";
        document.body.style.overflow = "hidden"; // Blochează scroll-ul pe body
    }
    
    function closeModal(modal) {
        modal.style.display = "none";
        document.body.style.overflow = "auto"; // Reactivează scroll-ul
    }
    
    // Event listener pentru butonul "Add Product" din dropdown
    if (addProductBtn) {
        addProductBtn.addEventListener("click", function() {
            openModal(addProductModal);
            dropdownMenu.classList.remove("active"); // Închide dropdown-ul
        });
    }
    
    // Event listeners pentru butoanele de închidere
    closeButtons.forEach(button => {
        button.addEventListener("click", function() {
            const modal = this.closest(".modal");
            closeModal(modal);
        });
    });
    
    // Event listeners pentru butoanele Cancel
    if (cancelAddBtn) {
        cancelAddBtn.addEventListener("click", function() {
            closeModal(addProductModal);
            addProductForm.reset(); // Resetează formularele
        });
    }
    
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener("click", function() {
            closeModal(editProductModal);
        });
    }
    
    // Închide modalurile când se face click în afara conținutului
    window.addEventListener("click", function(event) {
        if (event.target === addProductModal) {
            closeModal(addProductModal);
        }
        if (event.target === editProductModal) {
            closeModal(editProductModal);
        }
    });
    
    // ✅ Adaugă un produs
    if (addProductForm) {
        addProductForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const name = document.getElementById("name").value;
            const description = document.getElementById("description").value;
            const price = document.getElementById("price").value;
            const image_url = document.getElementById("image_url").value;
            
            // Obiectul pentru Backend
            const productData = {
                name: name,
                description: description,
                price: price,
                image_url: image_url,
                available: true // Presupunem că noile produse sunt disponibile implicit
            };

            fetch("/dashboard", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(productData)
            })
            .then(response => response.json())
            .then(data => {
                closeModal(addProductModal);
                addProductForm.reset();
                location.reload(); // Reîncarcă pagina pentru a vedea noul produs
            })
            .catch(error => {
                console.error("Error adding product:", error);
                alert("A apărut o eroare la adăugarea produsului.");
            });
        });
    }
    
    // ✅ Șterge un produs
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
                    .then(response => response.json())
                    .then(data => {
                        // Eliminăm elementul din DOM
                        const productCard = document.getElementById("product-" + id);
                        if (productCard) {
                            productCard.remove();
                        }
                    })
                    .catch(error => {
                        console.error("Error deleting product:", error);
                        alert("A apărut o eroare la ștergerea produsului.");
                    });
                }
            }
        });
    }
    
    // ✅ Deschide modalul pentru editarea unui produs
    if (productContainer) {
        productContainer.addEventListener("click", function(event) {
            if (event.target.classList.contains("edit-btn")) {
                const button = event.target;
                const id = button.getAttribute("data-id");
                const name = button.getAttribute("data-name");
                const description = button.getAttribute("data-description");
                const price = button.getAttribute("data-price");
                const imageUrl = button.getAttribute("data-image");
                
                // Completează formularele cu valorile existente
                document.getElementById("edit-id").value = id;
                document.getElementById("edit-name").value = name;
                document.getElementById("edit-description").value = description;
                document.getElementById("edit-price").value = price;
                document.getElementById("edit-image_url").value = imageUrl;
                
                // Deschide modalul
                openModal(editProductModal);
            }
        });
    }
    
    // ✅ Actualizează un produs
    if (editProductForm) {
        editProductForm.addEventListener("submit", function(event) {
            event.preventDefault();
            
            const id = document.getElementById("edit-id").value;
            const name = document.getElementById("edit-name").value;
            const description = document.getElementById("edit-description").value;
            const price = document.getElementById("edit-price").value;
            const image_url = document.getElementById("edit-image_url").value;
            
            // Obiectul pentru Backend
            const productData = {
                id: id,
                name: name,
                description: description,
                price: price,
                image_url: image_url,
                available: true // Menținem disponibilitatea
            };
            
            fetch("/dashboard", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(productData)
            })
            .then(response => response.json())
            .then(data => {
                closeModal(editProductModal);
                
                // Actualizăm elementele din DOM
                const productCard = document.getElementById("product-" + id);
                if (productCard) {
                    productCard.querySelector(".product-title").innerText = name;
                    productCard.querySelector(".product-description").innerText = description;
                    productCard.querySelector(".price").innerText = "$" + price;
                    productCard.querySelector(".product-image").src = image_url;
                }
            })
            .catch(error => {
                console.error("Error updating product:", error);
                alert("A apărut o eroare la actualizarea produsului.");
            });
        });
    }
});