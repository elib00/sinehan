//main
document.addEventListener("DOMContentLoaded", () => {
    const data = JSON.parse(document.getElementById('displayData').textContent);

    const scheduledMovies = data.scheduledMovies;
    for(let m of scheduledMovies) {
        console.log(m);
    }
    initializeTicketsDisplayOptionsDropdown();
});

//helpers
const initializeTicketsDisplayOptionsDropdown = () => {
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
        displayAllTickets();
    });

    scheduledMovieChoice.addEventListener("click", () => {
        const container = document.getElementById("ticketsContainer");
        const newDiv = document.createElement("div");
        replaceWithGSAP(container, newDiv);
    });
    
};

const displayAllTickets = () => {

};

const replaceWithGSAP = (container, newContent) => {
    // Animate out current content
    gsap.to(container.children, {
        opacity: 0,
        y: 50,
        duration: 0.5,
        onComplete: () => { 
            // Clear and add new content
            container.innerHTML = '';
            container.appendChild(newContent);
            
            // Animate in new content
            gsap.from(container.children, {
                opacity: 0,
                y: -50,
                duration: 0.5
            });
        }
    });
}