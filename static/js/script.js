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
    <div class="autocomplete" style="width:300px;">
      <input id="skillInput" type="text" name="skillName" placeholder="skillName">
    </div>
    <input id="addSkillButton" type="submit">
  </form>
  `;

  modalContent.append(element);

  const input = document.querySelector('#skillInput'),
    formButton = document.querySelector('#addSkillButton');

  autocomplete(input);

  formButton.addEventListener('click', (e) => {
    e.preventDefault();

    const urlRequest = `${baseUrl}/findSkill?skillName=${input.value}`;
    fetch(urlRequest)
      .then(response => response.json())
      .then(skillData => {
        console.log(skillData);
        const ontology = skillData.ontology.split(',')[0].split('>');
        addSkillToChart(skillData.searchWord, ontology[1], ontology[0], skillData.type, skillData.filling);
        
        skill = {
          'name': skillData.searchWord,
          'id': skillData.type,
          'enabled': true
        };

        addSkill(skill, skillList.length);
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

//     const urlRequest = `http://localhost:5000/findSkill?findSkill=${skillName}`;
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
    <input id="cvFileInput" type="file" name="file">
    <p class="text-center">OR <br> Enter the link (hh.ru): </p>
    <input id="cvStringInput" type="text" name="link">
    <input id="cvSubmitButtonInput" type="submit" />
  </form>
  `;

  modalContent.append(element);

  // const inputFile = document.querySelector('#cvFileInput'),
  //   inputString = document.querySelector('#cvStringInput'),
  //   formButton = document.querySelector('#cvSubmitButtonInput'),
  //   urlRequest = `http://localhost:5000/uploader`;

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
  element.innerHTML = `TestEvidenceForm`;

  modalContent.append(element);
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