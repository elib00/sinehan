//main
document.addEventListener("DOMContentLoaded", () => {
    const data = JSON.parse(document.getElementById('displayData').textContent);
    initializeTicketsDisplayOptionsDropdown(data);
});

//helpers
const initializeTicketsDisplayOptionsDropdown = (data) => {
    const ticketsDisplayOptionsDropdown = document.getElementById("ticketsDisplayOptionsDropdown");
    const ticketsDisplayOptionsButton = document.getElementById("ticketsDisplayOptionsButton");

    ticketsDisplayOptionsButton.addEventListener("mouseenter", () => {
        ticketsDisplayOptionsDropdown.classList.remove("hidden");
    });

    // Hide the dropdown when mouse leaves both the button and the dropdown
    ticketsDisplayOptionsButton.addEventListener("mouseleave", () => {
        setTimeout(() => {
            if (!ticketsDisplayOptionsDropdown.matches(":hover") && !ticketsDisplayOptionsButton.matches(":hover")) {
                ticketsDisplayOptionsDropdown.classList.add("hidden");
            }
        }, 100);  // Small delay to handle the mouse movement gracefully
    });

    ticketsDisplayOptionsDropdown.addEventListener("mouseleave", () => {
        setTimeout(() => {
            if (!ticketsDisplayOptionsButton.matches(":hover") && !ticketsDisplayOptionsDropdown.matches(":hover")) {
                ticketsDisplayOptionsDropdown.classList.add("hidden");
            }
        }, 100);  // Small delay to handle the mouse movement gracefully
    });

    const allTicketsChoice = document.getElementById("allTicketsChoice");
    const scheduledMovieChoice = document.getElementById("scheduledMovieChoice");
    const usersChoice = document.getElementById("usersChoice");

    allTicketsChoice.addEventListener("click", () => {
        displayByAllTickets(data.tickets);
    });


    scheduledMovieChoice.addEventListener("click", () => {
        displayByScheduledMovie(data.scheduledMovies);
    });
    

    usersChoice.addEventListener("click", () => {
        displayByUsers(data.users);
    });
};

const addListenersToCancelTicketButtons = () => {
    const ticketsGrid = document.getElementById("ticketsGrid");
    const cancelTicketButtons = ticketsGrid.querySelectorAll("[data-cancel-ticket-button]");
    const modalContainer = document.getElementById('cancelTicketConfirmationModal');
    const keepReservationButton = document.getElementById('keepReservationButton');
    const cancelTicketForm = document.getElementById("cancelTicketForm")

    cancelTicketButtons.forEach(button => {
        button.addEventListener("click", () => {
            modalContainer.classList.remove("hidden");
            const url = button.getAttribute("data-cancel-url");
            cancelTicketForm.action = url;
        });
    });

    // Close the modal when clicking "Stay" button
    keepReservationButton.addEventListener('click', () => {
        modalContainer.classList.add('hidden');
    });
}

const addListenersToEditTicketButtons = () => {
    const changeSeatModal = document.getElementById('seatMappingModal');
    const openEditTicketButtons = document.querySelectorAll("[data-edit-ticket-button]");
    const closeModalBtn = document.getElementById('closeSeatMappingModal');
    const cancelBtn = document.getElementById('cancelSeatMapping');
    const seatMappingForm = document.getElementById('seatMappingForm');
    const modalOverlay = document.querySelector("[data-modal-overlay]");

    const closeEditTicketModal = () => {
        changeSeatModal.classList.remove('flex');
        changeSeatModal.classList.add('hidden');
    };

    openEditTicketButtons.forEach(button => {
        button.addEventListener("click", () => {
            changeSeatModal.classList.remove('hidden');
            changeSeatModal.classList.add('flex');
            
            const currentSeat = changeSeatModal.querySelector("#currentSeat");
            currentSeat.value = button.getAttribute("data-seat-identifier"); 
            const url = button.getAttribute("data-edit-ticket-url");    
            seatMappingForm.action = url;
        }); 
    });

    closeModalBtn.addEventListener('click', closeEditTicketModal);
    cancelBtn.addEventListener('click', closeEditTicketModal);
    modalOverlay.addEventListener("click", closeEditTicketModal);
}

