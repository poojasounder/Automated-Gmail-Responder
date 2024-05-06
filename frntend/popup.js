const defaultPrompt =
  'Task: Write an email response to the following email from a student with answers to their questions given the following context.';

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
