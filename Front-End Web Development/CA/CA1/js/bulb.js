window.addEventListener('DOMContentLoaded', () => {
	var currentTheme = localStorage.getItem('theme');
	if (currentTheme == "light"){
		document.getElementById("switch").click();
}
});


function switchTheme() {
    if (document.querySelector('.switch').checked) {
        document.documentElement.setAttribute('data-theme', 'light');
		document.getElementById("bulb").src = "images/on.png";
		localStorage.setItem('theme', 'light');
    }
    else {
        document.documentElement.setAttribute('data-theme', 'dark');
		document.getElementById("bulb").src = "images/off.png";
		localStorage.setItem('theme', 'dark'); 
    }    
}