const addListenersToViewTicketButtons = (ticketsArray, typeOfDisplay) => {
    const viewTicketButtons = document.querySelectorAll("[data-view-tickets-button]");
    console.log(viewTicketButtons);
    viewTicketButtons.forEach(button => {
        button.addEventListener("click", () => {
            buttonIndex = button.getAttribute("data-ticket-index");
            openTicketDetailsModal(ticketsArray[buttonIndex], typeOfDisplay);
        });
    });
};

const displayByAllTickets = (tickets) => {
    const displayedByText = document.getElementById("displayedByText");
    const container = document.getElementById("ticketsContainer");
    const newTicketGrid = document.createElement("div");

    newTicketGrid.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 box-border";
    newTicketGrid.id = "ticketsGrid";
    let html = ``;

    for(let ticket of tickets){
        html += `
                <div 
                    class="bg-white border border-gray-200 rounded-xl shadow-md overflow-hidden overflow-hidden transform transition-all duration-300 hover:scale-105">
                    <div class="p-5 space-y-3">
                        <!-- Header Section -->
                        <div class="flex justify-between items-center border-b border-gray-100">
                            <div class="flex items-center space-x-4">
                                <div class="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center">
                                    <img src="/static/icons/ticket_icon.svg" alt="Icon" class="w-8 h-8">
                                </div>
                                <div>
                                    <h3 class="text-xl font-bold text-gray-800">Ticket #${ ticket.ticket_id }</h3>
                                </div>
                            </div>
                            <div class="flex items-center sm:flex-col md:flex-col lg:flex-row">
                                <button 
                                    class="text-blue-600 hover:text-blue-800 p-2 rounded-full hover:bg-blue-50"
                                    data-ticket-id="${ticket.ticket_id}"
                                    data-seat-identifier="${ticket.seat_identifier}"
                                    title="Edit seat identifier"
                                    data-edit-ticket-button
                                    data-edit-ticket-url="/admin/dashboard/edit_ticket_seat/${ticket.ticket_id}/"
                                    >
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                                    </svg>
                                </button>
                                <span class="${ticket.ticket_is_active ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"} px-3 py-1 rounded-full text-sm font-medium">
                                    ${ticket.ticket_is_active ? "Active" : "Inactive"}
                                </span>
                            </div>
                        </div>
                
                        <!-- User Details Row -->
                        <div>
                            <p class="text-base text-gray-800 font-medium">${ticket.user_first_name} ${ticket.user_last_name}</p>
                            <p class="text-sm text-gray-600 truncate">${ticket.user_email}</p>
                        </div>
                
                        <!-- Movie Details Row -->
                        <div>
                            <h2 class="text-lg font-bold text-gray-800 truncate">${ticket.scheduled_movie_movie_name}</h2>
                            <p class="text-sm text-gray-600">
                                ${ticket.scheduled_movie_date}
                                <span class="mx-1">•</span> 
                                ${ticket.scheduled_movie_time}
                            </p>
                        </div>
                
                        <!-- Additional Information -->
                        <div class="grid grid-cols-2 gap-3 text-sm text-gray-700">
                            <div class="flex items-center space-x-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" fill="#4CAF50" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" fill="#2196F3" />
                                </svg>
                                <span class="text-sm text-gray-600 truncate">${ticket.scheduled_movie_cinema_name}</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="10" fill="#FFC107" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="#FFFFFF" stroke-width="2" />
                                </svg>
                                <span class="text-sm text-gray-600">Available Seats: ${ticket.available_seats }</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" fill="#9C27B0" stroke="#FFFFFF" stroke-width="2" />
                                </svg>
                                <span class="text-sm text-gray-600">Seat: ${ticket.seat_identifier}</span>
                            </div>
                        </div>
                
                        <!-- Action Buttons -->
                        <!-- 
                        <div class="flex space-x-3 border-t border-gray-100">
                            <button class="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors duration-300 text-sm font-semibold">
                                View Details
                            </button> -->`

        if(ticket.ticket_is_active){
            html += `
                    <button 
                        data-cancel-ticket-button
                        data-cancel-url="/admin/dashboard/cancel_ticket/${ticket.ticket_id}/"
                        class="flex-1 bg-red-500 w-full text-white py-3 rounded-lg hover:bg-red-600 transition-colors duration-300 text-sm font-semibold">
                        Cancel Ticket
                    </button>
            `;
        }              
                              
        html +=        `</div>
                    </div>
                </div>`;

        // html += `
        //         <div 
        //             class="bg-white shadow-md rounded-lg overflow-hidden transform transition-all duration-300 hover:scale-105">
        //             <div class="p-6">
        //                 <!-- Ticket Info -->
        //                 <div class="mb-4 flex items-center space-x-4">
        //                     <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
        //                         <img src="/static/icons/ticket_icon.svg" alt="Icon" class="w-8 h-8">
        //                     </div>
        //                     <div>
        //                         <h3 class="font-semibold text-xl">Ticket #${ ticket.ticket_id }</h3>
        //                     </div>
        //                 </div>

        //                 <!-- User Info -->
        //                 <div class="mb-4 flex-col items-center">
        //                     <p class="text-base"><span class="font-medium">Holder:</span> ${ticket.user_first_name} ${ticket.user_last_name}</p>
        //                     <p class="text-base"><span class="font-medium">Email:</span> ${ticket.user_email}</p>
        //                 </div>

        //                 <div class="mb-4 flex flex-row items-center gap-4">
        //                     <span class="${ticket.ticket_is_active ? "bg-green-500" : "bg-red-500"} text-white px-3 py-1 rounded-full text-sm">
        //                         ${ticket.ticket_is_active ? "Active" : "Inactive"}
        //                     </span>
        //                     <p class="text-sm">Available seats: ${ticket.available_seats}</p>
        //                 </div>

        //                 <!--  Demarcation -->
        //                 <div class="border-t border-gray-300 my-2"></div>

        //                 <!-- Movie Details -->
        //                 <div class="space-y-3">
        //                     <div>
        //                         <h2 class="text-xl font-bold text-gray-800">
        //                             ${ticket.scheduled_movie_movie_name}
        //                         </h2>
        //                         <p class="text-gray-600 text-sm">
        //                             ${ticket.scheduled_movie_date} at ${ticket.scheduled_movie_time}
        //                         </p>
        //                     </div>

        //                     <!-- Additional Ticket Details -->
        //                     <div class="grid grid-cols-2 gap-2 text-sm text-gray-600">
        //                         <div class="flex items-center">
        //                             <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        //                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
        //                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
        //                             </svg>
        //                             <span>${ticket.scheduled_movie_cinema_name}</span>
        //                         </div>
        //                         <div class="flex items-center">
        //                             <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        //                                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
        //                             </svg>
        //                             <span>Seat: ${ticket.seat_identifier }</span>
        //                         </div>
        //                     </div>

        //                     <!-- Action Buttons -->
        //                     <div class="flex space-x-3 mt-4 justify-between">
        //                         <button 
        //                             class="flex-1 block w-full text-center bg-black text-white py-2 rounded-md transition duration-300">
        //                             View Details
        //                         </button>`
        // if(ticket.ticket_is_active){
        //     html += 
        //             `<button
        //                 data-cancel-ticket-button
        //                 data-cancel-url="/admin/dashboard/cancel_ticket/${ticket.ticket_id}/"
        //                 class="flex-1 block w-full text-center bg-red-500 text-white py-2 rounded-md hover:bg-red-600 transition duration-300">
        //                     Cancel Ticket
        //             </button>`
        // }                       

        // html +=             `</div>
        //                 </div>
        //             </div>
        //         </div>
        // `
    }



    newTicketGrid.innerHTML = html;
    replaceWithGSAP(container, newTicketGrid, [addListenersToCancelTicketButtons, addListenersToEditTicketButtons]);
    displayedByText.textContent = "By All Tickets";
};

