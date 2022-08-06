const baseUrl = 'http://localhost:5000'

//Modal

const modalTrigger = document.querySelectorAll('[data-modal]'),
  modal = document.querySelector('.modal'),
  modalContent = document.querySelector('.modal-content');

// Функция закрытия модального окна 
function closeModal() {
  modal.style.display = 'none';
  document.body.style.overflow = '';
}

// Функция открытия модального окна 
function openModal(e) {
  const eId = e.target.id;
  if (eId == 'parseCV') {
    createModalCv();
  } else if (eId == 'parseEvidence') {
    createModalEvidence();
  } else if (eId == 'addSkill') {
    createModalAddingSkill();
  } else if (eId == 'addGoal') {
    createModalGoal();
  }

  modal.style.display = 'block';
  document.body.style.overflow = 'hidden';
}

function createModalAddingSkill() {
  modalContent.innerHTML = '';

  const element = document.createElement('div');
  element.innerHTML = `
  <span data-close class="close">&times;</span>
  <form autocomplete="off" action="#">
    <div style="width:300px;">
      <input id="skillInput" type="text" name="skillName" placeholder="skillName">
    </div>
    <input id="addSkillButton" type="submit">
  </form>
  `;

  modalContent.append(element);

  const input = document.querySelector('#skillInput'),
    formButton = document.querySelector('#addSkillButton');

  autocomplete(input, 'skillInputAutocomplete', 'skillName');

  formButton.addEventListener('click', (e) => {
    e.preventDefault();

    const urlRequest = `${baseUrl}/findSkill?skillName=${input.value}`;
    fetch(urlRequest)
      .then(response => response.json())
      .then(skillData => {
        console.log(skillData);
        const ontology = skillData.ontology.split(',')[0].split('>');
        let skill = addSkillToChart(skillData.searchWord, ontology[1], ontology[0], skillData.type, skillData.filling);

        // skill = {
        //   'name': skillData.searchWord,
        //   'id': skillData.type,
        //   'enabled': true
        // };

        addSkill(skill, skillList.length);
        closeModal();
      });
  });
}

function createModalGoal() {
  modalContent.innerHTML = '';
  //Дата, Название J
  console.log('132');
  const element = document.createElement('div');
  element.innerHTML = `
  <span data-close class="close">&times;</span>
  <form autocomplete="off" action="#">
    <div>
      <input id="goalJDInput" type="text" name="jobName" placeholder="jobName">
      <input id="goalDateInput" type="date" name="dateJd" placeholder="dateJd" min="2022-01-01" max="2050-01-01">
    </div>
    <input id="submitGoalForm" type="submit" onclick=addLifeGoal()>
  </form>
  `;

  modalContent.append(element);

  const input = document.querySelector('#goalJDInput'),
    dateInput = document.querySelector('#goalDateInput'),
    formButton = document.querySelector('#submitGoalForm');

  autocomplete(input, 'jobInputAutocomplete', 'jobName');

  formButton.addEventListener('click', (e) => {
    e.preventDefault();

    const urlRequest = `${baseUrl}/findJob?jobName=${input.value}&deadline=${dateInput.value}`;
    fetch(urlRequest)
      .then(response => response.json())
      .then(data => {
        console.log('JD', data);

        modalContent.innerHTML = '';

        const element = document.createElement('div');
        const courses = data.offeredCourses;

        for (let i = 0; i < courses.length; i++) {
          if (i <= 3) {
            const courseCard = document.createElement('div');
            skillReqStr = ``;

            for (let i = 0; i < data.gapSkills.length; i++) {
              skillReqStr += `${data.gapSkills[i]}, `;
              if (i >= 9) {
                break;
              }
            }

            skillGetStr = ``;

            for (let i = 0; i < courses[i].courseName.skills.length; i++) {
              skillReqStr += `${courses[i].courseName.skills[i]}, `;
            }

            courseCard.innerHTML = `
            <div class="container"> 
              <div class="container__text">
                <h1>${courses[i].courseName.name}</h1>
                <p>
                It seems you lack these skills:${skillReqStr})
                </p>
                <div class="container__text__timing">
                  <div class="container__text__timing_time">
                    <h2>Get Skills</h2>
                    <a>${skillGetStr}</a>
                  </div>
                  
                  <div class="container__text__timing_time">
                    <h2>Link</h2>
                    <a>${courses[i].courseName.url}</a>
                  </div>

                </div>
            </div>
            `;
          }
        }

        closeModal();
      });
  });
}


// function addSkillOnChart(skillName) {
//   const form = document.querySelector('#addSkillButton');

//   form.addEventListener('click', (e) => {
//     e.preventDefault();
//     //form.children();
//     console.log(skillName);

//     const urlRequest = `http://${baseUrl}/findSkill?findSkill=${skillName}`;
//     fetch(urlRequest)
//       .then(response => response.json())
//       .then(data => {
//         console.log(data);
//       });
//   });
// }

function createModalCv() {
  modalContent.innerHTML = '';
  console.log(disabledSkills);
  console.log(dataTree);

  const element = document.createElement('div');
  element.innerHTML = `
  <span data-close class="close">&times;</span>
  <form action="${baseUrl}/uploader" method="POST" enctype="multipart/form-data">
    <input id="cvFileInput" type="file" name="file" onchange="this.form.submit()">
    <p class="text-center">OR <br> Enter the link (hh.ru): </p>
    <input id="cvStringInput" type="text" name="link">
    <input id="cvSubmitButtonInput" type="submit" />
  </form>
  `;

  modalContent.append(element);

  // const inputFile = document.querySelector('#cvFileInput'),
  //   inputString = document.querySelector('#cvStringInput'),
  //   formButton = document.querySelector('#cvSubmitButtonInput'),
  //   urlRequest = `http://digitalprofessional.me:5000/uploader`;

  // formButton.addEventListener('click', (e) => {
  //   e.preventDefault();
  //   let data;
  //   if (inputFile.files.length && !inputString.value) {
  //     data = inputFile.files[0];
  //   } else {
  //     data = inputString.value;
  //   }

  //   fetch(urlRequest, {
  //     method: 'POST',
  //     body: data
  //   });
  // });
}

function createModalEvidence() {
  modalContent.innerHTML = '';

  const element = document.createElement('div');
  element.innerHTML = `
  <span data-close class="close">&times;</span>
  <form autocomplete="off" action="#">
    <div style="width:300px;">
      <input id="evidenceInput" type="text" name="evidenceInput" placeholder="url for coursera">
    </div>
    <input id="parseCertificateButton" type="submit">
  </form>
  `;

  modalContent.append(element);

  console.log(element);
  const input = document.querySelector('#evidenceInput'),
    formButton = document.querySelector('#parseCertificateButton');
  console.log(formButton);
  formButton.addEventListener('click', (e) => {
    e.preventDefault();

    const urlRequest = `${baseUrl}/parseCertificate?url=${input.value}`;
    fetch(urlRequest)
      .then(response => response.json())
      .then(ceritificateData => {
        console.log(ceritificateData);

        addCerificate(ceritificateData);

        closeModal();
      });
  });

}

modalTrigger.forEach(item => {
  item.addEventListener('click', openModal);
});

// Закрытие модального окна по клику за его область
modal.addEventListener('click', (e) => {
  if (e.target === modal || e.target.getAttribute('data-close') == '') {
    closeModal();
  }
});


// Закрытие модального окна по клику на ESC
document.addEventListener('keydown', (e) => {
  if (e.code === 'Escape' && modal.style.display == 'block') {
    closeModal();
  }
});
