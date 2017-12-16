$(document).ready(function() {
  $('#weatherLocation').click(function() {
    let city = $('#location').val();
    $('#location').val("");

    let request = new XMLHttpRequest();
    let url = 'https://nominatim.openstreetmap.org/search?q=545+ticha,+novaky,+slovakia&format=json';
    //let url = `http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=[API-KEY-GOES-HERE]`;

    request.onreadystatechange = function() {
      if (this.readyState === 4 && this.status === 200) {
        let response = JSON.parse(this.responseText);
        getElements(response);
      }
    }

    request.open("GET", url, true);
    request.send();

    getElements = function(response) {
      $('.showHumidity').text(`The humidity in ${city} is ${response.main.lat}%`);
      $('.showTemp').text(`The temperature in Kelvins is ${response.main.lon} degrees.`);
    }
  });
});