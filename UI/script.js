function comparePrices() {
    // Sanpdeal
    const snapdealInput = document.getElementById('Snap').value;
    const FlipkartInput = document.getElementById('Flip').value;
    const amazonInput = document.getElementById('Amaz').value;

    const requestdata = {
        snapdeal_url: snapdealInput,
        flipkart_url: FlipkartInput,
        amazon_url: amazonInput
    };
    console.log(requestdata);
    // Make an HTTP request to the Python server
    fetch('http://localhost:5003/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestdata),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        // Handle the data as needed (update UI, etc.)
        if (data.error) {
            console.error(data.error);
        } else {
            console.log("data: ", data);
            const flip = data.flip;
            const snap = data.snap;
            const amaz = data.amaz;
            document.getElementById("snapnameinp").innerText = snap.product_name;
            document.getElementById("snapinp").innerText = "₹"+snap.product_price;
            document.getElementById("flipnameinp").innerText = flip.product_name;
            document.getElementById("flipinp").innerText = flip.product_price;
            document.getElementById("amaznameinp").innerText = amaz.product_name;
            document.getElementById("amazinp").innerText = amaz.product_price;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

}

document.getElementById('btn').addEventListener('click', comparePrices);
