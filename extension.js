const vscode = require('vscode');

/**
 * Hermes Visual Agent Desk — VS Code Extension
 * Embeds the 3D Voxel Studio and 2D Hermes Pixel Office directly into VS Code editor or panel.
 */
function activate(context) {
    const provider = new HermesDeskViewProvider(context.extensionUri);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('hermesDesk.sidebarView', provider)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('hermesDesk.open', () => {
            const panel = vscode.window.createWebviewPanel(
                'hermesDeskTab',
                'Hermes Visual Agent Desk',
                vscode.ViewColumn.One,
                {
                    enableScripts: true,
                    retainContextWhenHidden: true
                }
            );
            panel.webview.html = getWebviewContent('http://127.0.0.1:8765');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('hermesDesk.open2D', () => {
            const panel = vscode.window.createWebviewPanel(
                'hermesDesk2D',
                'Hermes 2D Pixel Office',
                vscode.ViewColumn.Beside,
                {
                    enableScripts: true,
                    retainContextWhenHidden: true
                }
            );
            panel.webview.html = getWebviewContent('http://127.0.0.1:8765?view=2d');
        })
    );
}

class HermesDeskViewProvider {
    constructor(extensionUri) {
        this._extensionUri = extensionUri;
    }

    resolveWebviewView(webviewView) {
        webviewView.webview.options = {
            enableScripts: true,
            retainContextWhenHidden: true
        };
        webviewView.webview.html = getWebviewContent('http://127.0.0.1:8765');
    }
}

function getWebviewContent(url) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hermes Desk</title>
    <style>
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: var(--vscode-editor-background, #090d16);
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>
<body>
    <iframe src="${url}" allow="clipboard-read; clipboard-write;"></iframe>
</body>
</html>`;
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
