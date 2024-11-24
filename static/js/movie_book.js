let selectedScheduledMovieID = null;

const timeButtons = document.querySelectorAll("#timeGrid button");

let currentStep = 1;
const totalSteps = 3;
let selectedSeatsBoxes = document.querySelectorAll(".seat.selected");
let selectedSeatsCount = selectedSeatsBoxes.length;

const container = document.querySelector(".seat-container");
const count = document.getElementById("count");
const total = document.getElementById("total");
const checkoutBtn = document.getElementById("checkout-btn");
const purchase = document.getElementById("purchase-btn");

const movie = JSON.parse("{{ movie|safe }}");

const ticketPrice = movie.price;

const dateGrid = document.getElementById("dateGrid");
const today = new Date();

function initializeSeats() {
  let selectedSeatsBoxes = document.querySelectorAll(".seat[data-seat]");

  let seatData = Array.from(selectedSeatsBoxes).map((seat) => ({
    element: seat,
    code: seat.getAttribute("data-seat"),
  }));

  let sortedSeats = seatData.sort((a, b) => {
    let [rowA, colA] = [a.code.charAt(0), parseInt(a.code.slice(1))];
    let [rowB, colB] = [b.code.charAt(0), parseInt(b.code.slice(1))];

    if (rowA < rowB) return -1;
    if (rowA > rowB) return 1;

    return colA - colB;
  });

  let ctr = 0;
  for (let i = 0; i < 5; i++) {
    for (let j = 0; j < 12; j++) {
      if (selectedSeatsMatrix[i][j] == true) {
        seatData[ctr].element.classList.add("occupied");
      } else {
        seatData[ctr].element.classList.remove("occupied");
      }

      ctr++;
    }
  }
}

// Navigation functions
function updateNavigationButtons() {
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  prevBtn.style.display = currentStep === 1 ? "none" : "block";

  if (currentStep === totalSteps) {
    nextBtn.style.display = "none";
  } else {
    nextBtn.style.display = "block";
    nextBtn.textContent = "Next";
    nextBtn.disabled = !canProceedToNextStep();
  }
  checkSummary();
  initializeSeats();
  console.log(selectedSeatsMatrix);
  updateProgressLine(currentStep, 3);
}

function updateProgressLine(currentStep, totalSteps) {
  const progressLine = document.querySelector(".progress-line");

  const percentage = ((currentStep - 1) / (totalSteps - 1)) * 100;

  progressLine.style.background = `linear-gradient(to right, #ff1414 ${percentage}%, #333 ${percentage}%)`;
}

function canProceedToNextStep() {
  selectedSeats = document.querySelectorAll(".seat.selected");

  switch (currentStep) {
    case 1:
      return (
        selectedCinema !== null &&
        selectedDate !== null &&
        selectedTime !== null
      );
    case 2:
      return selectedSeats.length > 1;
    case 3:
      return selectedSeats.length > 0;
    default:
      return false;
  }
}

function updateProgressBar() {
  document.querySelectorAll(".progress-step").forEach((step, index) => {
    if (index + 1 === currentStep) {
      step.classList.add("active");
      step.classList.remove("completed");
    } else if (index + 1 < currentStep) {
      step.classList.remove("active");
      step.classList.add("completed");
    } else {
      step.classList.remove("active", "completed");
    }
  });
}

function showStep(step) {
  document
    .querySelectorAll(".step")
    .forEach((s) => s.classList.remove("active"));
  document.getElementById(`step${step}`).classList.add("active");
  updateNavigationButtons();
  updateProgressBar();
}

function nextStep() {
  if (canProceedToNextStep()) {
    currentStep++;
    showStep(currentStep);
  }
}

function checkSummary() {
  let selectedSeats = document.querySelectorAll(".seat.selected");
  let selectedSeatsArray = Array.from(selectedSeats).map((seat) =>
    seat.getAttribute("data-seat")
  );

  const movie_box = document.getElementById("selected-movie");
  const cinema = document.getElementById("selected-cinema");
  const date_time = document.getElementById("selected-date-time");
  const seats = document.getElementById("selected-seats");
  const ticket_count = document.getElementById("selected-ticket-count");
  const ticket_price = document.getElementById("selected-ticket-price");
  const total = document.getElementById("selected-total-price");

  movie_box.innerHTML = movie.movie_name;
  cinema.innerHTML = selectedCinema;
  date_time.innerHTML = selectedDate + " at " + selectedTime;
  seats.innerHTML = selectedSeatsArray.join(" ");
  ticket_count.innerHTML =
    "Ticket Price (" + (selectedSeatsArray.length - 1) + "x)";
  ticket_price.innerHTML = "₱" + ticketPrice;
  total.innerHTML =
    "₱" + ((selectedSeatsArray.length - 1) * ticketPrice).toFixed(2);

  for (const combination of validCombinations) {
    const cinemaMatch =
      selectedCinema === null || combination.cinema_name == selectedCinema;
    const dateMatch = selectedDate === null || combination.date == selectedDate;
    const timeMatch = selectedTime === null || combination.time == selectedTime;

    if (cinemaMatch && dateMatch && timeMatch) {
      selectedScheduledMovieID = combination.id;
      selectedSeatsMatrix = combination.seats;
      break;
    }
  }

  selectedSeatsArray = selectedSeatsArray.filter((item) => item != null);

  document.getElementById("scheduled_movie").value = selectedScheduledMovieID;
  document.getElementById("selected_seats").value =
    JSON.stringify(selectedSeatsArray);
}

