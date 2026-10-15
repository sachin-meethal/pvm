let cart = [];

function addItem(id, name, price) {
    const existing = cart.find(item => item.id === id);

    if (existing) {
        existing.qty++;
    } else {
        cart.push({
            id: id,
            name: name,
            price: Number(price),
            qty: 1
        });
    }

    renderCart();
}

function renderCart() {
    let html = "";
    let total = 0;

    cart.forEach(item => {
        const lineTotal = item.qty * item.price;
        total += lineTotal;

        html += `
            <div class="d-flex justify-content-between mb-2">
                <div>
                    <strong>${item.name}</strong><br>
                    ${item.qty} × ₹${item.price}
                </div>
                <div>₹${lineTotal}</div>
            </div>
        `;
    });

    if (cart.length === 0) {
        html = "<p class='text-muted'>No items selected.</p>";
    }

    document.getElementById("cart-items").innerHTML = html;
    document.getElementById("cart-total").textContent = "₹" + total;
}

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

function saveBill() {

    if (cart.length === 0) {
        alert("Please add at least one item.");
        return;
    }

    fetch("/billing/save/", {
        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },

        body: JSON.stringify({
            customer_name: document.getElementById("customer-name").value,
            payment_method: document.getElementById("payment-method").value,
            cart: cart
        })

    })
    .then(response => response.json())
    .then(data => {

        if (data.status === "success") {

            alert(
                "Bill Saved!\n\n" +
                "Bill No : " + data.bill_no +
                "\nTotal : ₹" + data.total
            );

            cart = [];
            renderCart();

            document.getElementById("customer-name").value = "";
            document.getElementById("payment-method").value = "Cash";

        } else {

            alert(data.message);

        }

    })
    .catch(error => {
        console.error(error);
        alert("Error saving bill.");
    });

}