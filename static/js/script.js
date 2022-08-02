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
  <form id="addSkillButton" autocomplete="off" action="http://localhost:5000/findSkill">
    <div class="autocomplete" style="width:300px;">
      <input id="myInput" type="text" name="skillName" placeholder="skillName">
    </div>
    <input type="submit">
  </form>
  `;

  modalContent.append(element);

  autocomplete(document.getElementById("myInput"));

  const form = document.querySelector('#addSkillButton');

  form.addEventListener('click', (e) => {
    e.preventDefault();
    console.log(e);

    const urlRequest = `http://localhost:5000/findSkill?findSkill=${skillName}`;
    fetch(urlRequest)
      .then(response => response.json())
      .then(data => {
        console.log(data);
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

  const element = document.createElement('div');
  element.innerHTML = `
  <span data-close class="close">&times;</span>
  <form action="http://localhost:5000/uploader" method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <p class="text-center">OR <br> Enter the link (hh.ru): </p>
    <input type="text" name="link">
    <input type="submit" />
  </form>
  `;

  modalContent.append(element);
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