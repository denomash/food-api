
const reg = document.getElementById('regform');

function register(e) {
	e.preventDefault();

	let username = document.getElementById('username').value;
	let email = document.getElementById('email').value;
	let password = document.getElementById('password').value;
	let confirm_password = document.getElementById('confirm_password').value;

	var myHeaders = new Headers({
	'Content-Type': 'application/json'
	});
	var myInit = {
		'method': 'POST',
	    'headers': myHeaders,
	    'body': JSON.stringify({username:username, email:email, password:password, confirm_password:confirm_password})
	};

	var myRequest = new Request('http://localhost:5000/api/v2/auth/signup');

	fetch(myRequest, myInit)
	.then((res) => res.json())
	.then((data) => {
		console.log(data);
		alert('Register successfull')
	})
}

reg.addEventListener('submit', register)