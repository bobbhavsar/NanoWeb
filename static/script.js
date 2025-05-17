function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("mainContent");
    const openBtn = document.getElementById("openBtn");

    if (sidebar.style.width === "250px") {
        // CLOSE
        sidebar.style.width = "0";
        mainContent.style.marginRight = "0";
        openBtn.style.display = "inline-block";
    } else {
        // OPEN
        sidebar.style.width = "250px";
        mainContent.style.marginRight = "250px";
        openBtn.style.display = "none";
    }
}
