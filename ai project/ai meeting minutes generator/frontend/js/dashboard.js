javascript
"use strict";

// =====================================================
// AI MEETING MINUTES GENERATOR
// DASHBOARD.JS
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    initializeDashboard();
    initializeMobileMenu();
    initializeSearch();
    initializeActionItems();
    initializeQuickActions();
    loadDashboardData();

    console.log("Dashboard loaded successfully.");

});


// =====================================================
// DASHBOARD INITIALIZATION
// =====================================================

function initializeDashboard() {

    updateGreeting();
    updateDashboardStats();
    loadRecentMeetings();
    loadPendingActions();

}


// =====================================================
// GREETING
// =====================================================

function updateGreeting() {

    const greetingElement =
        document.querySelector(
            "#dashboardGreeting, .dashboard-greeting"
        );

    if (!greetingElement) {
        return;
    }


    const hour = new Date().getHours();

    let greeting = "Good Evening";

    if (hour < 12) {
        greeting = "Good Morning";
    }
    else if (hour < 17) {
        greeting = "Good Afternoon";
    }


    greetingElement.textContent =
        greeting + ", Ranjith 👋";

}


// =====================================================
// DASHBOARD DATA
// =====================================================

function loadDashboardData() {

    const history =
        getMeetingHistory();

    console.log(
        "Meetings available:",
        history.length
    );

}


// =====================================================
// DASHBOARD STATISTICS
// =====================================================

function updateDashboardStats() {

    const history =
        getMeetingHistory();


    // Total meetings
    const totalMeetings =
        history.length;


    updateElement(
        "#totalMeetings",
        totalMeetings
    );


    // Total action items
    const actionItems =
        getActionItems();


    updateElement(
        "#totalActionItems",
        actionItems.length
    );


    // Minutes generated
    updateElement(
        "#minutesGenerated",
        history.length
    );


    // Meeting hours
    calculateMeetingHours(history);

}


// =====================================================
// MEETING HOURS
// =====================================================

function calculateMeetingHours(history) {

    const element =
        document.querySelector(
            "#meetingHours"
        );

    if (!element) {
        return;
    }


    // Demo calculation
    // If duration is available, use it.
    let totalMinutes = 0;


    history.forEach(function (meeting) {

        if (meeting.duration) {

            totalMinutes +=
                Number(meeting.duration);

        }

    });


    const hours =
        totalMinutes / 60;


    if (totalMinutes > 0) {

        element.textContent =
            hours.toFixed(1) + "h";

    }
    else {

        element.textContent =
            "0h";

    }

}


// =====================================================
// RECENT MEETINGS
// =====================================================

function loadRecentMeetings() {

    const container =
        document.querySelector(
            "#recentMeetings, .recent-meetings"
        );


    if (!container) {
        return;
    }


    const history =
        getMeetingHistory();


    const recent =
        history.slice(0, 5);


    if (recent.length === 0) {

        container.innerHTML = `
            <div class="empty-state">
                <i class="fa-regular fa-calendar"></i>
                <h3>No meetings yet</h3>
                <p>
                    Upload your first meeting to generate AI minutes.
                </p>
            </div>
        `;

        return;
    }


    container.innerHTML = "";


    recent.forEach(function (meeting) {

        const row =
            document.createElement("div");


        row.className =
            "meeting-row";


        row.setAttribute(
            "data-search-item",
            ""
        );


        row.innerHTML = `
            <div class="meeting-info">
                <div class="meeting-icon">
                    <i class="fa-solid fa-microphone"></i>
                </div>

                <div>
                    <h4>
                        ${escapeHTML(meeting.filename)}
                    </h4>

                    <span>
                        ${formatDate(meeting.date)}
                    </span>
                </div>
            </div>

            <div class="meeting-status">
                <span class="status completed">
                    ${escapeHTML(meeting.status)}
                </span>
            </div>
        `;


        container.appendChild(row);

    });

}


// =====================================================
// MEETING HISTORY
// =====================================================

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

    }
    catch (error) {

        console.error(
            "Unable to read meeting history:",
            error
        );

        return [];

    }

}


// =====================================================
// ACTION ITEMS
// =====================================================

