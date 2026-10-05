# 🎙️ AI Meeting Minutes Generator

An AI-powered web application that converts meeting audio/video recordings into structured and easy-to-read meeting minutes.

The system uses **OpenAI Whisper** for speech-to-text transcription and local Python-based processing for summarization, speaker-turn detection, decisions, and action items.

---

## 📌 Project Overview

The **AI Meeting Minutes Generator** helps users automatically convert recorded meetings into organized meeting documentation.

Instead of manually listening to an entire meeting and preparing notes, users can upload an audio or video recording and generate:

- 📝 Meeting Transcript
- 👥 Speaker Turns
- 📋 Meeting Summary
- 🔑 Key Points
- ✅ Action Items
- 🎯 Decisions
- 📊 Meeting Statistics
- 📄 Exportable Meeting Minutes

---

## 🎯 Objectives

The main objectives of this project are:

1. Automatically convert meeting recordings into text.
2. Reduce the time required to prepare meeting minutes.
3. Generate concise meeting summaries.
4. Identify important discussion points.
5. Extract possible decisions and action items.
6. Organize meeting information in a professional dashboard.
7. Provide a simple and user-friendly interface.

---

## ✨ Features

### 🎙️ Audio/Video Upload

Supports common meeting recording formats:

```text
MP3
WAV
M4A
MP4
AVI
MOV
MKV
WEBM
MPEG
```

Maximum recommended upload size:

```text
500 MB
```

---

### 🗣️ Speech-to-Text

The application uses **OpenAI Whisper** to convert speech into text.

Example:

```text
Meeting Audio
      ↓
Whisper
      ↓
Text Transcript
```

Whisper can also process Tamil, English, Hindi, and other supported languages.

For example:

```python
transcribe_audio(
    "uploads/meeting.mp3",
    language="ta"
)
```

---

### 👥 Speaker Detection

The project includes a basic speaker-turn detection module.

Example:

```text
Speaker 1: Good morning everyone.

Speaker 2: Good morning. Let's start the meeting.

Speaker 1: Today we will discuss the project progress.
```

> Note: The current implementation estimates speaker turns using speech pauses. It does not identify the actual person's identity by voice.

---

### 📝 Automatic Summarization

The transcript is processed to generate a concise summary.

Example:

```text
The team discussed the current project progress,
frontend development, backend development and
the upcoming testing schedule.
```

---

### 🔑 Key Points

Important topics from the meeting are extracted automatically.

Example:

```text
• Frontend development is almost complete.
• Backend development is in progress.
• Testing is