const airport = fetch("/airport")
  .then((response) => response.json())
  .then((airport) => {
    return airport
 });
 
function modaling(id){
	var modal = document.getElementById(`myModal${id}`);
	var btn = document.getElementById(`myBtn${id}`);
	var span = document.getElementById(`close${id}`);


	btn.onclick = function() {
	  modal.style.display = "block";
	}

	span.onclick = function() {
	  modal.style.display = "none";
	}

	window.onclick = function(event) {
	  if (event.target == modal) {
		modal.style.display = "none";	  
	  }
	}
}
 
function search(){
  fetch(`/flightDirect/${changeorigid}/${changedestid}`)
  .then((response) => response.json())
  .then((possibleFlights) => {
	if (possibleFlights.length){
		var menuHtml = ""
		var filteredPossibleFlights = []
		var dateFilter = document.getElementById('date').value;
		var returnDate = document.getElementById('date1').value;
		if (dateFilter == ""){
			dateFilter = String(Date())
		}
		for ([i, flight] of Object.entries(possibleFlights)){
			if(!(new Date(dateFilter) >= new Date(flight.embarkDate))){
				filteredPossibleFlights.push(flight)
			}
		}
		for ([i, flight] of Object.entries(filteredPossibleFlights)){
			var templateHtml = `<div class="container flight"> <div class="form-row"> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.travelTime} </a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a></a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.price} </a> </div> </div> <div class="form-row"> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.originAirport} </a> </div> <div class="form-check col-lg-1 col-md-6 col-sm-12 pl-4"> <a> -></a> </div> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.destinationAirport} </a> </div> <div class="form-check col-lg-3 col-md-6 col-sm-12 pl-4"> <a id="myBtn${i}" onclick="modaling(${i})" href="javascript:void(0)"> More Details </a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.embarkDate} </a> </div> </div> <div id="myModal${i}" class="modal"><div class="modal-content"> <span class="close" id="close${i}">&times;</span> <p> Flight Code: ${flight.flightcode}<br> Aircraft: ${flight.aircraft}<br> Origin Airport: ${flight.originAirport}<br> Destination Airport: ${flight.destinationAirport}<br> Embark Date: ${flight.embarkDate}<br> Travel Time: ${flight.travelTime}<br> Price: ${flight.price} </p> </div> </div> </div>`;
			menuHtml += templateHtml
		}
		if (returnDate != ""){
			menuHtml += `<section class="return" id="return"> <h1>Return</h1> </section>`
			fetch(`/flightDirect/${changedestid}/${changeorigid}`)
			.then((response) => response.json())
			.then((possibleFlights) => {
					if (possibleFlights.length){
					var filteredPossibleFlights = []
					if (returnDate == ""){
						returnDate = String(Date())
					}
					for ([i, flight] of Object.entries(possibleFlights)){
						if(!(new Date(returnDate) >= new Date(flight.embarkDate))){
							filteredPossibleFlights.push(flight)
						}
					}
					for ([i, flight] of Object.entries(filteredPossibleFlights)){
						var templateHtml = `<div class="container flight"> <div class="form-row"> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.travelTime} </a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a></a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.price} </a> </div> </div> <div class="form-row"> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.originAirport} </a> </div> <div class="form-check col-lg-1 col-md-6 col-sm-12 pl-4"> <a> -></a> </div> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.destinationAirport} </a> </div> <div class="form-check col-lg-3 col-md-6 col-sm-12 pl-4"> <a id="myBtn${i}" onclick="modaling(${i})" href="javascript:void(0)"> More Details </a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.embarkDate} </a> </div> </div> <div id="myModal${i}" class="modal"><div class="modal-content"> <span class="close" id="close${i}">&times;</span> <p> Flight Code: ${flight.flightcode}<br> Aircraft: ${flight.aircraft}<br> Origin Airport: ${flight.originAirport}<br> Destination Airport: ${flight.destinationAirport}<br> Embark Date: ${flight.embarkDate}<br> Travel Time: ${flight.travelTime}<br> Price: ${flight.price} </p> </div> </div> </div>`;
						menuHtml += templateHtml
						document.getElementById("flights").innerHTML = menuHtml;
					}
				}
				else{
					document.getElementById("flights").innerHTML = menuHtml+`<div class="container" ><a style="color:white;"> No Return Flights Found. </a></div>`;
				}
			});
		}
		else{
			document.getElementById("flights").innerHTML = menuHtml;
		}
	}
	else{
		fetch(`/transfer/flight/${changeorigid}/${changedestid}`)
		.then((response) => response.json())
		.then((transferFlights) => {
			if (transferFlights.length){
				var menuHtml = ""
				var filteredTransferFlights = []
				var dateFilter = document.getElementById('date').value;
				var returnDate = document.getElementById('date1').value;
				if (dateFilter == ""){
					dateFilter = String(Date())
				}
				for ([i, flight] of Object.entries(transferFlights)){
					if(!(new Date(dateFilter) >= new Date(flight.embarkDate1))){
						filteredTransferFlights.push(flight)
					}
				}
				for ([i, flight] of Object.entries(filteredTransferFlights)){
					var templateHtml = `<div class="container flight"> <div class="form-row"> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> First Flight: ${flight.travelTime1} </a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> Second Flight: ${flight.travelTime2} </a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight['Total price']} </a> </div> </div> <div class="form-row"> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.originAirport} </a> </div> <div class="form-check col-lg-1 col-md-6 col-sm-12 pl-4"> <a> -></a> </div> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.transferAirport} </a> </div> <div class="form-check col-lg-3 col-md-6 col-sm-12 pl-4"> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.embarkDate1} </a> </div> </div> <div class="form-row"> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.transferAirport} </a> </div> <div class="form-check col-lg-1 col-md-6 col-sm-12 pl-4"> <a> -></a> </div> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.destinationAirport} </a> </div> <div class="form-check col-lg-3 col-md-6 col-sm-12 pl-4"> <a id="myBtn${i}" onclick="modaling(${i})" href="javascript:void(0)"> More Details </a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.embarkDate2} </a> </div> </div> <div id="myModal${i}" class="modal"> <div class="modal-content"> <span class="close" id="close${i}">&times;</span> <p> Flight Code 1: ${flight.flightCode1} <br> Flight Code 2: ${flight.flightCode2} <br> Aircraft 1: ${flight.aircraft1} <br> Aircraft 2: ${flight.aircraft2} <br> Origin Airport: ${flight.originAirport} <br> Transfer Airport: ${flight.transferAirport}  <br> Destination Airport: ${flight.destinationAirport} <br> Embark Date 1: ${flight.embarkDate1} <br> Embark Date 2: ${flight.embarkDate2} <br> Travel Time 1: ${flight.travelTime1} <br> Travel Time 2: ${flight.travelTime2} <br> Price: ${flight['Total price']} </p> </div> </div> </div>`;
					menuHtml += templateHtml
				}
				if (returnDate != ""){
					menuHtml += `<section class="return" id="return"> <h1>Return</h1> </section>`
					fetch(`/transfer/flight/${changedestid}/${changeorigid}`)
					.then((response) => response.json())
					.then((transferFlights) => {
						if (transferFlights.length){
							var filteredTransferFlights = []
							if (returnDate == ""){
								returnDate = String(Date())
							}
							for ([i, flight] of Object.entries(transferFlights)){
								if(!(new Date(returnDate) >= new Date(flight.embarkDate))){
									filteredTransferFlights.push(flight)
								}
							}
							for ([i, flight] of Object.entries(filteredTransferFlights)){
								var templateHtml = `<div class="container flight"> <div class="form-row"> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.travelTime} </a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a></a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.price} </a> </div> </div> <div class="form-row"> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.originAirport} </a> </div> <div class="form-check col-lg-1 col-md-6 col-sm-12 pl-4"> <a> -></a> </div> <div class="form-check col-lg-2 col-md-6 col-sm-12 pl-4"> <a> ${flight.destinationAirport} </a> </div> <div class="form-check col-lg-3 col-md-6 col-sm-12 pl-4"> <a id="myBtn${i}" onclick="modaling(${i})" href="javascript:void(0)"> More Details </a> </div> <div class="form-check col-lg-4 col-md-6 col-sm-12 pl-4"> <a> ${flight.embarkDate} </a> </div> </div> <div id="myModal${i}" class="modal"><div class="modal-content"> <span class="close" id="close${i}">&times;</span> <p> Flight Code: ${flight.flightcode}<br> Aircraft: ${flight.aircraft}<br> Origin Airport: ${flight.originAirport}<br> Destination Airport: ${flight.destinationAirport}<br> Embark Date: ${flight.embarkDate}<br> Travel Time: ${flight.travelTime}<br> Price: ${flight.price} </p> </div> </div> </div>`;
								menuHtml += templateHtml
								document.getElementById("flights").innerHTML = menuHtml;
							}
						}
						else{
							document.getElementById("flights").innerHTML = menuHtml+`<div class="container" ><a style="color:white;"> No Return Flights Found. </a></div>`;
						}
					});
				}
				else{
					document.getElementById("flights").innerHTML = menuHtml;
				}
			}
			else{
				document.getElementById("flights").innerHTML = `<div class="container" ><a style="color:white;"> No Flights Found. </a></div>`;
			}
	})}
})};
 
