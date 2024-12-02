function showNotification(message, type = "error") {
  // Create notification element
  const notification = document.createElement("div");
  notification.className = `notification ${type}`;
  notification.innerHTML = `
        <div>
            <strong>${
              type.charAt(0).toUpperCase() + type.slice(1)
            }:</strong> ${message}
            <button class="notification-close" onclick="closeNotification(this)">×</button>
        </div>
    `;

  // Add to container
  const container = document.getElementById("notification-container");
  container.appendChild(notification);

  // GSAP Animation for entry
  gsap.fromTo(
    notification,
    { opacity: 0, x: 100 },
    {
      opacity: 1,
      x: 0,
      duration: 0.5,
      ease: "power2.out",
    }
  );

  // Auto-remove after 5 seconds
  setTimeout(() => {
    closeNotification(notification.querySelector(".notification-close"));
  }, 5000);
}

function closeNotification(closeButton) {
  const notification = closeButton.closest(".notification");

  // GSAP Animation for exit
  gsap.to(notification, {
    opacity: 0,
    x: 100,
    duration: 0.5,
    ease: "power2.in",
    onComplete: () => {
      notification.remove();
    },
  });
}
