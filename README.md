# transtrans

## demo function
- real-time transcripting the voice of meeting attendee who is in a zoom meeting
- real-time translating the voice of meeting attendee who is in a zoom meeting to the user's lauguage
- user be able choose source and target language, and monitor the transription and tranlate output


## demo architecture diagram

<img width="914" alt="image" src="https://github.com/user-attachments/assets/c48aa333-7a5f-4eaf-afe4-ffa886fd7e2e" />


## pre-requisite
- **Enable Amazon Transcribe to capture Zoom Audio**
  - Mac User (BlackHole):
    - Install BlackHole:
    ```sh
    brew install blackhole-2ch
    ```
    or download and install from [BlackHole GitHub](https://github.com/ExistentialAudio/BlackHole)

    - Config Mac Audio Settings:
      - Open "Audio MIDI Setup" (in Applications > Utilities)
      - Create a Multi-Output Device:
         - Click "+" button > Select "Create Multi-Output Device"
         - Toggle your speaker and BlackHole-2ch
         - Ensure your speakers are set as the primary device
    - Config Zoom：
      - Open Zoom Settings > Audio
      - Select Speaker: Choose the Multi-Output Device you just created
      - This way you can hear the meeting audio while it's being sent to BlackHole

  - Windows User (VB-Cable):
    - Download and install VB-Cable:
      - Download from the official website
      - Run the installer as administrator
      - Configure Windows Audio Settings:
        - Right-click the volume icon in taskbar > Open Sound Settings
        - Select VB-Cable as the "Output" device
        - Optional: Use Voicemeeter to create mixed output to hear audio simultaneously
    - Config Zoom:
      - Open Zoom Settings > Audio
      - Select Speaker: Choose VB-Cable

## demo video

https://github.com/user-attachments/assets/0fde01c7-1ad8-46fb-aaf9-61d521cdaa48