function prevStep() {
  if (currentStep > 1) {
    currentStep--;
    showStep(currentStep);
  }
}

container.addEventListener("click", (e) => {
  if (
    e.target.classList.contains("seat") &&
    !e.target.classList.contains("occupied")
  ) {
    e.target.classList.toggle("selected");
    const selectedSeats = document.querySelectorAll(
      ".row .seat.selected"
    ).length;
    count.textContent = selectedSeats;
    total.textContent = (selectedSeats * ticketPrice).toFixed(2);

    checkoutBtn.disabled = selectedSeats === 0;
    updateNavigationButtons();
  }
});

function toPurchase() {
  document.getElementById("paymentModal").style.display = "flex";
}

function closeModal(modalId) {
  document.getElementById(modalId).style.display = "none";
}

checkoutBtn.addEventListener("click", () => {
  const selectedSeats = document.querySelectorAll(".row .seat.selected");
  const seatNumbers = Array.from(selectedSeats).map(
    (seat) => seat.dataset.seat
  );
  const totalAmount = parseFloat(total.textContent);
});

// Selection functions

const validCombinations = JSON.parse("{{ valid_combinations|safe }}");
const cinemaButtons = document.querySelectorAll("#cinemaGrid button");
const dateButtons = document.querySelectorAll("#dateGrid button");

let selectedCinema = null;
let selectedDate = null;
let selectedTime = null;
let selectedSeatsMatrix = null;

function selectCinema(cinema) {
  if (selectedCinema == cinema) {
    event.target.classList.remove("selected");
    selectedCinema = null;
  } else {
    selectedCinema = cinema;

    document.querySelectorAll("#cinemaGrid button").forEach((btn) => {
      btn.classList.remove("selected");
    });

    event.target.classList.add("selected");
  }

  updateSelectionSummary();
  updateNavigationButtons();

  dateButtons.forEach((btn) => {
    let date = btn.getAttribute("data-date");
    btn.disabled = !isValidCombination(selectedCinema, date, selectedTime);
  });

  timeButtons.forEach((btn) => {
    let time = btn.getAttribute("data-time");
    btn.disabled = !isValidCombination(selectedCinema, selectedDate, time);
  });
}

function selectDate(date) {
  if (selectedDate == date) {
    event.target.classList.remove("selected");
    selectedDate = null;
  } else {
    selectedDate = date;
    document.querySelectorAll("#dateGrid button").forEach((btn) => {
      btn.classList.remove("selected");
    });
    event.target.classList.add("selected");
  }

  updateSelectionSummary();
  updateNavigationButtons();

  cinemaButtons.forEach((btn) => {
    let cinema = btn.getAttribute("data-cinema");
    btn.disabled = !isValidCombination(cinema, selectedDate, selectedTime);
  });

  timeButtons.forEach((btn) => {
    let time = btn.getAttribute("data-time");
    btn.disabled = !isValidCombination(selectedCinema, selectedDate, time);
  });
}

function selectTime(time) {
  if (selectedTime == time) {
    event.target.classList.remove("selected");
    selectedTime = null;
  } else {
    selectedTime = time;
    document.querySelectorAll("#timeGrid button").forEach((btn) => {
      btn.classList.remove("selected");
    });
    event.target.classList.add("selected");
  }

  updateSelectionSummary();
  updateNavigationButtons();

  cinemaButtons.forEach((btn) => {
    let cinema = btn.getAttribute("data-cinema");
    btn.disabled = !isValidCombination(cinema, selectedDate, selectedTime);
  });

  dateButtons.forEach((btn) => {
    let date = btn.getAttribute("data-date");
    btn.disabled = !isValidCombination(selectedCinema, date, selectedTime);
  });
}

function updateSelectionSummary() {
  const summaryText = document.getElementById("summaryText");
  if (selectedCinema && selectedDate && selectedTime) {
    summaryText.textContent = `Cinema ${selectedCinema} | ${selectedDate} | ${selectedTime}`;
  } else {
    const missing = [];
    if (!selectedCinema) missing.push("cinema");
    if (!selectedDate) missing.push("date");
    if (!selectedTime) missing.push("time");
    summaryText.textContent = `Please select: ${missing.join(", ")}`;
  }
}

function isValidCombination(cinema, date, time) {
  return validCombinations.some((combination) => {
    const cinemaMatch = cinema === null || combination.cinema_name == cinema;
    const dateMatch = date === null || combination.date == date;
    const timeMatch = time === null || combination.time == time;

    return cinemaMatch && dateMatch && timeMatch;
  });
}

// Initialize the booking system
window.onload = function () {
  updateNavigationButtons();
  updateSelectionSummary();
};
