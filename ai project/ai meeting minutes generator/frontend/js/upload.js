"use strict";

const API_BASE_URL = "http://127.0.0.1:8000";
const MAX_FILE_SIZE = 500 * 1024 * 1024;

const ALLOWED_EXTENSIONS = [
    ".mp3",
    ".wav",
    ".m4a",
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
    ".mpeg"
];

let selectedFile = null;
let isUploading = false;

document.addEventListener("DOMContentLoaded", function () {
    setupUploadArea();
    setupFileInput();
    setupGenerateButton();
    setupRemoveButton();

    console.log("Upload.js loaded successfully.");
});

/* ================================
   UPLOAD AREA
================================ */

function setupUploadArea() {
    const uploadArea = document.querySelector("#uploadArea, .upload-area");

    if (!uploadArea) return;

    uploadArea.addEventListener("click", function (event) {
        if (
            event.target.closest(
                "#fileInput, #removeFile, .remove-file, .remove-button"
            )
        ) {
            return;
        }

        const fileInput = document.querySelector("#fileInput");

        if (fileInput) {
            fileInput.click();
        }
    });

    uploadArea.addEventListener("dragover", function (event) {
        event.preventDefault();

        uploadArea.classList.add("drag-over");
    });

    uploadArea.addEventListener("dragleave", function () {
        uploadArea.classList.remove("drag-over");
    });

    uploadArea.addEventListener("drop", function (event) {
        event.preventDefault();

        uploadArea.classList.remove("drag-over");

        const files = event.dataTransfer.files;

        if (files.length > 0) {
            validateAndSelectFile(files[0]);
        }
    });
}

/* ================================
   FILE INPUT
================================ */

function setupFileInput() {
    const fileInput = document.querySelector("#fileInput");

    if (!fileInput) return;

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            validateAndSelectFile(fileInput.files[0]);
        }
    });
}

/* ================================
   VALIDATE FILE
================================ */

function validateAndSelectFile(file) {
    if (!file) return;

    const extension = getFileExtension(file.name);

    if (!ALLOWED_EXTENSIONS.includes(extension)) {
        showToast(
            "Unsupported file format. Please upload an audio or video file.",
            "error"
        );
        return;
    }

    if (file.size === 0) {
        showToast("The selected file is empty.", "error");
        return;
    }

    if (file.size > MAX_FILE_SIZE) {
        showToast("File size must be less than 500 MB.", "error");
        return;
    }

    selectedFile = file;

    displaySelectedFile(file);

    showToast("Meeting file selected successfully.", "success");
}

/* ================================
   FILE INFORMATION
================================ */

function displaySelectedFile(file) {
    const selectedFileBox = document.querySelector(
        "#selectedFile, .selected-file"
    );

    if (!selectedFileBox) return;

    const fileName = selectedFileBox.querySelector(
        "#fileName, .file-name"
    );

    const fileSize = selectedFileBox.querySelector(
        "#fileSize, .file-size"
    );

    const fileType = selectedFileBox.querySelector(
        "#fileType, .file-type"
    );

    if (fileName) {
        fileName.textContent = file.name;
    }

    if (fileSize) {
        fileSize.textContent = formatFileSize(file.size);
    }

    if (fileType) {
        fileType.textContent = getFileExtension(file.name)
            .replace(".", "")
            .toUpperCase();
    }

    selectedFileBox.style.display = "flex";
}

/* ================================
   REMOVE FILE
================================ */

function setupRemoveButton() {
    const removeButton = document.querySelector(
        "#removeFile, .remove-file, .remove-button"
    );

    if (!removeButton) return;

    removeButton.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();

        removeSelectedFile();
    });
}

function removeSelectedFile() {
    selectedFile = null;

    const fileInput = document.querySelector("#fileInput");

    if (fileInput) {
        fileInput.value = "";
    }

    const selectedFileBox = document.querySelector(
        "#selectedFile, .selected-file"
    );

    if (selectedFileBox) {
        selectedFileBox.style.display = "none";
    }

    updateProgress(0, "");

    showToast("Selected file removed.", "info");
}

/* ================================
   GENERATE BUTTON
================================ */

function setupGenerateButton() {
    const generateButton = document.querySelector(
        "#generateButton, .generate-button, [data-generate]"
    );

    if (!generateButton) return;

    generateButton.addEventListener(
        "click",
        generateMeetingMinutes
    );
}

/* ================================
   PROCESS MEETING
================================ */

async function generateMeetingMinutes() {
    if (isUploading) return;

    if (!selectedFile) {
        showToast(
            "Please select a meeting recording first.",
            "warning"
        );
        return;
    }

    isUploading = true;

    const button = document.querySelector(
        "#generateButton, .generate-button, [data-generate]"
    );

    const progressBox = document.querySelector(
        "#uploadProgress, .upload-progress"
    );

    try {
        if (button) {
            button.disabled = true;
            button.innerHTML =
                '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
        }

        if (progressBox) {
            progressBox.style.display = "block";
        }

        updateProgress(10, "Preparing meeting file...");

        const formData = new FormData();

        formData.append("file", selectedFile);

        updateProgress(25, "Uploading meeting recording...");

        const response = await fetch(
            `${API_BASE_URL}/process-meeting`,
            {
                method: "POST",
                body: formData
            }
        );

        updateProgress(50, "AI is processing your meeting...");

        let data;

        try {
            data = await response.json();
        } catch (error) {
            throw new Error(
                "The server returned an invalid response."
            );
        }

        if (!response.ok) {
            throw new Error(
                data.detail ||
                data.message ||
                "Meeting processing failed."
            );
        }

        updateProgress(70, "Transcribing meeting...");

        await wait(500);

        updateProgress(
            85,
            "Generating structured meeting minutes..."
        );

        await wait(500);

        updateProgress(
            100,
            "Meeting minutes generated successfully!"
        );

        saveLatestResult(data);

        saveMeetingHistory(data);

        displayMeetingResult(data);

        showToast(
            "Meeting minutes generated successfully!",
            "success"
        );

    } catch (error) {
        console.error("Upload Error:", error);

        updateProgress(
            0,
            "Processing failed."
        );

        showToast(
            error.message ||
            "Unable to connect to the AI server.",
            "error"
        );

    } finally {
        isUploading = false;

        if (button) {
            button.disabled = false;

            button.innerHTML =
                '<i class="fa-solid fa-wand-magic-sparkles"></i> Generate AI Meeting Minutes';
        }
    }
}

