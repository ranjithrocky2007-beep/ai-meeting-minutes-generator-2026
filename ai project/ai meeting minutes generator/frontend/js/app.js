javascript
"use strict";

// =====================================================
// AI MEETING MINUTES GENERATOR - APP.JS
// =====================================================

// FastAPI backend URL
const API_BASE_URL = "http://127.0.0.1:8000";

// Maximum file size = 500 MB
const MAX_FILE_SIZE = 500 * 1024 * 1024;

// Supported audio/video formats
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
let isProcessing = false;


// =====================================================
// PAGE LOAD
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    setupFileUpload();
    setupGenerateButton();
    setupRemoveButton();
    setupMobileMenu();
    setupSearch();
    setupTaskCheckboxes();

    loadMeetingHistory();

    console.log("AI Meeting Minutes Generator loaded.");

});


// =====================================================
// FILE UPLOAD
// =====================================================

function setupFileUpload() {

    const uploadArea = document.querySelector(
        "#uploadArea, .upload-area"
    );

    const fileInput = document.querySelector(
        "#fileInput"
    );

    if (!uploadArea || !fileInput) {
        return;
    }


    // Click upload area
    uploadArea.addEventListener("click", function (event) {

        if (
            event.target.closest(
                "#removeFile, .remove-file, .remove-button"
            )
        ) {
            return;
        }

        fileInput.click();

    });


    // Select file
    fileInput.addEventListener("change", function () {

        if (fileInput.files.length > 0) {

            validateAndSelectFile(
                fileInput.files[0]
            );

        }

    });


    // Drag over
    uploadArea.addEventListener("dragover", function (event) {

        event.preventDefault();

        uploadArea.classList.add("drag-over");

    });


    // Drag leave
    uploadArea.addEventListener("dragleave", function () {

        uploadArea.classList.remove("drag-over");

    });


    // Drop
    uploadArea.addEventListener("drop", function (event) {

        event.preventDefault();

        uploadArea.classList.remove("drag-over");

        const files = event.dataTransfer.files;

        if (files.length > 0) {

            validateAndSelectFile(files[0]);

        }

    });

}


// =====================================================
// VALIDATE FILE
// =====================================================

function validateAndSelectFile(file) {

    if (!file) {
        return;
    }


    const extension = getExtension(file.name);


    // Check format
    if (!ALLOWED_EXTENSIONS.includes(extension)) {

        showToast(
            "Unsupported file format.",
            "error"
        );

        return;
    }


    // Check file size
    if (file.size > MAX_FILE_SIZE) {

        showToast(
            "File size must be less than 500 MB.",
            "error"
        );

        return;
    }


    // Check empty file
    if (file.size === 0) {

        showToast(
            "The selected file is empty.",
            "error"
        );

        return;
    }


    selectedFile = file;

    displaySelectedFile(file);

    showToast(
        "Meeting file selected successfully.",
        "success"
    );

}


// =====================================================
// GET FILE EXTENSION
// =====================================================

function getExtension(fileName) {

    const lastDot =
        fileName.lastIndexOf(".");

    if (lastDot === -1) {
        return "";
    }

    return fileName
        .substring(lastDot)
        .toLowerCase();

}


// =====================================================
// DISPLAY SELECTED FILE
// =====================================================

function displaySelectedFile(file) {

    const selectedFileBox =
        document.querySelector(
            "#selectedFile, .selected-file"
        );

    if (!selectedFileBox) {
        return;
    }


    const fileName =
        selectedFileBox.querySelector(
            "#fileName, .file-name"
        );

    const fileSize =
        selectedFileBox.querySelector(
            "#fileSize, .file-size"
        );


    if (fileName) {

        fileName.textContent =
            file.name;

    }


    if (fileSize) {

        fileSize.textContent =
            formatFileSize(file.size);

    }


    selectedFileBox.style.display =
        "flex";

}


// =====================================================
// FORMAT FILE SIZE
// =====================================================

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
    ).toFixed(2)
    + " "
    + units[index];

}


// =====================================================
// REMOVE SELECTED FILE
// =====================================================

function setupRemoveButton() {

    const removeButton =
        document.querySelector(
            "#removeFile, .remove-file, .remove-button"
        );

    if (!removeButton) {
        return;
    }


    removeButton.addEventListener(
        "click",
        function (event) {

            event.preventDefault();

            event.stopPropagation();

            removeSelectedFile();

        }
    );

}


function removeSelectedFile() {

    selectedFile = null;


    const fileInput =
        document.querySelector(
            "#fileInput"
        );


    if (fileInput) {
        fileInput.value = "";
    }


    const selectedFileBox =
        document.querySelector(
            "#selectedFile, .selected-file"
        );


    if (selectedFileBox) {

        selectedFileBox.style.display =
            "none";

    }


    updateProgress(
        0,
        ""
    );

}


