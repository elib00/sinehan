export const formatBirthdateToMMDDYYYY = (birthdateStr) => {
    const date = new Date(birthdateStr); // Convert to Date object
    const month = String(date.getMonth()).padStart(2, '0'); // Get month and pad with zero
    const day = String(date.getDate()).padStart(2, '0'); // Get day and pad with zero
    const year = date.getFullYear(); // Get full year
    return new Date(Date.UTC(year, month, day))
}