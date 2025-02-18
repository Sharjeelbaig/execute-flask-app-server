from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Linux System Control</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f9f9f9;
      color: #333;
    }
    .container {
      max-width: 800px;
      margin: 50px auto;
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      padding: 20px;
    }
    h1 {
      text-align: center;
      color: #444;
    }
    form {
      margin-bottom: 20px;
    }
    label {
      display: block;
      margin-bottom: 8px;
      font-weight: bold;
    }
    input[type="text"], button {
      width: 100%;
      padding: 10px;
      margin-bottom: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    button {
      background-color: #007BFF;
      color: white;
      border: none;
      cursor: pointer;
    }
    button:hover {
      background-color: #0056b3;
    }
    pre {
      background: #f4f4f4;
      padding: 10px;
      border-radius: 4px;
      overflow-x: auto;
    }
    ul {
      list-style-type: none;
      padding: 0;
    }
    ul li {
      background: #f4f4f4;
      margin: 5px 0;
      padding: 10px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Linux System Control</h1>
    
    <!-- Run Command -->
    <form id="runCommandForm">
      <label for="commandInput">Run a Command:</label>
      <input type="text" id="commandInput" placeholder="Enter a Linux command (e.g., ls -l)">
      <button type="submit">Run Command</button>
    </form>
    <pre id="commandOutput">Command output will appear here...</pre>

    <!-- Open Application -->
    <form id="openAppForm">
      <label for="appNameInput">Open an Application:</label>
      <input type="text" id="appNameInput" placeholder="Enter an application name (e.g., firefox)">
      <button type="submit">Open Application</button>
    </form>
    <pre id="appOutput">Application output will appear here...</pre>

    <!-- List All Applications -->
    <button id="listAppsButton">List All Applications</button>
    <ul id="appList"></ul>
  </div>

  <script>
    // Run Command
    document.getElementById('runCommandForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const command = document.getElementById('commandInput').value;
      const response = await fetch(`/${encodeURIComponent(command)}`);
      const result = await response.json();
      document.getElementById('commandOutput').textContent = JSON.stringify(result, null, 2);
    });

    // Open Application
    document.getElementById('openAppForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const appName = document.getElementById('appNameInput').value;
      const response = await fetch(`/openApp/${encodeURIComponent(appName)}`);
      const result = await response.json();
      document.getElementById('appOutput').textContent = JSON.stringify(result, null, 2);
    });

    // List All Applications
    document.getElementById('listAppsButton').addEventListener('click', async () => {
      const response = await fetch('/listAllLinuxApps');
      const apps = await response.text();
      document.getElementById('appList').innerHTML = apps;
    });
  </script>
</body>
</html>

'''

# Run command
@app.route('/<path:dummy>')
def hello_world(dummy):
    # Convert %20 to space, then convert spaces into an array
    command = dummy.replace('%20', ' ').split(' ')

    try:
        output = subprocess.check_output(command, text=True)
        return {
            'output': output,
            'command': command
        }
    except subprocess.CalledProcessError as e:
        return {
            'error': str(e),
            'command': command
        }, 400
    except Exception as e:
        return {
            'error': f"Unexpected Error: {e}",
            'command': command
        }, 500

# Open application
@app.route('/openApp/<appname>')
def open_app(appname):
    command = ['xdg-open', appname]
    try:
        output = subprocess.check_output(command, text=True)
        return {
            'output': output,
            'command': command
        }
    except subprocess.CalledProcessError as e:
        return {
            'error': str(e),
            'command': command
        }, 400
    except Exception as e:
        return {
            'error': f"Unexpected Error: {e}",
            'command': command
        }, 500

# List all desktop entries (applications)
@app.route('/listAllLinuxApps')
def list_all_linux_apps():
    command = ['ls', '/usr/share/applications']
    try:
        output = subprocess.check_output(command, text=True)
        return f"""
        <h1>Applications</h1>
        <ol>
            <li>{'</li><li>'.join(output.split())}</li>
        </ol>
        """
    except subprocess.CalledProcessError as e:
        return {
            'error': str(e),
            'command': command
        }, 400
    except Exception as e:
        return {
            'error': f"Unexpected Error: {e}",
            'command': command
        }, 500

if __name__ == '__main__':
    app.run()
