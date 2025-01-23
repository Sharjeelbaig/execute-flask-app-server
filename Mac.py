from flask import Flask, request
import subprocess

app = Flask(__name__)

# Run command
@app.route('/<path:dummy>')
def hello_world(dummy):
    # conver %20 to space then convert spaces into an array
    command = dummy.replace('%20', ' ').split(' ')

    try:
        output = subprocess.check_output(command, text=True)
        # return f"""
        # <pre>{output}</pre>
        # <code>Command: {command}</code>
        # """
        return {
            'output': output,
            'command': command
        }
    except subprocess.CalledProcessError as e:
        return f"""
        <pre>Error: {e}</pre>
        <code>Command: {command}</code>
        """, 400
    except Exception as e:
        return f"""
        <pre>Unexpected Error: {e}</pre>
        <code>Command: {command}</code>
        """, 500
    
#open -a appname
@app.route('/openApp/<appname>')
def openApp(appname):
    command = ['open', '-a', appname]
    try:
        output = subprocess.check_output(command, text=True)
        return f"""
        <pre>{output}</pre>
        <code>Command: {command}</code>
        """
    except subprocess.CalledProcessError as e:
        return f"""
        <pre>Error: {e}</pre>
        <code>Command: {command}</code>
        """, 400
    except Exception as e:
        return f"""
        <pre>Unexpected Error: {e}</pre>
        <code>Command: {command}</code>
        """, 500


# Show all app
@app.route('/listAllMacApps')
def listAllMacApps():
    command = ['ls', '/Applications']
    try:
        output = subprocess.check_output(command, text=True)
        return f"""
    <h1>Applications</h1>
    <ol>
        <li>{'</li><li>'.join(output.split())}</li>
    </ol>

"""
    except subprocess.CalledProcessError as e:
        return f"""
        <pre>Error: {e}</pre>
        <code>Command: {command}</code>
        """, 400
    except Exception as e:
        return f"""
        <pre>Unexpected Error: {e}</pre>
        <code>Command: {command}</code>
        """, 500

if __name__ == '__main__':
    app.run()
