// The name must match the 'name' field in your Native Messaging JSON manifest
const NATIVE_HOST_NAME = "com.autojob.bridge";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "processJobText") {
    
    // Connect and send to the Python script
    chrome.runtime.sendNativeMessage(
      NATIVE_HOST_NAME,
      { 
        text: request.payload,
        url: request.metadata.url,
        time: request.metadata.timestamp 
      },
      (response) => {
        if (chrome.runtime.lastError) {
          console.error("Native Messaging Error:", chrome.runtime.lastError.message);
          sendResponse({ error: chrome.runtime.lastError.message });
        } else {
          console.log("Received from Python:", response);
          sendResponse({ status: "success", pythonReply: response });
        }
      }
    );

    console.log("Sent to Python:", request.payload);

    return true; // Keeps the message channel open for the async response
  }
});