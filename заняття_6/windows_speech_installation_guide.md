# SpeechRecognition and PyAudio on Windows

A troubleshooting guide for Python students.

## 1. Start here

- **SpeechRecognition** lets your Python program work with speech recognition services.
- **PyAudio** lets your program record sound from a microphone.
- On Windows, a compatible prebuilt PyAudio package includes PortAudio. You normally do **not** need to install PortAudio separately.

Open **Command Prompt**, **PowerShell**, or your editor's **Terminal**. Run these commands one at a time:

```powershell
python --version
python -m pip install --upgrade pip
python -m pip install SpeechRecognition
python -m pip install PyAudio
```

Use `python -m pip` instead of plain `pip` so the packages are installed for that Python interpreter.

If your class uses a virtual environment, use your teacher's project terminal and interpreter. See section 8 if the installation works but your program cannot import the libraries.

**Version tip:** Follow your teacher's Python version. As checked on 28 October 2026, PyAudio 0.2.14 has standard Windows wheels for CPython 3.9–3.13, including Python 3.12. Python 3.14 or later and native Windows ARM64 Python do not have matching wheels in that release. Do not assume the newest Python version will work with every library.

### Check that installation worked

```powershell
python -c "import speech_recognition; import pyaudio; print('Both libraries are ready!')"
```

The installation name is `SpeechRecognition`, but the Python import is `speech_recognition`.

## 2. `SyntaxError: invalid syntax`

**What happened:** You may have typed an installation command into the Python shell or a `.py` file.

If the prompt starts with `>>>`, you are inside Python. Type:

```python
exit()
```

Then run the installation commands in the terminal. Do not copy the `>>>` or `PS C:\...>` prompt characters.

## 3. `'pip' is not recognized`

Try this instead:

```powershell
python -m pip install SpeechRecognition
python -m pip install PyAudio
```

If `python` is also not recognized, continue to section 4.

A warning saying that a `Scripts` directory is not on `PATH` does not necessarily mean installation failed. Run the import check in section 1.

## 4. `'python' is not recognized` or `Python was not found`

Try the Windows Python launcher:

```powershell
py --version
py -m pip install SpeechRecognition
py -m pip install PyAudio
```

If that works, use `py` in place of `python` in this guide. If several Python versions are installed, `py` may choose a different one from your editor; check section 8.

If neither command works:

1. Close and reopen the terminal, then try again.
2. If Python is not installed, ask your teacher or parent to help install the class version from [python.org](https://www.python.org/downloads/windows/).
3. With the traditional installer, enable **Add python.exe to PATH** if offered.
4. Reopen the terminal after installing.

If `python` opens the Microsoft Store despite an existing installation, try `py`. Ask your teacher to check Windows **Manage app execution aliases** and your Python installation before changing settings.

## 5. `No module named pip`

Run:

```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

Then retry installation. If `ensurepip` is also missing or fails, ask your teacher to help repair the Python installation.

## 6. `Failed building wheel for PyAudio`, C++ errors, or missing `portaudio.h`

You might see:

```text
Failed building wheel for PyAudio
Microsoft Visual C++ 14.0 or greater is required
fatal error C1083: Cannot open include file: 'portaudio.h'
```

**What happened:** pip tried to build PyAudio from source instead of downloading a ready-to-use Windows wheel. A wheel is a prebuilt package.

First try:

```powershell
python -m pip install --upgrade pip
python -m pip install --only-binary=:all: PyAudio
```

`--only-binary=:all:` prevents a source build. If it reports no matching distribution, check section 7.

**For a beginner class, use a Python version that has a compatible wheel.** Installing C++ Build Tools alone may not fix this: a source build also needs PortAudio development files.

For example, if your teacher chooses standard 64-bit CPython 3.13, install it alongside your existing Python, then create a new project environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install SpeechRecognition
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: PyAudio
```

Run these commands in your project folder. If `.venv` already exists, ask your teacher to help create a fresh environment rather than overwriting it. Select the new environment in your editor too.

Do not download random wheel files from unknown websites. Use the official packages on PyPI.

## 7. `No matching distribution found` or `Could not find a version that satisfies the requirement`

Possible causes include an unsupported Python version, an incompatible CPU architecture, a typing mistake, or a restricted package server.

1. Check spelling: `SpeechRecognition` and `PyAudio`.
2. Check your Python and update pip:

   ```powershell
   python --version
   python -m pip install --upgrade pip
   python -c "import platform, struct; print(platform.python_implementation(), platform.machine()); print(struct.calcsize('P') * 8, 'bit Python')"
   ```

3. For PyAudio, compare your setup with the version tip in section 1. Ask your teacher to help choose a supported interpreter. On an ARM Windows laptop, ask about using an x64 Python installation supported by that laptop's Windows version.
4. If the output includes connection errors or retry warnings, fix the connection first; see section 10.

An error about `Requires-Python` means the package requires a different Python version. SpeechRecognition currently requires Python 3.9 or newer; PyAudio wheel availability adds its own limits.

## 8. `ModuleNotFoundError` even though installation succeeded

Examples:

```text
ModuleNotFoundError: No module named 'speech_recognition'
ModuleNotFoundError: No module named 'pyaudio'
AttributeError: Could not find PyAudio; check installation
```

Usually, your editor is running a different Python interpreter from the one used for installation.

Run this **inside your program or editor's Python console**:

```python
import sys
print(sys.executable)
```

Compare it with the terminal:

```powershell
python -c "import sys; print(sys.executable)"
python -m pip show SpeechRecognition PyAudio
```

If the paths differ, install using the editor's interpreter or change the editor to the correct one.

- **VS Code:** Open the Command Palette, choose **Python: Select Interpreter**, and select your project environment. Open a new terminal afterward.
- **PyCharm:** Check the project's Python interpreter in Settings. Use that interpreter's package installer or project terminal.
- **Thonny:** It may use its own Python. Use **Tools → Manage packages** for that interpreter, with your teacher's help if PyAudio needs a different Python version.

For a project environment named `.venv`, you can install directly without activating it:

```powershell
.\.venv\Scripts\python.exe -m pip install SpeechRecognition PyAudio
```

Also check that your own files are not named `speech_recognition.py` or `pyaudio.py`. Rename them to something like `voice_test.py`, then restart your program.

## 9. `Access is denied`, `PermissionError`, or PowerShell blocks activation

### Installation permission errors

Close any running copy of your program and retry. For a personal project, a virtual environment usually avoids system-folder permissions:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install SpeechRecognition PyAudio
```

If you are deliberately installing outside a virtual environment, a per-user install may help:

```powershell
python -m pip install --user SpeechRecognition PyAudio
```

Do not use `--user` inside a virtual environment. On a school-managed PC, ask your teacher or administrator if installation is blocked.

### `Activate.ps1 cannot be loaded because running scripts is disabled`

You can use the environment without changing PowerShell's security settings:

```powershell
.\.venv\Scripts\python.exe -m pip install SpeechRecognition PyAudio
.\.venv\Scripts\python.exe voice_test.py
```

The second command assumes you have saved your program as `voice_test.py`.

## 10. Download timeout, proxy, or certificate errors

Examples include `ReadTimeoutError`, `ProxyError`, `CERTIFICATE_VERIFY_FAILED`, and repeated `Retrying` messages.

1. Check that websites open and complete any Wi-Fi sign-in page.
2. Check that Windows date and time are correct.
3. For a slow connection, retry with a longer timeout:

   ```powershell
   python -m pip install --timeout 120 SpeechRecognition PyAudio
   ```

4. On school Wi-Fi, ask your teacher or IT administrator to check proxy settings, certificates, and access to `pypi.org` and `files.pythonhosted.org`.

Do not disable antivirus or certificate checking to make installation work.

## 11. `DLL load failed` while importing PyAudio

This can indicate a damaged installation or an incompatible native component.

1. Check that your editor uses the intended interpreter (section 8).
2. Reinstall the prebuilt package for that interpreter:

   ```powershell
   python -m pip install --force-reinstall --no-cache-dir --only-binary=:all: PyAudio
   ```

3. If it still fails, send your teacher the full error and Python details from section 14. A teacher may need to check Windows runtime dependencies or recreate the environment.

Do not download individual DLL files from random websites.

## 12. Libraries import, but the microphone does not work

These are runtime or device problems, so reinstalling the libraries may not help.

### `No Default Input Device Available` or `Invalid input device`

1. Connect your microphone or headset and check its mute button.
2. Open **Settings → System → Sound → Input**. Select and test the correct microphone.
3. Restart your Python program after connecting the device.
4. If your code uses `device_index`, check it again: device numbers can change when you reconnect equipment.

List device names in Python:

```python
import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(index, name)
```

The list can include output devices. With your teacher, choose an entry that supports microphone input, then use its number:

```python
# Example only: replace 2 with your microphone's actual index.
with sr.Microphone(device_index=2) as source:
    pass
```

### Microphone permission is blocked

On **Windows 11**, open **Settings → Privacy & security → Microphone**. Enable microphone access, app access, and **Let desktop apps access your microphone**.

On **Windows 10**, open **Settings → Privacy → Microphone** and check the equivalent device, app, and desktop-app permissions.

Then restart your editor. If the controls are locked by your school, ask your teacher.

### `Invalid sample rate`, device busy, or audio overflow

Close other recording or calling apps, try the built-in microphone or a wired headset, and restart the program. If your code forces a `sample_rate`, ask your teacher to try the device default by using `sr.Microphone()` without that argument.

## 13. Recording works, but speech is not recognized

These errors happen after installation:

| Error or symptom | What to try |
| --- | --- |
| `UnknownValueError` | Speak clearly, reduce background noise, and check the recognition language. |
| `WaitTimeoutError` | Start speaking after the listening prompt; ask your teacher to check the listening timeout. |
| `RequestError` | For an online recognizer, check the internet and service access. Depending on the service, your teacher may need to check credentials, quotas, or availability. |
| Listening seems to continue forever | Press `Ctrl+C` in the terminal. Ask your teacher to set `timeout` and `phrase_time_limit`. |

Your teacher can use `adjust_for_ambient_noise()` before recording. Stay quiet while it calibrates.

The language should match the speaker, for example `language="en-US"` or `language="uk-UA"` when using a recognizer that supports it. Online recognition sends recorded audio to a service; follow your teacher's instructions about which service to use.

## 14. Still stuck? Send this to your teacher

Copy the full error as text, including the lines above the final error. Also send:

```powershell
python --version
python -m pip --version
python -c "import sys, platform; print(sys.executable); print(platform.machine())"
python -m pip show SpeechRecognition PyAudio
```

Mention your editor and whether you use a virtual environment. If `python` does not work, say that and try the same commands with `py`.

**Good news:** `Requirement already satisfied` means the package is already installed for that interpreter. A notice that a newer pip version is available is not an installation failure.

## Official references

Checked on 28 October 2026. Package support can change.

- [SpeechRecognition installation and requirements](https://pypi.org/project/SpeechRecognition/)
- [PyAudio Windows installation and available wheels](https://pypi.org/project/PyAudio/)
- [pip user guide](https://pip.pypa.io/en/stable/user_guide/)
- [Python ensurepip documentation](https://docs.python.org/3/library/ensurepip.html)
- [Microsoft: microphone permissions](https://support.microsoft.com/en-us/windows/privacy/turn-on-app-permissions-for-your-microphone-in-windows)
- [SpeechRecognition troubleshooting](https://github.com/Uberi/speech_recognition#troubleshooting)