// =====================================================
// GENERATE BUTTON
// =====================================================

function setupGenerateButton() {

    const button =
        document.querySelector(
            "#generateButton, .generate-button, [data-generate]"
        );


    if (!button) {
        return;
    }


    button.addEventListener(
        "click",
        generateMeetingMinutes
    );

}


// =====================================================
// GENERATE MEETING MINUTES
// =====================================================

async function generateMeetingMinutes() {

    if (isProcessing) {
        return;
    }


    if (!selectedFile) {

        showToast(
            "Please select a meeting recording first.",
            "warning"
        );

        return;
    }


    isProcessing = true;


    const button =
        document.querySelector(
            "#generateButton, .generate-button, [data-generate]"
        );


    const progressBox =
        document.querySelector(
            "#uploadProgress, .upload-progress"
        );


    if (button) {

        button.disabled = true;

        button.innerHTML =
            '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';

    }


    if (progressBox) {

        progressBox.style.display =
            "block";

    }


    try {

        // Step 1
        updateProgress(
            10,
            "Uploading meeting..."
        );


        const formData =
            new FormData();

        formData.append(
            "file",
            selectedFile
        );


        // Step 2
        updateProgress(
            25,
            "Connecting to AI server..."
        );


        const response =
            await fetch(
                `${API_BASE_URL}/process-meeting`,
                {
                    method: "POST",
                    body: formData
                }
            );


        // Read response
        const data =
            await response.json();


        // Check API error
        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Meeting processing failed."
            );

        }


        // Step 3
        updateProgress(
            60,
            "Transcribing meeting..."
        );


        await wait(500);


        // Step 4
        updateProgress(
            80,
            "Generating meeting minutes..."
        );


        await wait(500);


        // Step 5
        updateProgress(
            100,
            "Completed successfully!"
        );


        // Save result
        localStorage.setItem(
            "latestMeetingResult",
            JSON.stringify(data)
        );


        saveMeetingHistory(data);


        // Display result
        displayResult(data);


        showToast(
            "Meeting minutes generated successfully!",
            "success"
        );


    } catch (error) {

        console.error(
            "Processing Error:",
            error
        );


        updateProgress(
            0,
            "Processing failed."
        );


        showToast(
            error.message ||
            "Unable to connect to backend.",
            "error"
        );


    } finally {

        isProcessing = false;


        if (button) {

            button.disabled = false;

            button.innerHTML =
                '<i class="fa-solid fa-wand-magic-sparkles"></i> Generate AI Meeting Minutes';

        }

    }

}


// =====================================================
// PROGRESS
// =====================================================