const displayByScheduledMovie = (scheduledMovies) => {
    const displayedByText = document.getElementById("displayedByText");
    const container = document.getElementById("ticketsContainer");
    const newTicketGrid = document.createElement("div");

    newTicketGrid.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 box-border";
    newTicketGrid.id = "ticketsGrid";
    let html = ``;

    let index = 0;
    let ticketsArray = [];
    for(let movie of scheduledMovies) {
        html += `
                <div 
                    class="bg-white shadow-md rounded-lg overflow-hidden transform transition-all duration-300 hover:scale-105">
                    <div class="p-6">
                        <!-- Ticket Info -->
                        <div class="mb-4 flex items-center space-x-4">
                            <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                                <img src="/static/icons/ticket_icon.svg" alt="Icon" class="w-8 h-8">
                            </div>
                            <div>
                                <h3 class="font-bold text-xl text-gray-800">Scheduled Movie #${movie.scheduled_movie_id}</h3>
                            </div>
                        </div>

                        <div class="mb-4 flex items-center space-x-4">
                            <span class="${movie.scheduled_movie_is_active ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"} px-3 py-1 rounded-full text-sm font-medium">
                                ${movie.scheduled_movie_is_active ? "Active" : "Inactive"}
                            </span>
                            <p class="text-lg font-semibold text-gray-800 italic"> ${movie.scheduled_movie_movie_name } </p>
                        </div>

                        <!--  Demarcation -->
                        <div class="border-t border-gray-300 my-2"></div>

                        <!-- Movie Details -->
                        <div class="space-y-3">
                            <div>
                                <div class="flex items-center space-x-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" fill="#4CAF50" />
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" fill="#2196F3" />
                                    </svg>
                                    <span class="truncate text-lg font-bold text-gray-800">${movie.scheduled_movie_cinema_name}</span>
                                </div>
                                <p class="text-sm text-gray-600">
                                    ${movie.scheduled_movie_date}
                                    <span class="mx-1">•</span> 
                                    ${movie.scheduled_movie_time}
                                </p>
                            </div>

                            <!-- Action Buttons -->
                            <div class="flex space-x-3 mt-4 justify-between">
                                <button 
                                    data-view-tickets-button
                                    data-ticket-index=${index}
                                    class="flex-1 block w-full text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors duration-300 text-sm font-semibold">
                                    View Tickets
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
        `;

        index++;
        ticketsArray.push(movie.scheduled_movie_tickets);
    }

    newTicketGrid.innerHTML = html;
    replaceWithGSAP(container, newTicketGrid, [() => addListenersToViewTicketButtons(ticketsArray, "scheduledMovie")]);
    displayedByText.textContent = "By Scheduled Movie";
}

