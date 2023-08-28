const form = document.getElementById("tradeForm");

        // Get the buy and sell buttons
        const buyButton = document.getElementById("buyButton");
        const sellButton = document.getElementById("sellButton");

        // Add event listeners for the buttons
        buyButton.addEventListener("click", function() {
            form.action = "/buy";
            form.submit();
        });

        sellButton.addEventListener("click", function() {
            form.action = "/sell";
            form.submit();
        });