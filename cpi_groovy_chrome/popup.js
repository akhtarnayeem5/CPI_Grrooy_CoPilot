let extractedGroovyCode = "";

document.getElementById("generateBtn").addEventListener("click", async () => {
const requirement = document.getElementById("requirement").value.trim();
const statusEl = document.getElementById("status");
const outputSection = document.getElementById("outputSection");
const codePreview = document.getElementById("codePreview");

if (!requirement) {
    statusEl.textContent = "Please enter a requirement.";
    return;
}

statusEl.textContent = "Generating Groovy code...";
outputSection.style.display = "none";
codePreview.textContent = "";

try {
    const response = await fetch("https://127.0.0.1:8000/api/v1/generate-groovy", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({requirement})
    });

    if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
    }

    const data = await response.json(); 
    const rawMarkdown = data.output || "";
    const codeMatch = rawMarkdown.match(/```groovy([\s\S]*?)```/);

    if (codeMatch) {
        extractedGroovyCode = codeMatch[1].trim();
        codePreview.textContent = extractedGroovyCode;
        outputSection.style.display = "block";
        statusEl.textContent = "Groovy code generated successfully!";
        outputSection.classList.remove("hidden");

    }
}catch (error) {
        statusEl.textContent = "Connection error: Make sure FASTApi is running and accessible.";
    }
}
);

//copy to clipboard functionality
document.getElementById("copyBtn").addEventListener("click",  async () => {
    if (! extractedGroovyCode) return;
    await navigator.clipboard.writeText(extractedGroovyCode);
    document.getElementById("status").textContent = "Groovy code copied to clipboard!";

});
//Injecting the extracted Groovy code into the active tab
document.getElementById("injectBtn").addEventListener("click", async () => {
    if (!extractedGroovyCode) return;

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) return;

    await chrome.scripting.executeScript(
        {
            target: { tabId: tab.id },
            world: "MAIN",
            args: [extractedGroovyCode],
            func: (code) => {
                const aceEditor = document.querySelector('.ace_editor');
                if (aceEditor && window.ace) {
                    const editor = window.ace.edit(aceEditor[0].id);
                    if (editor) {
                        editor.setValue(code, -1); // -1 moves cursor to the start
                        return true;
                    }
                }
                // Fallback: Try to find a textarea if Ace Editor is not present
                const textarea = document.querySelector('textarea');
                if (textarea) {
                    textarea.value = code;
                    return true;
                }
                alert("No suitable editor found to inject the Groovy code.");
                return false;
            }}
    );
    document.getElementById("status").textContent = "Groovy code injected into the active tab!";
});