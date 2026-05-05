const { app } = require("photoshop");
const { entrypoints } = require("uxp");

// Configuration
const STANDALONE_SERVER_URL = "http://localhost:6400"; // Prism Standalone
const PHOTOSHOP_SERVER_URL = "http://localhost:6401"; // Photoshop-specific instance

let isConnected = false;

// Connect to Prism Standalone (which launches Photoshop-specific instance)
async function connectToPrism() {
    if (isConnected) {
        console.log("Already connected to Prism");
        return;
    }
    
    try {
        console.log("Connecting to Prism Standalone...");
        const response = await fetch(`${STANDALONE_SERVER_URL}/prism`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: "connectPhotoshop",
                app: "photoshop"
            })
        });
        
        if (!response.ok) {
            console.error(`Failed to connect: ${response.status}`);
            showError(`Failed to connect to Prism Standalone (port 6400). Make sure Prism is running.`);
        } else {
            const data = await response.json();
            console.log("Connected to Prism:", data);
            isConnected = true;
        }
    } catch (error) {
        console.error(`Connection error:`, error);
        showError(`Cannot reach Prism Standalone (port 6400). Make sure Prism is running.`);
    }
}

// Disconnect from Prism
async function disconnectFromPrism() {
    if (!isConnected) {
        return;
    }
    
    try {
        console.log("Disconnecting from Prism...");
        await fetch(`${PHOTOSHOP_SERVER_URL}/prism`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: "disconnect",
                app: "photoshop"
            })
        });
        isConnected = false;
    } catch (error) {
        console.error(`Disconnect error:`, error);
    }
}

// Send command to Photoshop-specific Prism instance
async function sendCommand(command) {
    if (!isConnected) {
        showError("Not connected to Prism. Please reopen the panel.");
        return;
    }
    
    try {
        const response = await fetch(`${PHOTOSHOP_SERVER_URL}/prism`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                command: command,
                app: "photoshop"
            })
        });
        
        if (!response.ok) {
            console.error(`HTTP error! status: ${response.status}`);
            showError(`Server error: ${response.status}`);
        } else {
            const data = await response.json();
            console.log(`Command '${command}' sent successfully:`, data);
        }
    } catch (error) {
        console.error(`Failed to send command '${command}':`, error);
        showError(`Failed to connect to Prism server: ${error.message}`);
    }
}

// Show error dialog
function showError(message) {
    const dialog = document.createElement("dialog");
    dialog.innerHTML = `
        <form method="dialog">
            <h3>Error</h3>
            <p>${message}</p>
            <footer>
                <button type="submit">Close</button>
            </footer>
        </form>
    `;
    
    document.body.appendChild(dialog);
    dialog.showModal().finally(() => dialog.remove());
}

// Initialize the panel
entrypoints.setup({
    panels: {
        prismPanel: {
            create() {
                // Panel creation logic
                console.log("Prism panel created");
                // Connect to Prism Standalone when panel is created
                connectToPrism();
            },
            show() {
                // Set up event listeners when panel is shown
                const buttons = [
                    { id: "saveVersionBtn", command: "saveVersion" },
                    { id: "saveExtendedBtn", command: "saveExtended" },
                    { id: "exportBtn", command: "export" },
                    { id: "projectBrowserBtn", command: "projectBrowser" },
                    { id: "settingsBtn", command: "settings" }
                ];
                
                buttons.forEach(({ id, command }) => {
                    const btn = document.getElementById(id);
                    if (btn) {
                        btn.addEventListener("click", () => sendCommand(command));
                    }
                });
            },
            hide() {
                // Cleanup when panel is hidden
                console.log("Prism panel hidden");
            },
            destroy() {
                // Cleanup when panel is destroyed
                console.log("Prism panel destroyed");
                disconnectFromPrism();
            }
        }
    },
    commands: {}
});
