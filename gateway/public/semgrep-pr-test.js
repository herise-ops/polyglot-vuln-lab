// Temporary Semgrep PR-comment test.
// Scanner input only. Do not merge into main.

const userInput = window.location.hash.substring(1);

// INTENTIONAL DOM XSS:
// Untrusted URL input is inserted directly into the page.
document.body.innerHTML = userInput;
