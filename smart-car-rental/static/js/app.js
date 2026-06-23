document.addEventListener("DOMContentLoaded", () => {
    const bookingDate = document.querySelector("#booking_date");
    const returnDate = document.querySelector("#return_date");

    if (!bookingDate || !returnDate) {
        return;
    }

    const today = new Date().toISOString().split("T")[0];
    bookingDate.min = today;
    returnDate.min = today;

    bookingDate.addEventListener("change", () => {
        returnDate.min = bookingDate.value || today;
        if (returnDate.value && returnDate.value < bookingDate.value) {
            returnDate.value = bookingDate.value;
        }
    });
});
