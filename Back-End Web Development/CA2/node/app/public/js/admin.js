$(document).ready(function() {
	fetch("/airport").then((response) => response.json()).then((airports) => {
		menuHtml = `<table class="
		table "> <thead> <tr> <th scope="
		col "></th> <th scope="
		col " style="color:white;">Name</th> <th scope="
		col " style="color:white;">Country</th> <th scope="
		col " style="color:white;">Description</th> </tr> </thead> <tbody>`;
		for (var [i, airport] of airports.entries()) {
			if (!airport.description){
				airport.description=""
			} 
			menuHtml += `<tr><th scope="row" style="color:white;">${i}</th><td style="color:white;">${airport.name}</td><td style="color:white;">${airport.country}</td><td style="color:white;">${airport.description}</td></tr>`
		}
		menuHtml += "</tbody></table>";
		document.getElementById("airports").innerHTML = menuHtml;
	});
});

$(document).ready(function() {
	fetch("/flights").then((response) => response.json()).then((flights) => {
		menuHtml = `<table class="
		table "> <thead> <tr> <th scope="
		col "></th> <th scope="
		col " style="color:white;">Flight Code</th><th scope="
		col " style="color:white;">Aircraft</th> <th scope="
		col " style="color:white;">Origin Airport</th> <th scope="
		col " style="color:white;">Destination Airport</th><th scope="
		col " style="color:white;">Embark Date</th><th scope="
		col " style="color:white;">Travel Time</th><th scope="
		col " style="color:white;">Price</th> </tr> </thead> <tbody>`;
		for (var [i, flight] of flights.entries()) {
			menuHtml += `<tr><th scope="row" style="color:white;">${i}</th><td style="color:white;">${flight.flightcode}</td><td style="color:white;">${flight.aircraft}</td><td style="color:white;">${flight.originAirport}</td><td style="color:white;">${flight.destinationAirport}</td><td style="color:white;">${flight.embarkDate}</td><td style="color:white;">${flight.travelTime}</td><td style="color:white;">${flight.price}</td></tr>`
		}
		menuHtml += "</tbody></table>";
		document.getElementById("flights").innerHTML = menuHtml;
	});
});

const airport = fetch("/airport")
  .then((response) => response.json())
  .then((airport) => {
    return airport
 });

const changeorig = async (airportid) => {
	var airports = await airport;
	changeorigid = airportid
	airport_name = airports[airportid-1].name
	document.getElementById("Flight0").innerHTML = airport_name;
}

const changedest = async (airportid) => {
	var airports = await airport;
	changedestid = airportid
	airport_name = airports[airportid-1].name
	document.getElementById("Flight1").innerHTML = airport_name;
}

const dropdown = async () => {
  var airports = await airport;
  var menuHtml = '<span class="dropdown"><a href="#" class="dropdown-toggle btn btn-default" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">From <span class="caret"></span><span id="Flight0"></span></a><ul class="dropdown-menu" style="overflow-y:scroll;height:300px;">';
  for (i = 0; i < airports.length; i++) {
    menu = ( '<li><a onclick="changeorig(' + airports[i].airportid + ')" href="javascript:void(0)">' + airports[i].name + '</a></li>');
	menuHtml += menu;
  }
  menuHtml += '</ul></span>';
  document.getElementById("To").innerHTML = menuHtml;
}

const dropdown1 = async () => {
  var airports = await airport;
  var menuHtml = '<span class="dropdown"><a href="#" class="dropdown-toggle btn btn-default" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">To <span class="caret"></span><span id="Flight1"></span></a><ul class="dropdown-menu" style="overflow-y:scroll;height:300px;">';
  for (i = 0; i < airports.length; i++) {
    menuHtml += '<li><a onclick="changedest('+airports[i].airportid+')" href="javascript:void(0)">' + airports[i].name + '</a></li>';
  }
  menuHtml += '</ul></span>';
  document.getElementById("From").innerHTML = menuHtml;
}

var changeorigid = ""
var changedestid = ""

document.addEventListener("DOMContentLoaded", function(event){
  dropdown();
  dropdown1();
});