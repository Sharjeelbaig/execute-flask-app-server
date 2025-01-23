from flask import Flask, request
import subprocess

app = Flask(__name__)

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
