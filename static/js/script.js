window.onload = function () {
  window.sp = new SuperParticles({
    container: {
      element: "#particles-js"
    }
  });
};

const baseUrl = `http://${document.location.host}`;
try{ 
  document.querySelector('#avatar_upload').setAttribute('action', `${baseUrl}/upload_avatar`);
}
catch {
  console.log('no avatar');
}

// Feedback form
document.querySelector('#feedbackFormButton').addEventListener('click', (e) => {
  e.preventDefault();

  let email = document.querySelector('#exampleInputEmail').value,
    name = document.querySelector('#exampleInputName').value,
    urlRequest = `digitalprofessional.me:5000/about`;

  console.log(urlRequest);
  postData(urlRequest, { email: email, name: name })
    .then(response => {
      document.querySelector('#feebdackForm').reset();
      console.log(response);
      return response.json();
    })
});

//Modal
const modalTrigger = document.querySelectorAll('[data-modal]'),
  modal = document.querySelector('.modal'),
  modalContent = document.querySelector('.modal-content');

// Функция закрытия модального окна 
function closeModal() {
  modal.style.display = 'none';
  document.body.style.overflow = 'visible';
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

// Создание модального окна для добавления скилла
function createModalAddingSkill() {
  modalContent.innerHTML = '';

  const element = document.createElement('div');

  element.innerHTML = `
  <span data-close class="close">&times;</span>
  <form autocomplete="off" action="#">
    <input style="width: 20rem" class="text-center" id="skillInput" type="text" name="skillName" placeholder="skillName">
    <br>
    <br>
    <input class="btn btn-primary row text-center" id="addSkillButton" type="submit" />
  </form>
  `;
  element.classList.add('text-center');
  // modalContent.innerHTML = '';

  // const element = document.createElement('div');
  // element.innerHTML = `
  // <span data-close class="close">&times;</span>
  // <form autocomplete="off" action="#">
  //   <div style="width:300px;">
  //     <input id="skillInput" type="text" name="skillName" placeholder="skillName">
  //   </div>
  //   <input id="addSkillButton" type="submit">
  // </form>
  // `;
  // element.classList.add('text-center');

  modalContent.append(element);

  const input = document.querySelector('#skillInput'),
    formButton = document.querySelector('#addSkillButton');

  autocomplete(input, 'skillInputAutocomplete', 'skillName');

  formButton.addEventListener('click', (e) => {
    e.preventDefault();

    postData(`${baseUrl}/findSkill`, { skill: input.value })
      .then(response => {
        console.log(response);
        return response.json();
      })
      .then(skillData => {
        console.log('op', skillData);
        const ontology = skillData.ontology.split('>');
        let skill = addSkillToChart(ontology[ontology.length - 1], ontology[1], ontology[0], skillData.type, skillData.filling);

        addSkill(skill, skillList.length);
        closeModal();
      });



    // const urlRequest = `${baseUrl}/findSkill?skillName=${input.value}`;
    // fetch(urlRequest)
    //   .then(response => response.json())
    //   .then(skillData => {
    //     const ontology = skillData.ontology.split(',')[0].split('>');
    //     let skill = addSkillToChart(skillData.searchWord, ontology[1], ontology[0], skillData.type, skillData.filling);

    //     // skill = {
    //     //   'name': skillData.searchWord,
    //     //   'id': skillData.type,
    //     //   'enabled': true
    //     // };

    //     addSkill(skill, skillList.length);
    //     closeModal();
    //   });
  });
}

// Создание модального окна для добавления цели
function createModalGoal() {
  modalContent.innerHTML = '';
  const element = document.createElement('div');

  element.innerHTML = `
  <span data-close class="close">&times;</span>
  <form autocomplete="off" action="#">
    <div>
      <input id="goalJDInput" type="text" name="jobName" placeholder="jobName">
      <input id="goalDateInput" type="date" name="dateJd" placeholder="dateJd" min="2022-01-01" max="2050-01-01">
    </div>
    <br>
    <input class="btn btn-primary row text-center" id="submitGoalForm" type="submit" onclick=addLifeGoal()>
  </form>
  <br>
  <form autocomplete="off" action="#">
    <label for="showJobsOptions">Показать подходящие курсы</label>
    <br>
    <input class="btn btn-primary row text-center" id="showJobsOptions" type="submit">
  </form>
  `;

  element.classList.add('text-center');

  modalContent.append(element);

  const input = document.querySelector('#goalJDInput'),
    dateInput = document.querySelector('#goalDateInput'),
    formButton = document.querySelector('#submitGoalForm'),
    jobOptionsButton = document.querySelector('#showJobsOptions');

  autocomplete(input, 'jobInputAutocomplete', 'jobName');

  jobOptionsButton.addEventListener('click', (e) => {
    e.preventDefault();

    const urlRequest = `${baseUrl}/findJobsOptions`;
    fetch(urlRequest)
      .then(response => response.json())
      .then(data => {
        showRelatedCourses(data, data.matchedJob);
      });
  });

  formButton.addEventListener('click', (e) => {
    e.preventDefault();

    postData(`${baseUrl}/findJob`, { jobName: input.value, deadline: dateInput.value })
      .then(response => {
        console.log(response);
        return response.json();
      })
      .then(data => {
        showRelatedCourses(data);
        // console.log('JD', data);
        // modalContent.innerHTML = '';

        // let gapSkills = [],
        //   relatedCourses = [];
        // data.offeredCourses.forEach(course => {
        //   course.gapSkills.forEach(skill => {
        //     if (!(gapSkills.includes(skill)) && !(relatedCourses.includes(course.courseData)) && relatedCourses.length < 4) {
        //       gapSkills.push(skill)
        //       relatedCourses.push(course.courseData);
        //     }
        //   })
        // });

        // console.log(gapSkills);
        // console.log(relatedCourses);

        // modalContent.style = 'width: 100% !important';

        // const rowForCards = document.createElement('div');
        // rowForCards.classList.add('row');
        // modalContent.append(rowForCards);

        // relatedCourses.forEach((course, i) => {
        //   const courseCard = document.createElement('div');
        //   courseCard.innerHTML = `
        //   <div class="card text-center" style="width: 18rem;">
        //     <img class="card-img-top" src="../static/icons/coursera.jpg" alt="Coursera logo image">
        //       <div class="card-body">
        //         <a href="${course.url}"><h5 class="card-title">${course.name}</h5></a>
        //         <!-- <p class="card-text">Описание курса</p> -->
        //       </div>
        //       <ul class="list-group list-group-flush" id="courseSkillBlock-${i}">
        //       </ul>
        //       <div class="card-body" id="card-footer-${i}">
        //         <!-- <a href="${course.url}" class="card-link">Ссылка на курс</a> -->
        //         <input class="btn btn-primary row text-center" id="addCourseToTimeline-${i}" type="submit" value="Добавить на timeline">
        //         </div>
        //   </div>
        //   `;
        //   courseCard.classList.add('col-3');
        //   rowForCards.append(courseCard);

        //   course.skills.forEach((skill, j) => {
        //     if (j < 5) {
        //       const skillItem = document.createElement('li');
        //       skillItem.classList.add('list-group-item');
        //       skillItem.textContent = skill;

        //       document.querySelector(`#courseSkillBlock-${i}`).append(skillItem);
        //     }
        //   });

        //   document.querySelector(`#addCourseToTimeline-${i}`).addEventListener('click', () => {
        //     addCerificate({
        //       skills: course.skills,
        //       courseName: course.name,
        //       date: data.deadline,
        //       url: '',
        //       userName: ''
        //     });

        //     document.querySelector(`#addCourseToTimeline-${i}`).remove();
        //     document.querySelector(`#card-footer-${i}`).remove();
        //   });
        // });
      });

    // fetch(urlRequest)
    //   .then(response => response.json())
    //   .then(data => {
    //     console.log('JD', data);

    //     // modalContent.innerHTML = '';

    //     // const element = document.createElement('div');
    //     // const courses = data.offeredCourses;

    //     // for (let i = 0; i < courses.length; i++) {
    //     //   if (i <= 3) {
    //     //     const courseCard = document.createElement('div');
    //     //     skillReqStr = ``;

    //     //     for (let i = 0; i < data.gapSkills.length; i++) {
    //     //       skillReqStr += `${data.gapSkills[i]}, `;
    //     //       if (i >= 9) {
    //     //         break;
    //     //       }
    //     //     }

    //     //     skillGetStr = ``;

    //     //     for (let i = 0; i < courses[i].courseName.skills.length; i++) {
    //     //       skillReqStr += `${courses[i].courseName.skills[i]}, `;
    //     //     }

    //     //     courseCard.innerHTML = `
    //     //     <div class="container"> 
    //     //       <div class="container__text">
    //     //         <h1>${courses[i].courseName.name}</h1>
    //     //         <p>
    //     //         It seems you lack these skills:${skillReqStr})
    //     //         </p>
    //     //         <div class="container__text__timing">
    //     //           <div class="container__text__timing_time">
    //     //             <h2>Get Skills</h2>
    //     //             <a>${skillGetStr}</a>
    //     //           </div>

    //     //           <div class="container__text__timing_time">
    //     //             <h2>Link</h2>
    //     //             <a>${courses[i].courseName.url}</a>
    //     //           </div>

    //     //         </div>
    //     //     </div>
    //     //     `;
    //     //   }
    //     // }

    //     closeModal();
    //   });
  });
}

// Создание модального окна для добавления CV
function createModalCv() {
  modalContent.innerHTML = '';

  const element = document.createElement('div');
  element.innerHTML = `
  <span data-close class="close">&times;</span>
  <form action="${baseUrl}/uploader" method="POST" enctype="multipart/form-data">
    <input id="cvFileInput" type="file" name="file" accept=".pdf, .doc, .docx, .txt, .rtf" onchange="this.form.submit()">
    <p class="text-center">OR <br> Enter the link (hh.ru): </p>
    <input id="cvStringInput" type="text" name="link">
    <br>
    <br>
    <input class="btn btn-primary row text-center" id="cvSubmitButtonInput" type="submit" />
  </form>
  `;
  element.classList.add('text-center');

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

// Создание модального окна для добавления сертификата
function createModalEvidence() {
  modalContent.innerHTML = '';

  const element = document.createElement('div');

  element.innerHTML = `
  <span data-close class="close">&times;</span>
  <form autocomplete="off" action="#">
    <input style="width: 20rem" class="text-center" id="evidenceInput" type="text" name="evidenceInput" placeholder="certificateUrl (stepik, coursera)">
    <br>
    <br>
    <input class="btn btn-primary row text-center" id="parseCertificateButton" type="submit" />
  </form>
  `;
  element.classList.add('text-center');

  modalContent.append(element);

  const input = document.querySelector('#evidenceInput'),
    formButton = document.querySelector('#parseCertificateButton');
  formButton.addEventListener('click', (e) => {
    e.preventDefault();

    const urlRequest = `${baseUrl}/parseCertificate`;
    postData(urlRequest, { url: input.value })
      .then(response => response.json())
      .then(ceritificateData => {
        console.log(ceritificateData);
        addCerificate(ceritificateData);

        closeModal();
      });
  });
}

// Назначение цели для кнопки открытия окна
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

// Асинхронный POST запрос
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
  })
  return response;
}

