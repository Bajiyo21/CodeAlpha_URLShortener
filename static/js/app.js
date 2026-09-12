const shortenBtn = document.getElementById("shortenBtn");
const urlInput = document.getElementById("urlInput");
const result = document.getElementById("result");
const shortUrl = document.getElementById("shortUrl");
const copyBtn = document.getElementById("copyBtn");

result.classList.add("hidden");

shortenBtn.addEventListener("click", async () => {

    const originalURL = urlInput.value.trim();

    if (!originalURL) {
        alert("Please enter a URL.");
        return;
    }

    shortenBtn.innerText = "Generating...";
    shortenBtn.disabled = true;

    try {
        const response = await fetch("/api/shorten/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                original_url: originalURL
            })
        });

        const data = await response.json();

        if (response.ok) {

            result.classList.remove("hidden");

            shortUrl.value = data.short_url;

            const qrImage = document.getElementById("qrImage");
            const downloadQR = document.getElementById("downloadQR");

            // Set QR image
            qrImage.src = data.qr_code;

            // Force browser to reload the new image
            qrImage.style.display = "block";

            // Download link
            downloadQR.href = data.qr_code;
} else {
            alert("Invalid URL.");
            console.log(data);
        }

    } catch (error) {
        console.log(error);
        alert("Server error. Is Django running?");
    }

    shortenBtn.innerText = "Shorten URL";
    shortenBtn.disabled = false;
});

copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(shortUrl.value);

    copyBtn.innerText = "Copied ✅";

    setTimeout(() => {
        copyBtn.innerText = "Copy";
    }, 2000);
});
const visitBtn = document.getElementById("visitBtn");

visitBtn.addEventListener("click",()=>{

    if(shortUrl.value !== ""){
        window.open(shortUrl.value,"_blank");
    }

});