const displayByUsers = (users) => {
    const displayedByText = document.getElementById("displayedByText");
    const container = document.getElementById("ticketsContainer");
    const newTicketGrid = document.createElement("div");

    newTicketGrid.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 box-border";
    newTicketGrid.id = "ticketsGrid";
    let html = ``;

    let index = 0;
    let ticketsArray = [];
    for(let user of users){
        html += `
                <div 
                    class="bg-white shadow-md rounded-lg overflow-hidden transform transition-all duration-300 hover:scale-105">
                    <div class="p-6">
                        <!-- Ticket Info -->
                        <div class="mb-4 flex items-center space-x-4">
                            <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                                <img src="/static/icons/ticket_icon.svg" alt="Icon" class="w-8 h-8">
                            </div>
                            <div>
                                <h3 class="font-bold text-xl">User #${user.user_id}</h3>
                            </div>
                        </div>

                        <!--  Demarcation -->
                        <div class="border-t border-gray-300 my-2"></div>


                        <!-- User Info -->
                        <div class="mb-4 p-4 border border-gray-300 rounded-lg shadow-md bg-white">
                            <div class="flex items-center mb-3">
                                <div class="w-12 h-12 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                                    ${user.user_first_name.charAt(0)}${user.user_last_name.charAt(0)}
                                </div>
                                <h3 class="ml-4 text-lg font-bold text-gray-900">${user.user_first_name} ${user.user_last_name}</h3>
                            </div>
                            <ul class="space-y-2 text-gray-700">
                                <li class="flex items-center">
                                    <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A10.975 10.975 0 0112 15c2.203 0 4.254.634 5.879 1.804"></path>
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a4 4 0 10-8 0 4 4 0 008 0z"></path>
                                    </svg>
                                    <span><span class="font-medium">Username:</span> ${user.user_username}</span>
                                </li>
                                <li class="flex items-center">
                                    <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7v5h-1m-3 3h.01M10 20h4a2 2 0 002-2v-5a2 2 0 00-2-2h-4a2 2 0 00-2 2v5a2 2 0 002 2z"></path>
                                    </svg>
                                    <span class="truncate"><span class="font-medium">Email:</span> ${user.user_email}</span>
                                </li>
                            </ul>
                        </div>

                        <div class="space-y-3">
                            <div class="flex space-x-3 mt-4 justify-between">
                                <button
                                    data-view-tickets-button
                                    data-ticket-index=${index}
                                    class="flex-1 block w-full text-center bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors duration-300 text-sm font-semibold">
                                    View Tickets
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
        `;
        
        ticketsArray.push(user.user_tickets);
        index++;
    }

    newTicketGrid.innerHTML = html;
    replaceWithGSAP(container, newTicketGrid, [() => addListenersToViewTicketButtons(ticketsArray, "user")]);
    displayedByText.textContent = "By Users";
};

