// Content script: detect page content changes, store job details text in a variable and save to file
(function(){
  'use strict';

  const TARGET_SELECTOR = '.jobs-search__job-details--wrapper';

  function getTargetText() {
    const target = document.querySelector(TARGET_SELECTOR);
    return target ? target.innerText : '';
  }

  // Store the latest saved text here
  let savedText = getTargetText();

  // Keep the previous text to compare
  let previousText = savedText;

  // Debounce timer id
  let saveTimer = null;

  // job link description 
  let jobLink = '';

  // Milliseconds to wait after last mutation before saving
  const DEBOUNCE_MS = 1000;

  // Function to perform the save: update variable and send to background script
  function performSave() {
    savedText = getTargetText();

    // Skip if empty or unchanged
    if (!savedText || savedText === previousText) return;
    previousText = savedText;


    // add the job link to the saved text
    if (jobLink) {
      savedText += `\nJob Link: ${jobLink}`;
    }

    console.log("Sending job details to Python...");

    // Send to Background Script instead of downloading
    if (typeof chrome !== 'undefined' && chrome.runtime) {
      chrome.runtime.sendMessage({
        action: "processJobText",
        payload: savedText,
        metadata: {
          url: window.location.href,
          timestamp: new Date().toISOString(),
        }
      }, (response) => {
        if (chrome.runtime.lastError) {
          console.error("Error sending to background:", chrome.runtime.lastError);
        } else {
          console.log("Python response:", response);
        }
      });
    }
  }

  // MutationObserver callback
  function onMutations(mutationsList) {
    // Simple guard: if no meaningful mutations, ignore
    if (!mutationsList || mutationsList.length === 0) return;

    // Debounce saves so we don't flood with downloads
    if (saveTimer) clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      saveTimer = null;
      performSave();
    }, DEBOUNCE_MS);
  }

  // Observer options: watch most kinds of DOM changes
  const observerOptions = {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true
  };

  const observer = new MutationObserver(onMutations);

  // Track clicks on the specific element and store its href
  document.addEventListener('click', (event) => {
    const clickedElement = event.target;

    // Check if the element is a <li>, if so extract href from <a> child
    if (clickedElement.tagName === 'LI') {
      const linkElement = clickedElement.querySelector('a');
      jobLink = linkElement ? (linkElement.getAttribute('href') || linkElement.href || '') : '';
    } else {
      jobLink = clickedElement.getAttribute('href') || clickedElement.href || '';
    }
  }, true);

  // Start observing
  observer.observe(document.documentElement, observerOptions);

  // Expose a small API on window so other extension parts can access savedText or trigger a save
  window.__autojob_content = {
    getSavedHtml: () => savedText,
    triggerSave: () => {
      if (saveTimer) clearTimeout(saveTimer);
      performSave();
    }
  };

  // Also listen for messages from extension (optional) to trigger a save
  if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
      if (!msg) return;
      if (msg.action === 'getSavedHtml') {
        sendResponse({ html: savedText });
      } else if (msg.action === 'saveNow') {
        performSave();
        sendResponse({ ok: true });
      }
    });
  }

})();