/* ================================
   DISPLAY RESULT
================================ */

function displayMeetingResult(data) {
    const resultBox = document.querySelector(
        "#meetingResult, .meeting-result"
    );

    if (!resultBox) return;

    resultBox.style.display = "block";

    const transcriptBox = resultBox.querySelector(
        "#transcript, .transcript"
    );

    const minutesBox = resultBox.querySelector(
        "#minutes, .minutes"
    );

    if (transcriptBox) {
        transcriptBox.textContent =
            data.transcript ||
            "Transcript not available.";
    }

    if (minutesBox) {
        if (typeof data.minutes === "string") {
            minutesBox.textContent = data.minutes;
        } else {
            minutesBox.textContent =
                JSON.stringify(
                    data.minutes || {},
                    null,
                    2
                );
        }
    }

    resultBox.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

/* ================================
   SAVE LATEST RESULT
================================ */

function saveLatestResult(data) {
    try {
        localStorage.setItem(
            "latestMeetingResult",
            JSON.stringify(data)
        );
    } catch (error) {
        console.error(
            "Unable to save latest result:",
            error
        );
    }
}

/* ================================
   MEETING HISTORY
================================ */

function saveMeetingHistory(data) {
    try {
        let history = getMeetingHistory();

        const meeting = {
            id: Date.now(),

            filename:
                data.filename ||
                selectedFile?.name ||
                "Meeting",

            transcript:
                data.transcript || "",

            minutes:
                data.minutes || "",

            status: "Completed",

            date: new Date().toISOString()
        };

        history.unshift(meeting);

        history = history.slice(0, 50);

        localStorage.setItem(
            "meetingHistory",
            JSON.stringify(history)
        );

    } catch (error) {
        console.error(
            "Unable to save meeting history:",
            error
        );
    }
}

function getMeetingHistory() {
    try {
        const data =
            localStorage.getItem("meetingHistory");

        if (!data) return [];

        const history = JSON.parse(data);

        return Array.isArray(history)
            ? history
            : [];

    } catch (error) {
        console.error(
            "Unable to read meeting history:",
            error
        );

        return [];
    }
}

/* ================================
   PROGRESS
================================ */

function updateProgress(percentage, message) {
    const progressBar = document.querySelector(
        "#progressBar, .progress-bar"
    );

    const progressText = document.querySelector(
        "#progressText, .progress-text"
    );

    if (progressBar) {
        progressBar.style.width =
            percentage + "%";
    }

    if (progressText) {
        progressText.textContent =
            message || "";
    }
}

/* ================================
   HELPERS
================================ */

function getFileExtension(fileName) {
    const lastDot =
        fileName.lastIndexOf(".");

    if (lastDot === -1) {
        return "";
    }

    return fileName
        .substring(lastDot)
        .toLowerCase();
}

function formatFileSize(bytes) {
    if (bytes === 0) {
        return "0 Bytes";
    }

    const units = [
        "Bytes",
        "KB",
        "MB",
        "GB"
    ];

    const index = Math.floor(
        Math.log(bytes) / Math.log(1024)
    );

    return (
        bytes /
        Math.pow(1024, index)
    ).toFixed(2) +
        " " +
        units[index];
}

function wait(milliseconds) {
    return new Promise(function (resolve) {
        setTimeout(resolve, milliseconds);
    });
}

/* ================================
   TOAST MESSAGE
================================ */

function showToast(message, type = "info") {
    let container =
        document.querySelector("#toastContainer");

    if (!container) {
        container =
            document.createElement("div");

        container.id =
            "toastContainer";

        container.className =
            "toast-container";

        document.body.appendChild(container);
    }

    const toast =
        document.createElement("div");

    toast.className =
        `toast toast-${type}`;

    toast.innerHTML = `
        <span>${escapeHTML(message)}</span>
        <button type="button" aria-label="Close">
            ×
        </button>
    `;

    container.appendChild(toast);

    const closeButton =
        toast.querySelector("button");

    if (closeButton) {
        closeButton.addEventListener(
            "click",
            function () {
                toast.remove();
            }
        );
    }

    setTimeout(function () {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 5000);
}

/* ================================
   SECURITY HELPER
================================ */

function escapeHTML(value) {
    const div =
        document.createElement("div");

    div.textContent =
        value ?? "";

    return div.innerHTML;
}

/* ================================
   GLOBAL FUNCTIONS
================================ */

window.generateMeetingMinutes =
    generateMeetingMinutes;

window.removeSelectedFile =
    removeSelectedFile;

window.showToast =
    showToast;