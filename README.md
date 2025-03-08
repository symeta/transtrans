# transtrans

## demo function
- real-time transcripting the voice of meeting attendee who is in a zoom meeting
- real-time translating the voice of meeting attendee who is in a zoom meeting to the user's lauguage
- user be able choose source and target language, and monitor the transription and tranlate output


## demo architecture diagram


## pre-requisite
- transcribe capture zoom audio
  - Mac 用户 (BlackHole)：
    - 安装 BlackHole：
    ```sh
    brew install blackhole-2ch
    ```
    或从 BlackHole GitHub 页面 下载安装

    - 配置 Mac 音频设置：
      打开"音频 MIDI 设置"（在应用程序 > 实用工具中）
      创建一个多输出设备：
      点击"+"按钮 > 选择"创建多输出设备"
      勾选你的扬声器和 BlackHole 2ch
      确保扬声器是主设备
    - 配置 Zoom：
      打开 Zoom 设置 > 音频
      选择扬声器：选择刚创建的多输出设备
      这样你可以同时听到会议声音，且音频会被发送到 BlackHole

  - Windows 用户 (VB-Cable)：
    - 下载并安装 VB-Cable：
      从官方网站下载
      以管理员身份运行安装程序
      配置 Windows 音频设置：
      右键点击任务栏上的音量图标 > 打开声音设置
      在"输出"设备中选择 VB-Cable
      可选：使用 Voicemeeter 创建混合输出以同时听到声音
    - 配置 Zoom：
      打开 Zoom 设置 > 音频
      选择扬声器：选择 VB-Cable

## demo video