const changeorig = async (airportid) => {
	var airports = await airport;
	changeorigid = airportid
	airport_name = airports[airportid-1].name
	document.getElementById("Airport").innerHTML = airport_name;
}

const changedest = async (airportid) => {
	var airports = await airport;
	changedestid = airportid
	airport_name = airports[airportid-1].name
	document.getElementById("Airport1").innerHTML = airport_name;
}

const dropdown = async () => {
  var airports = await airport;
  var menuHtml = '<span class="dropdown"><a href="#" class="dropdown-toggle btn btn-default" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">From <span class="caret"></span><span id="Airport"></span></a><ul class="dropdown-menu" style="overflow-y:scroll;height:300px;">';
  for (i = 0; i < airports.length; i++) {
    menu = ( '<li><a onclick="changeorig(' + airports[i].airportid + ')" href="javascript:void(0)">' + airports[i].name + '</a></li>');
	menuHtml += menu;
  }
  menuHtml += '</ul></span>';
  document.getElementById("flightOrigin").innerHTML = menuHtml;
}

const dropdown1 = async () => {
  var airports = await airport;
  var menuHtml = '<span class="dropdown"><a href="#" class="dropdown-toggle btn btn-default" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">To <span class="caret"></span><span id="Airport1"></span></a><ul class="dropdown-menu" style="overflow-y:scroll;height:300px;">';
  for (i = 0; i < airports.length; i++) {
    menuHtml += '<li><a onclick="changedest('+airports[i].airportid+')" href="javascript:void(0)">' + airports[i].name + '</a></li>';
  }
  menuHtml += '</ul></span>';
  document.getElementById("flightDestination").innerHTML = menuHtml;
}

var changeorigid = ""
var changedestid = ""

document.addEventListener("DOMContentLoaded", function(event){
  dropdown();
  dropdown1();
});