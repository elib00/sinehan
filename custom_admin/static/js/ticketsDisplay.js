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
    const activeChoice = document.getElementById("activeChoice");

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

const displayByAllTickets = (tickets) => {
    const displayedByText = document.getElementById("displayedByText");
    const container = document.getElementById("ticketsContainer");
    const newTicketGrid = document.createElement("div");

    newTicketGrid.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 box-border";
    newTicketGrid.id = "ticketsGrid";
    let html = ``;

    // for(let ticket of tickets){
    //     html += `
    //             <div 
    //                 class="bg-white shadow-md rounded-lg overflow-hidden transform transition-all duration-300 hover:scale-105 cursor-pointer">
    //                 <div class="p-6">
    //                     <!-- Ticket Info -->
    //                     <div class="mb-4 flex items-center space-x-4">
    //                         <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
    //                             <img src="/static/icons/ticket_icon.svg" alt="Icon" class="w-8 h-8">
    //                         </div>
    //                         <div>
    //                             <h3 class="font-semibold text-xl">Ticket #${ ticket.ticket_id }</h3>
    //                         </div>
    //                     </div>

    //                     <!-- User Info -->
    //                     <div class="mb-4 flex-col items-center">
    //                         <p class="text-base"><span class="font-medium">Holder:</span> ${ticket.user_first_name} ${ticket.user_last_name}</p>
    //                         <p class="text-base"><span class="font-medium">Email:</span> ${ticket.user_email}</p>
    //                     </div>

    //                     <div class="mb-4 flex flex-row items-center gap-4">
    //                         <span class="${ticket.ticket_is_active ? "bg-green-500" : "bg-red-500"} text-white px-3 py-1 rounded-full text-sm">
    //                             ${ticket.ticket_is_active ? "Active" : "Inactive"}
    //                         </span>
    //                         <p class="text-sm">Available seats: ${ticket.available_seats}</p>
    //                     </div>

    //                     <!--  Demarcation -->
    //                     <div class="border-t border-gray-300 my-2"></div>

    //                     <!-- Movie Details -->
    //                     <div class="space-y-3">
    //                         <div>
    //                             <h2 class="text-xl font-bold text-gray-800">
    //                                 ${ticket.scheduled_movie_movie_name}
    //                             </h2>
    //                             <p class="text-gray-600 text-sm">
    //                                 ${ticket.scheduled_movie_date} at ${ticket.scheduled_movie_time}
    //                             </p>
    //                         </div>

    //                         <!-- Additional Ticket Details -->
    //                         <div class="grid grid-cols-2 gap-2 text-sm text-gray-600">
    //                             <div class="flex items-center">
    //                                 <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    //                                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
    //                                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
    //                                 </svg>
    //                                 <span>${ticket.scheduled_movie_cinema_name}</span>
    //                             </div>
    //                             <div class="flex items-center">
    //                                 <svg class="w-5 h-5 mr-2 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    //                                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
    //                                 </svg>
    //                                 <span>Seat: ${ticket.seat_identifier }</span>
    //                             </div>
    //                         </div>

    //                         <!-- Action Buttons -->
    //                         <div class="flex space-x-3 mt-4 justify-between">
    //                             <button 
    //                                 class="flex-1 block w-full text-center bg-black text-white py-2 rounded-md transition duration-300">
    //                                 View Details
    //                             </button>`
    //     if(ticket.ticket_is_active){
    //         html += 
    //                 `<button
    //                     data-cancel-ticket-button
    //                     data-cancel-url="/admin/dashboard/cancel_ticket/${ticket.ticket_id}/"
    //                     class="flex-1 block w-full text-center bg-red-500 text-white py-2 rounded-md hover:bg-red-600 transition duration-300">
    //                         Cancel Ticket
    //                 </button>`
    //     }                       

    //     html +=             `</div>
    //                     </div>
    //                 </div>
    //             </div>
    //     `
    //}



    newTicketGrid.innerHTML = html;
    replaceWithGSAP(container, newTicketGrid, addListenersToCancelTicketButtons);
    displayedByText.textContent = "By All Tickets";

};


