# 📲 Apepe
> 📲 Enumerate information from an app based on the APK file

<div align="center">
 <img src="https://i.imgur.com/0qh6sHq.jpg" width="850">
</div>

<br>

<p align="center">
    <img src="https://img.shields.io/github/license/oppsec/Apepe?color=orange&logo=github&logoColor=orange&style=for-the-badge">
    <img src="https://img.shields.io/github/issues/oppsec/Apepe?color=orange&logo=github&logoColor=orange&style=for-the-badge">
    <img src="https://img.shields.io/github/stars/oppsec/Apepe?color=orange&label=STARS&logo=github&logoColor=orange&style=for-the-badge">
    <img src="https://img.shields.io/github/forks/oppsec/Apepe?color=orange&logo=github&logoColor=orange&style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/oppsec/Apepe?color=orange&logo=github&logoColor=orange&style=for-the-badge">
</p>

___

### 🕵️ What is Apepe?
🕵️ **Apepe** is a project developed to help to capture informations from a Android app through his APK file. It can be used to extract the content, get app settings, suggest SSL Pinning bypass based on the app detected language, extract deeplinks from AndroidManifest.xml, JSONs and DEX files.

<br>

### ⚡ Installing / Getting started

A quick guide of how to install and use Apepe.

```shell
1. git clone https://github.com/oppsec/Apepe.git
2. pip install -r requirements.txt --break-system-packages
3. python3 main -h
```

<br>

### ⚙️ Pre-requisites
- [Python](https://www.python.org/downloads/) installed on your machine
- APK file from the targeted app
- Androguard library >= 4.1.2

<br>

### ✨ Features
- List the activies, permissions, services, and libraries used by the app
- Identify the app development language based on classes name
- Suggest SSL Pinnings bypass with the `-l` flag
- Find deeplinks in DEX, JSONs files and AndroidManifest.xml with the `-d` flag

<br>

### 🖼️ Preview

<img src="https://i.imgur.com/UAnF9k1.png" width=800>

<br>

### 🔨 Contributing

A quick guide of how to contribute with the project.

```shell
1. Create a fork from Apepe repository
2. Download the project with git clone https://github.com/your/Apepe.git
3. cd Apepe/
4. Make your changes
5. Commit and make a git push
6. Open a pull request
```

<br>

### ⚠️ Warning
- The developer is not responsible for any malicious use of this tool.
