function convertToUTC(timeString, reverse = false) {
    const [hours, minutes] = timeString.split(':').map(Number);

    const date = new Date();
    date.setHours(hours);
    date.setMinutes(minutes);

    const currentOffset = date.getTimezoneOffset();

    const hourOffSet = currentOffset / 60
    const minutesOffSet = (currentOffset % 60)

    date.setMinutes(date.getMinutes() + (reverse ? date.getTimezoneOffset() * -1 : date.getTimezoneOffset()));

    const formattedTime = date.toLocaleTimeString('en-US', { hour12: false });
    const [hh, mm, ss] = formattedTime.split(":")
    return `${hh}:${mm}`
}