function getActionItems() {

    try {

        const data =
            localStorage.getItem(
                "actionItems"
            );


        if (!data) {
            return [];
        }


        const actions =
            JSON.parse(data);


        return Array.isArray(actions)
            ? actions
            : [];

    }
    catch (error) {

        return [];

    }

}


// =====================================================
// PENDING ACTION ITEMS
// =====================================================

function loadPendingActions() {

    const container =
        document.querySelector(
            "#pendingActions, .pending-actions"
        );


    if (!container) {
        return;
    }


    const actions =
        getActionItems();


    const pending =
        actions.filter(function (action) {

            return !action.completed;

        });


    if (pending.length === 0) {

        container.innerHTML = `
            <div class="empty-state">
                <i class="fa-solid fa-circle-check"></i>
                <h3>All caught up!</h3>
                <p>No pending action items.</p>
            </div>
        `;

        return;
    }


    container.innerHTML = "";


    pending
        .slice(0, 5)
        .forEach(function (action, index) {

            const item =
                document.createElement("div");


            item.className =
                "action-item";


            item.innerHTML = `
                <label>
                    <input
                        type="checkbox"
                        class="dashboard-task"
                        data-index="${index}"
                    >

                    <span>
                        ${escapeHTML(
                            action.title ||
                            action.text ||
                            "Action item"
                        )}
                    </span>
                </label>
            `;


            container.appendChild(item);

        });


    initializeActionItems();

}


// =====================================================
// ACTION ITEM CHECKBOX
// =====================================================

function initializeActionItems() {

    const checkboxes =
        document.querySelectorAll(
            ".dashboard-task"
        );


    checkboxes.forEach(function (checkbox) {

        checkbox.addEventListener(
            "change",
            function () {

                const item =
                    checkbox.closest(
                        ".action-item"
                    );


                if (item) {

                    item.classList.toggle(
                        "completed",
                        checkbox.checked
                    );

                }


                updateDashboardStats();

            }
        );

    });

}


// =====================================================
// SEARCH
// =====================================================

function initializeSearch() {

    const searchInput =
        document.querySelector(
            "#dashboardSearch, #searchInput, .search-input"
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
                    "[data-search-item], .meeting-row"
                );


            items.forEach(function (item) {

                const text =
                    item.textContent
                        .toLowerCase();


                if (
                    keyword === "" ||
                    text.includes(keyword)
                ) {

                    item.style.display = "";

                }
                else {

                    item.style.display = "none";

                }

            });

        }
    );

}


// =====================================================
// MOBILE SIDEBAR
// =====================================================

function initializeMobileMenu() {

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


// Global sidebar function
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
// QUICK ACTIONS
// =====================================================

function initializeQuickActions() {

    const newMeetingButtons =
        document.querySelectorAll(
            "[data-new-meeting]"
        );


    newMeetingButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    window.location.href =
                        "meeting.html";

                }
            );

        }
    );


    const historyButtons =
        document.querySelectorAll(
            "[data-history]"
        );


    historyButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    window.location.href =
                        "history.html";

                }
            );

        }
    );


    const analyticsButtons =
        document.querySelectorAll(
            "[data-analytics]"
        );


    analyticsButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    window.location.href =
                        "analytics.html";

                }
            );

        }
    );

}


// =====================================================
// UPDATE ELEMENT
// =====================================================

function updateElement(
    selector,
    value
) {

    const element =
        document.querySelector(
            selector
        );


    if (element) {

        element.textContent =
            value;

    }

}


// =====================================================
// DATE FORMAT
// =====================================================

function formatDate(date) {

    try {

        return new Date(
            date
        ).toLocaleString();

    }
    catch (error) {

        return "";

    }

}


// =====================================================
// HTML SECURITY
// =====================================================

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
// REFRESH DASHBOARD
// =====================================================

function refreshDashboard() {

    updateDashboardStats();
    loadRecentMeetings();
    loadPendingActions();

}


// =====================================================
// GLOBAL FUNCTIONS
// =====================================================

window.toggleSidebar =
    toggleSidebar;

window.refreshDashboard =
    refreshDashboard;

window.loadRecentMeetings =
    loadRecentMeetings;

window.loadPendingActions =
    loadPendingActions;