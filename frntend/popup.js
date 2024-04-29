const defaultPrompt = 'This is the defualt prompt';

document.addEventListener('DOMContentLoaded', function () {
  chrome.storage.local.get('savedText', function (data) {
    let savedText = data.savedText || defaultPrompt;
    document.getElementById('prompt').value = savedText;
  });

  document.getElementById('prompt').addEventListener('input', function () {
    let text = document.getElementById('prompt').value;
    chrome.storage.local.set({ savedText: text });
  });

  document.getElementById('resetButton').addEventListener('click', function () {
    document.getElementById('prompt').value = defaultPrompt;
    chrome.storage.local.set({ savedText: defaultPrompt });
  });
});
