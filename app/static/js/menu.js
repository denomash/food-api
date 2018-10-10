

var myHeaders = new Headers({
    'Content-Type': 'application/json'
});
var myInit = { method: 'GET',
               headers: myHeaders,
               mode: 'cors',
               cache: 'default' };


var myRequest = new Request('http://localhost:5000/api/v2/menu');
fetch(myRequest,myInit)
.then((resp) =>	resp.json())
.then((data) => {
	let meals = data.Meals
	console.log(meals)
	let output = ''
	
	meals.forEach((meal) => {
		output += `
			<div class="card">
			<img src="${meal.image}">
			<h3>${meal.food}</h3>
			<p>Ksh ${meal.price}</p>
			<button onclick="location.href="{{ url_for('processing') }}";">Order</button>
			</div>
		`;
	});
	document.getElementById('menu').innerHTML = output;
})