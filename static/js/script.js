async function fetchTemperature() {
  const city = $("#citySelect").val();
  const date = $("#datePicker").val();
  if (!city || !date) return alert("Please select both city and date.");
  const res = await fetch(`/bulk/temperature?city=${city}&date=${date}`);
  const data = await res.json();
  console.log(data); // Log the response data
  if (data.error) return alert(data.error);
  alert(`Temperature in ${city} on ${date}: ${data.avg_temperature}°C`);
}