function updateProgress(
    percentage,
    message
) {

    const progressBar =
        document.querySelector(
            "#progressBar, .progress-bar"
        );


    const progressText =
        document.querySelector(
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


// =====================================================
// DISPLAY RESULT
// =====================================================

function displayResult(data) {

    const resultBox =
        document.querySelector(
            "#meetingResult, .meeting-result"
        );


    if (!resultBox) {
        return;
    }


    resultBox.style.display =
        "block";


    const transcript =
        resultBox.querySelector(
            "#transcript, .transcript"
        );


    const minutes =
        resultBox.querySelector(
            "#minutes, .minutes"
        );


    if (transcript) {

        transcript.textContent =
            data.transcript ||
            "Transcript not available.";

    }


    if (minutes) {

        if (
            typeof data.minutes ===
            "string"
        ) {

            minutes.textContent =
                data.minutes;

        } else {

            minutes.textContent =
                JSON.stringify(
                    data.minutes || {},
                    null,
                    2
                );

        }

    }


    resultBox.scrollIntoView({
        behavior: "smooth"
    });

}


// =====================================================
// MEETING HISTORY
// =====================================================

function saveMeetingHistory(data) {

    let history = getMeetingHistory();


    const meeting = {

        id: Date.now(),

        filename:
            data.filename ||
            selectedFile?.name ||
            "Meeting",

        transcript:
            data.transcript ||
            "",

        minutes:
            data.minutes ||
            "",

        status:
            "Completed",

        date:
            new Date().toISOString()

    };


    history.unshift(meeting);


    // Keep only latest 50
    history =
        history.slice(0, 50);


    localStorage.setItem(
        "meetingHistory",
        JSON.stringify(history)
    );

}


function getMeetingHistory() {

    try {

        const data =
            localStorage.getItem(
                "meetingHistory"
            );


        if (!data) {
            return [];
        }


        const history =
            JSON.parse(data);


        return Array.isArray(history)
            ? history
            : [];

    } catch (error) {

        console.error(
            "History Error:",
            error
        );

        return [];

    }

}


// =====================================================
// LOAD HISTORY
// =====================================================

function loadMeetingHistory() {

    const container =
        document.querySelector(
            "#meetingHistory, .meeting-history"
        );


    if (!container) {
        return;
    }


    const history =
        getMeetingHistory();


    if (history.length === 0) {

        container.innerHTML = `
            <div class="empty-state">
                <i class="fa-regular fa-calendar"></i>
                <h3>No meetings found</h3>
                <p>Your processed meetings will appear here.</p>
            </div>
        `;

        return;
    }


    container.innerHTML = "";


    history.forEach(function (meeting) {

        const item =
            document.createElement("div");


        item.className =
            "history-item";


        item.innerHTML = `
            <div>
                <h4>${escapeHTML(meeting.filename)}</h4>
                <small>
                    ${formatDate(meeting.date)}
                </small>
            </div>

            <span class="status completed">
                ${escapeHTML(meeting.status)}
            </span>
        `;


        container.appendChild(item);

    });

}


// =====================================================
// SEARCH
// =====================================================

function setupSearch() {

    const searchInput =
        document.querySelector(
            "#searchInput, .search-input"
        );


    if (!searchInput) {
        return;
    }


    searchInput.addEventListener(
        "input",
        function () {

            const keyword =
                searchInput.value
                    .trim()
                    .toLowerCase();


            const items =
                document.querySelectorAll(
                    ".meeting-row, .history-item, [data-search-item]"
                );


            items.forEach(function (item) {

                const text =
                    item.textContent
                        .toLowerCase();


                item.style.display =
                    !keyword ||
                    text.includes(keyword)
                        ? ""
                        : "none";

            });

        }
    );

}


// =====================================================
// MOBILE SIDEBAR
// =====================================================

function setupMobileMenu() {

    const menuButton =
        document.querySelector(
            ".mobile-menu, [data-menu='true']"
        );


    const sidebar =
        document.querySelector(
            ".sidebar"
        );


    if (!menuButton || !sidebar) {
        return;
    }


    menuButton.addEventListener(
        "click",
        function () {

            sidebar.classList.toggle(
                "open"
            );

        }
    );

}


// Global function
function toggleSidebar() {

    const sidebar =
        document.querySelector(
            ".sidebar"
        );


    if (sidebar) {

        sidebar.classList.toggle(
            "open"
        );

    }

}


// =====================================================
// ACTION ITEMS
// =====================================================

function setupTaskCheckboxes() {

    const checkboxes =
        document.querySelectorAll(
            "input[type='checkbox'][data-task], .task-checkbox"
        );


    checkboxes.forEach(function (checkbox) {

        checkbox.addEventListener(
            "change",
            function () {

                const task =
                    checkbox.closest(
                        ".task-item, .action-item"
                    );


                if (task) {

                    task.classList.toggle(
                        "completed",
                        checkbox.checked
                    );

                }

            }
        );

    });

}


// =====================================================
// TOAST
// =====================================================

function showToast(
    message,
    type = "info"
) {

    let container =
        document.querySelector(
            "#toastContainer"
        );


    if (!container) {

        container =
            document.createElement(
                "div"
            );

        container.id =
            "toastContainer";

        container.className =
            "toast-container";

        document.body.appendChild(
            container
        );

    }


    const toast =
        document.createElement(
            "div"
        );


    toast.className =
        `toast toast-${type}`;


    toast.innerHTML = `
        <span>${escapeHTML(message)}</span>
        <button type="button">×</button>
    `;


    container.appendChild(
        toast
    );


    const close =
        toast.querySelector(
            "button"
        );


    close.addEventListener(
        "click",
        function () {

            toast.remove();

        }
    );


    setTimeout(function () {

        if (toast.parentNode) {

            toast.remove();

        }

    }, 5000);

}


// =====================================================
// HELPERS
// =====================================================

function wait(milliseconds) {

    return new Promise(function (resolve) {

        setTimeout(
            resolve,
            milliseconds
        );

    });

}


function formatDate(date) {

    try {

        return new Date(
            date
        ).toLocaleString();

    } catch (error) {

        return "";

    }

}


function escapeHTML(value) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        value ?? "";

    return div.innerHTML;

}


// =====================================================
// GLOBAL EXPORTS
// =====================================================

window.toggleSidebar =
    toggleSidebar;

window.removeSelectedFile =
    removeSelectedFile;

window.generateMeetingMinutes =
    generateMeetingMinutes;

window.showToast =
    showToast;

window.loadMeetingHistory =
    loadMeetingHistory;