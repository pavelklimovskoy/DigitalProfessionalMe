const baseUrl = `${document.location.protocol}//${document.location.host}`;

function specializationsInput() {
	const input = document.querySelector('#specializationInput'),
		formButton = document.querySelector('#addSkillButton');

	autocompleteInput(input, 'jobInputAutocomplete', 'jobName');
	// autocompleteInput(input, 'translatedSkillInputAutocomplete', 'skillName');

	formButton.addEventListener('click', (e) => {
		e.preventDefault();

		// postData(`${baseUrl}/findSkill`, { skill: input.value })
		// 	.then(response => {
		// 		return response.json();
		// 	})
		// 	.then(skillData => {

		// 		closeModal();
		// 	});
	});
}

function skillInput() {
	const input = document.querySelector('#skillInput'),
		formButton = document.querySelector('#addSkillButton'),
		skillStack = document.querySelector('#skillStack');

	autocompleteInput(input, 'skillInputAutocomplete', 'skillName');


	formButton.addEventListener('click', (e) => {
		e.preventDefault();

		if (input.value != "") {
			const skillElement = document.createElement("li");
			skillElement.classList.add("list-group-item");
			skillElement.innerHTML = input.value;

			skillStack.append(skillElement);
		}

		input.value = "";
	});
}

function getAdminData() {
	let cardGroup = document.querySelector('#uniList');
	let uniInfo = document.querySelector('#uniInfo');
	res = getData('getAdminPanelData');
	res.then(res => {
		console.log(res);
		let i = 1;
		res.forEach(element => {
			console.log(element);
			let uniCard = document.createElement('div');
			uniCard.innerHTML = `
				
                    <img src="../static/icons/${element.logo}" class="card-img-top" alt="...">
                    <div class="card-body">
                      <h5 class="card-title">${element.name}</h5>
                      <p class="card-text">${element.description}</p>
                      <a id="buttonUni${i}" href="#" class="btn btn-primary">Отобразить</a>
                    </div>
                
			`;

			uniCard.classList.add('card');
			uniCard.style.width = '18rem';
			cardGroup.append(uniCard);

			let curBtn = document.querySelector(`#buttonUni${i}`);
			console.log(curBtn);
			curBtn.addEventListener('click', () => {
				cardGroup.style.display = 'none';
				uniInfo.style.display = 'block';
				console.log(element.specializations);

				let pivot = new WebDataRocks({
					container: "#wdr-component",
					toolbar: true,
					report: {
						dataSource: {
							//filename: "https://docs.google.com/spreadsheets/d/e/2PACX-1vQZ1gSS4Ko5StitrMIrojG7P5ohqfHtusH2gapZZDRtbukPMiY4bgPHqlNsSYy1hf-XlHWZWwTsyTQ1/pub?gid=0&single=true&output=csv"
							"data": element.programs
							//filename: `${element.data}`
							//filename: "https://docs.google.com/spreadsheets/d/e/2PACX-1vQZ1gSS4Ko5StitrMIrojG7P5ohqfHtusH2gapZZDRtbukPMiY4bgPHqlNsSYy1hf-XlHWZWwTsyTQ1/pubhtml"
						}
					}
				});


				//let dataUni = postData(`getUniData`, { dataname: element.data });

				//dataUni.then(uniResp => {
				//	console.log(uniResp);

				//});

				// let pivot = new WebDataRocks({
				// 	container: "#wdr-component",
				// 	toolbar: true,
				// 	report: {
				// 		dataSource: {
				// 			//filename: "https://docs.google.com/spreadsheets/d/e/2PACX-1vQZ1gSS4Ko5StitrMIrojG7P5ohqfHtusH2gapZZDRtbukPMiY4bgPHqlNsSYy1hf-XlHWZWwTsyTQ1/pub?gid=0&single=true&output=csv"
				// 			"data":
				// 			//filename: `${element.data}`
				// 			//filename: "https://docs.google.com/spreadsheets/d/e/2PACX-1vQZ1gSS4Ko5StitrMIrojG7P5ohqfHtusH2gapZZDRtbukPMiY4bgPHqlNsSYy1hf-XlHWZWwTsyTQ1/pubhtml"
				// 		}
				// 	}
				// });
			});



			i++;
		});
		// datalistUnivers = document.querySelector('#datalistUnivers');
		// datalistSpecs = document.querySelector('#datalistSpecs');
		// datalistStandarts = document.querySelector('#datalistOptionsStandarts');

		// res.Universities.forEach(uni => {
		// 	e = document.createElement('option');
		// 	e.value = uni;
		// 	datalistUnivers.append(e);
		// });

		// res.Specialization.forEach(spec => {
		// 	e = document.createElement('option');
		// 	e.value = spec;
		// 	datalistSpecs.append(e);
		// });

		// res.Standarts.forEach(std => {
		// 	e = document.createElement('option');
		// 	e.value = std;
		// 	datalistStandarts.append(e);
		// });

		// console.log(document.querySelector('#datalistUnivers'));
	});
}

skillInput();
specializationsInput();
getAdminData();



// Асинхронный POST запрос c jsonData
async function postData(url = '', data = {}) {
	const response = await fetch(url, {
		method: 'POST',
		mode: 'cors',
		cache: 'no-cache',
		credentials: 'same-origin',
		headers: {
			'Content-Type': 'application/json'
		},
		redirect: 'follow',
		referrerPolicy: 'no-referrer',
		body: JSON.stringify(data)
	});
	return response;
}

// Асинхронный POST запрос c формой
async function postFormData(url = '', data = {}) {
	let formData = new FormData();
	console.log(data);
	if (data.queryURL != '') {
		formData.append('link', data.queryURL);
		formData.append('file', '');
	}
	else {
		formData.append('link', '');
		formData.append('file', data.file);
	}
	console.log(formData);

	const response = await fetch(url, {
		method: 'POST',
		body: formData
	});
	return response;
}

// Асинхронный GET запрос
async function getData(url = '') {
	const response = await fetch(`${baseUrl}/${url}`);
	const data = await response.json();
	return data;
}