const replaceWithGSAP = (container, newContent, callbacksArray) => {
    // Animate out current content
    gsap.to(container.children, {
        opacity: 0,
        y: 50,
        duration: 0.5,
        onComplete: () => { 
            // Clear and add new content
            container.innerHTML = '';
            container.appendChild(newContent);

            if (Array.isArray(callbacksArray) && callbacksArray.length > 0) {
                callbacksArray.forEach(callback => {
                    if (typeof callback === "function") {
                        callback();
                    }
                });
            }

            // Animate in new content
            gsap.from(container.children, {
                opacity: 0,
                y: -50,
                duration: 0.5
            });
        }
    });
}

function createUserTicketDetailCard(ticket) {
    // Create a container for each ticket
    const ticketCard = document.createElement('div');
    if (!ticket) {
        ticketCard.className = 'bg-gray-50 rounded-xl p-6 shadow-lg border border-gray-200 flex items-center justify-center text-center';
        ticketCard.innerHTML = `
            <div class="space-y-4">
                <svg class="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a4.978 4.978 0 01-1.414-2.829m-1.414-5.657a9 9 0 0112.728 0m-12.728 0L3 3m4.243 4.243l-2.829 2.829m2.829-2.829v5.657"></path>
                </svg>
                <h3 class="text-xl font-semibold text-gray-700">No Tickets Found</h3>
                <p class="text-gray-500">This scheduled movie currently has no ticket reservations.</p>
            </div>
        `;
        return ticketCard;
    }

    ticketCard.className = 'bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 shadow-lg border border-gray-200 relative overflow-hidden';
    // Ticket Header with cinema and movie details
    const ticketHeader = `
        <div class="mb-4 pb-4 border-b border-gray-300 relative">
            <div class="flex justify-between items-center">
                <div class="space-y-1">
                    <h3 class="text-xl font-bold text-gray-800">${ticket.ticket_scheduled_movie_movie_name}</h3>
                    <div class="flex items-center space-x-2">
                        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        </svg>
                        <p class="text-sm text-gray-600 font-medium">${ticket.ticket_cinema_cinema_name}</p>
                    </div>
                </div>
                <div class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                    Ticket #${ticket.ticket_id}
                </div>
            </div>
        </div>
    `;

    // Ticket Details Section
    const ticketDetails = `
        <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
                <p class="text-xs text-gray-500 font-medium uppercase">Date</p>
                <div class="flex items-center space-x-2">
                    <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                    <p class="text-base text-gray-800 font-semibold">${ticket.ticket_scheduled_movie_date}</p>
                </div>
            </div>
            <div class="space-y-2">
                <p class="text-xs text-gray-500 font-medium uppercase">Time</p>
                <div class="flex items-center space-x-2">
                    <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <p class="text-base text-gray-800 font-semibold">${ticket.ticket_scheduled_movie_time}</p>
                </div>
            </div>
            <div class="space-y-2">
                <p class="text-xs text-gray-500 font-medium uppercase">Seat</p>
                <div class="flex items-center space-x-2">
                    <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <p class="text-base text-gray-800 font-semibold">${ticket.ticket_seat_identifier}</p>
                </div>
            </div>
            <div class="space-y-2">
                <p class="text-xs text-gray-500 font-medium uppercase">Status</p>
                <div class="flex items-center space-x-2">
                    <span class="w-3 h-3 ${ticket.ticket_is_active ? 'bg-green-500' : 'bg-red-500'} rounded-full"></span>
                    <p class="text-base ${ticket.ticket_is_active ? 'text-green-800' : 'text-red-800'} font-semibold">
                        ${ticket.ticket_is_active ? 'Active' : 'Inactive'}
                    </p>
                </div>
            </div>
        </div>
    `;

    // Combine the sections
    ticketCard.innerHTML = `
        ${ticketHeader}
        ${ticketDetails}
    `;

    return ticketCard;
}

