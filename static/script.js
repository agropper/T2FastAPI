var createCheckoutSession = function(priceId) {
    return fetch("/create-checkout-session", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        priceId: priceId
      })
    }).then(function(result) {
      return result.json();
    });
  };

const PREMIUM_PRICE_ID = "price_1Icc9NJy4KVxLLXgMytfQvua";
const BASIC_PRICE_ID = "price_1IwzoQJy4KVxLLXg1j48MRUM";
const stripe = Stripe("pk_test_n4B7NQ3lBzJ6OHs8l9VsBWLm");

document.addEventListener("DOMContentLoaded", function(event) {
    document
    .getElementById("checkout-premium")
    .addEventListener("click", function(evt) {
        createCheckoutSession(PREMIUM_PRICE_ID).then(function(data) {
            stripe
                .redirectToCheckout({
                    sessionId: data.sessionId
                });
            });
        });
    
    document
    .getElementById("checkout-basic")
    .addEventListener("click", function(evt) {
        createCheckoutSession(BASIC_PRICE_ID).then(function(data) {
            stripe
                .redirectToCheckout({
                    sessionId: data.sessionId
                });
            });
        });

    const billingButton = document.getElementById("manage-billing");
    if (billingButton) {
        billingButton.addEventListener("click", function(evt) {
        fetch("/create-portal-session", {
            method: "POST"
        })
            .then(function(response) {
                return response.json()
            })
            .then(function(data) {
                window.location.href = data.url;
            });
        })
    }
});
