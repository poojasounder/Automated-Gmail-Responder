(function () {
  const bodyElement = document.body;
  const btnLocation = '.a8X.gU'; //Toolbar button container
  const bodyLocation = '.gs'; //Body of email container
  const composeLocation = '.Am.aiL.aO9.Al.editable.LW-avf.tS-tW'; //Compose email container
  const imageURL = chrome.runtime.getURL('/logo.png'); //Logo used for button
  const apiURL = 'https://dummyjson.com/products/1'; //Dummy api for testing purposes

  //Checks for necessary elements to load
  const elementObserver = new MutationObserver(function (
    mutations,
    mutationInstance
  ) {
    const someDiv = document.querySelector(btnLocation);
    if (someDiv) {
      mutationInstance.disconnect();
      injectButton();
    }
  });

  function observePage() {
    elementObserver.observe(bodyElement, {
      childList: true,
      subtree: true,
    });
  }

  //Resets elementObserver when URL changes
  function observeURLChanges() {
    const locationObserver = new MutationObserver(function () {
      observePage();
    });

    locationObserver.observe(document, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['href'],
    });
  }

  //Adds button to reply toolbar
  function injectButton() {
    const someDiv = document.querySelector(btnLocation);
    const btnCheck = document.querySelector('#capstone-button');
    if (someDiv && !btnCheck) {
      const container = document.createElement('div');
      container.classList.add('wG', 'J-Z-I');

      const img = document.createElement('img');
      img.src = imageURL;
      img.alt = 'Capstone Draft';
      img.id = 'capstone-button';
      img.classList.add('aaA', 'aMZ');

      img.style.cssText = 'cursor: pointer; width: 20px; height: 20px';

      container.appendChild(img);
      document.querySelector(btnLocation).appendChild(container);
      img.addEventListener('click', handleClick());
    }
  }

  function handleClick() {
    document
      .getElementById('capstone-button')
      .addEventListener('click', function (event) {
        processEmail();
      });
  }

  async function processEmail() {
    const recievedEmail = extractBody();
    const emailResponse = await buildEmail(recievedEmail);
    injectBody(emailResponse);
  }

  //Constructs the email greeting and body
  async function buildEmail(text) {
    let emailResponse = ``;
    const name = text.split('<')[0];
    const body = text.split('me')[1];
    const apiResponse = await apiRequest(body);
    emailResponse = `Hello ${name},<br>`;
    emailResponse += apiResponse;
    console.log(emailResponse);
    return emailResponse;
  }

  //Injects built email into the compose location of gmail
  function injectBody(text) {
    if (document.querySelector(composeLocation)) {
      document.querySelector(composeLocation).innerHTML = text;
    }
  }

  //Sends the recieved email to the api to get response
  async function apiRequest(text) {
    let result = await fetch(apiURL);
    let data = await result.json();

    let response = data.description + text;

    return response;
  }

  //Extracts text from email for future usage
  function extractBody() {
    const elements = document.querySelectorAll(bodyLocation);
    const extractedBody = [];
    elements.forEach((element) => {
      extractedBody.push(element.textContent);
    });
    return extractedBody[0];
  }

  observePage();
  observeURLChanges();
})();