function createScheduledMovieTicketDetailCard(ticket) {
    // Create a container for each ticket
    const ticketCard = document.createElement('div');

    ticketCard.className = 'bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 shadow-lg border border-gray-200 relative overflow-hidden';
    // Ticket Header with ticket details
    const ticketHeader = `
        <div class="mb-4 pb-4 border-b border-gray-300 relative">
            <div class="flex justify-between items-center">
                <div class="space-y-1">
                    <h3 class="text-xl font-bold text-gray-800">${ticket.ticket_holder}</h3>
                    <div class="flex items-center space-x-2">
                        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                        </svg>
                        <p class="text-sm text-gray-600 font-medium">${ticket.ticket_holder_username}</p>
                    </div>
                </div>
                <div class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                    Ticket #${ticket.ticket_id}
                </div>
            </div>
        </div>
    `;

    // Ticket Details Section
    const ticketDetails = `
        <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
                <p class="text-xs text-gray-500 font-medium uppercase">Seat</p>
                <div class="flex items-center space-x-2">
                    <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <p class="text-base text-gray-800 font-semibold">${ticket.ticket_seat_identifier}</p>
                </div>
            </div>
            <div class="space-y-2">
                <p class="text-xs text-gray-500 font-medium uppercase">Status</p>
                <div class="flex items-center space-x-2">
                    <span class="w-3 h-3 ${ticket.ticket_is_active === 'Active' ? 'bg-green-500' : 'bg-red-500'} rounded-full"></span>
                    <p class="text-base ${ticket.ticket_is_active === 'Active' ? 'text-green-800' : 'text-red-800'} font-semibold">
                        ${ticket.ticket_is_active}
                    </p>
                </div>
            </div>
        </div>
    `;

    // Combine the sections
    ticketCard.innerHTML = `
        ${ticketHeader}
        ${ticketDetails}
    `;

    return ticketCard;
}

function openTicketDetailsModal(tickets, typeOfDisplay) {
    const modalContainer = document.getElementById('ticketDetailsContainer');
    
    // Clear previous contents
    modalContainer.innerHTML = '';
    
    // Create and append ticket cards
    if(typeOfDisplay === "scheduledMovie"){
        if(tickets.length === 0){
            const emptyTicketCard = document.createElement('div');
            emptyTicketCard.className = 'bg-gray-50 rounded-xl p-6 shadow-lg border border-gray-200 flex items-center justify-center text-center';
            emptyTicketCard.innerHTML = `
                <div class="space-y-4">
                    <svg class="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a4.978 4.978 0 01-1.414-2.829m-1.414-5.657a9 9 0 0112.728 0m-12.728 0L3 3m4.243 4.243l-2.829 2.829m2.829-2.829v5.657"></path>
                    </svg>
                    <h3 class="text-xl font-semibold text-gray-700">No Tickets Found</h3>
                    <p class="text-gray-500">This user currently has no ticket reservations.</p>
                </div>
            `;

            modalContainer.appendChild(emptyTicketCard);
        }else{
            tickets.forEach(ticket => {
                const ticketCard = createScheduledMovieTicketDetailCard(ticket);
                modalContainer.appendChild(ticketCard);
            });   
        } 
    }else if(typeOfDisplay === "user"){
        if(tickets.length === 0){
            const emptyTicketCard = document.createElement('div');
            emptyTicketCard.className = 'bg-gray-50 rounded-xl p-6 shadow-lg border border-gray-200 flex items-center justify-center text-center';
            emptyTicketCard.innerHTML = `
                <div class="space-y-4">
                    <svg class="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a4.978 4.978 0 01-1.414-2.829m-1.414-5.657a9 9 0 0112.728 0m-12.728 0L3 3m4.243 4.243l-2.829 2.829m2.829-2.829v5.657"></path>
                    </svg>
                    <h3 class="text-xl font-semibold text-gray-700">No Tickets Found</h3>
                    <p class="text-gray-500">This user currently has no ticket reservations.</p>
                </div>
            `;

            modalContainer.appendChild(emptyTicketCard);
        }else{
            tickets.forEach(ticket => {
                const ticketCard = createUserTicketDetailCard(ticket);
                modalContainer.appendChild(ticketCard);
            });  
        } 
    }

    // Show modal
    const modal = document.getElementById('ticketDetailsModal');
    modal.classList.remove('hidden');
}

//Close modal functionality
const closeViewTicketDetailsModalButton = document.getElementById('closeTicketDetailsModalButton');
closeViewTicketDetailsModalButton.addEventListener('click', () => {
    const modal = document.getElementById('ticketDetailsModal');
    modal.classList.add('hidden');
});
