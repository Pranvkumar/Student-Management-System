// Show a welcome message when page loads
document.addEventListener("DOMContentLoaded", () => {
    console.log("Page loaded!");
    alert("Welcome to the HTML Syntax Examples page!");

    // Animate progress bar
    const progress = document.querySelector("progress");
    let value = 0;
    const interval = setInterval(() => {
        value += 1;
        progress.value = value;
        if (value >= 70) clearInterval(interval);
    }, 50);

    // Dynamic meter update
    const meter = document.querySelector("meter");
    let meterValue = 0.0;
    setInterval(() => {
        meterValue = (meterValue + 0.1) % 1.0;
        meter.value = meterValue;
    }, 500);

    // Form name greeting
    const nameInput = document.getElementById("name");
    nameInput.addEventListener("input", () => {
        document.title = `Hello, ${nameInput.value || "Guest"}!`;
    });

    // Toggle table row highlight on click
    document.querySelectorAll("table tbody tr").forEach(row => {
        row.addEventListener("click", () => {
            row.classList.toggle("highlight");
        });
    });
});

// Existing button click function
function showAlert() {
    alert('Button clicked!');
}