const displayByScheduledMovie = (scheduledMovies) => {
    const displayedByText = document.getElementById("displayedByText");
    const container = document.getElementById("ticketsContainer");
    const newTicketGrid = document.createElement("div");

    newTicketGrid.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 box-border";
    newTicketGrid.id = "ticketsGrid";
    let html = ``;

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
                                <h3 class="font-semibold text-xl">Scheduled Movie #${movie.scheduled_movie_id}</h3>
                            </div>
                        </div>

                        <div class="mb-4 flex items-center space-x-4">
                            <p class="text-xl font-bold text-gray-800"> ${movie.scheduled_movie_movie_name } </p>
                        </div>

                        <div class="mb-4 flex flex-row items-center gap-4">
                            <span class="${movie.scheduled_movie_is_active ? "bg-green-500" : "bg-red-500"} text-white px-3 py-1 rounded-full text-sm">
                                ${movie.scheduled_movie_is_active ? "Active" : "Inactive"}
                            </span>
                            <p class="text-sm">Available seats: ${movie.scheduled_movie_available_seats}</p>
                        </div>

                        <!--  Demarcation -->
                        <div class="border-t border-gray-300 my-2"></div>

                        <!-- Movie Details -->
                        <div class="space-y-3">
                            <div>
                                <h2 class="text-xl font-bold text-gray-800">
                                    ${movie.scheduled_movie_cinema_name}
                                </h2>
                                <p class="text-gray-600 text-sm">
                                    ${movie.scheduled_movie_date} at ${movie.scheduled_movie_time}
                                </p>
                            </div>

                            <!-- Action Buttons -->
                            <div class="flex space-x-3 mt-4 justify-between">
                                <button 
                                    class="flex-1 block w-full text-center bg-black text-white py-2 rounded-md">
                                    View Tickets
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
        `;
    }

    newTicketGrid.innerHTML = html;
    replaceWithGSAP(container, newTicketGrid);
    displayedByText.textContent = "By Scheduled Movie";
}

const displayByUsers = (users) => {
    const displayedByText = document.getElementById("displayedByText");
    const container = document.getElementById("ticketsContainer");
    const newTicketGrid = document.createElement("div");

    newTicketGrid.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 box-border";
    newTicketGrid.id = "ticketsGrid";
    let html = ``;

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
                                <h3 class="font-semibold text-xl">User #${user.user_id}</h3>
                            </div>
                        </div>

                        <!-- User Info -->
                        <div class="mb-4 flex-col items-center">
                            <p class="text-base"><span class="font-medium">Name:</span> ${user.user_first_name} ${user.user_last_name }</p>
                            <p class="text-base"><span class="font-medium">Username:</span> ${user.user_username}</p>
                            <p class="text-base"><span class="font-medium">Email:</span> ${user.user_email}</p>
                        </div>

                        <!--  Demarcation -->
                        <div class="border-t border-gray-300 my-2"></div>


                        <div class="space-y-3">
                            <div class="flex space-x-3 mt-4 justify-between">
                                <button 
                                    class="flex-1 block w-full text-center bg-black text-white py-2 rounded-md transition duration-300">
                                    View Tickets
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
        `;
    }


    newTicketGrid.innerHTML = html;
    replaceWithGSAP(container, newTicketGrid);
    displayedByText.textContent = "By Users";
};

const replaceWithGSAP = (container, newContent, callback) => {
    // Animate out current content
    gsap.to(container.children, {
        opacity: 0,
        y: 50,
        duration: 0.5,
        onComplete: () => { 
            // Clear and add new content
            container.innerHTML = '';
            container.appendChild(newContent);

            if (typeof callback === 'function') {
                callback(); 
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