function showRelatedCourses(data, matchedJob = '') {
  console.log('JD', data);
  modalContent.innerHTML = '';

  let gapSkills = [],
    relatedCourses = [];
  data.offeredCourses.forEach(course => {
    course.gapSkills.forEach(skill => {
      if (!(gapSkills.includes(skill)) && !(relatedCourses.includes(course.courseData)) && relatedCourses.length < 4) {
        gapSkills.push(skill)
        relatedCourses.push(course.courseData);
      }
    })
  });

  console.log(gapSkills);
  console.log(relatedCourses);

  modalContent.style = 'width: 100% !important';

  const rowForCards = document.createElement('div');
  rowForCards.classList.add('row');
  modalContent.append(rowForCards);

  relatedCourses.forEach((course, i) => {
    const courseCard = document.createElement('div');
    courseCard.innerHTML = `
    <div class="card text-center" style="width: 18rem;">
      <img class="card-img-top" src="../static/icons/coursera.jpg" alt="Coursera logo image">
        <div class="card-body">
          <a href="${course.url}"><h5 class="card-title">${course.name}</h5></a>
          <!-- <p class="card-text">Описание курса</p> -->
        </div>
        <ul class="list-group list-group-flush" id="courseSkillBlock-${i}">
        </ul>
        <div class="card-body" id="card-footer-${i}">
          <!-- <a href="${course.url}" class="card-link">Ссылка на курс</a> -->
          <input class="btn btn-primary row text-center" id="addCourseToTimeline-${i}" type="submit" value="Добавить на timeline">
          </div>
    </div>
    `;
    courseCard.classList.add('col-3');
    rowForCards.append(courseCard);

    course.skills.forEach((skill, j) => {
      if (j < 5) {
        const skillItem = document.createElement('li');
        skillItem.classList.add('list-group-item');
        skillItem.textContent = skill;

        document.querySelector(`#courseSkillBlock-${i}`).append(skillItem);
      }
    });

    if (matchedJob) {
      const jobText = document.createElement('p');
      jobText.textContent = `Наиболее подходящая профессия: ${matchedJob}`;
      document.querySelector(`#card-footer-${i}`).append(jobText);
    }

    document.querySelector(`#addCourseToTimeline-${i}`).addEventListener('click', () => {
      addCerificate({
        skills: course.skills,
        courseName: course.name,
        date: data.deadline,
        url: '',
        userName: ''
      });

      document.querySelector(`#addCourseToTimeline-${i}`).remove();
      if (!matchedJob) {
        document.querySelector(`#card-footer-${i}`).remove();
      }
    });
  });
}