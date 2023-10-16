function getTodayAndYesterday() {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  yesterday.setHours(0, 0, 0, 0);

  return { today, yesterday };
}

function dateToString(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${year}-${month}-${day}T${hours}:${minutes}`;
}


const dates = getTodayAndYesterday();

const datetimeStart = document.getElementById("start_time");
const datetimeEnd = document.getElementById("end_time");

if (!datetimeStart.value) {
  datetimeStart.value = dateToString(dates.yesterday);
}
if (!datetimeEnd.value) {
  datetimeEnd.value = dateToString(dates.today)
}


