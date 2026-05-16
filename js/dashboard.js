function showHome() {
    document.getElementById('home-section').style.display = 'block';
    document.getElementById('reports-section').style.display = 'none';
}

function showReports() {
    document.getElementById('home-section').style.display = 'none';
    document.getElementById('reports-section').style.display = 'block';
}

function openProfilePopup() {
    document.getElementById('profile-popup').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
}

function closeProfilePopup() {
    document.getElementById('profile-popup').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

function openProfileEdit() {
    document.getElementById('profile-edit').classList.add('open');
    document.getElementById('overlay').style.display = 'block';
}

function closeProfileEdit() {
    document.getElementById('profile-edit').classList.remove('open');
    document.getElementById('overlay').style.display = 'none';
}

function saveProfile() {
    const name = document.getElementById('edit-name').value;
    const email = document.getElementById('edit-email').value;
    alert(`Profile Updated!\nName: ${name}\nEmail: ${email}`);
    closeProfileEdit();
}

function deleteReport(reportId) {
    if (confirm(`Are you sure you want to delete report with ID ${reportId}?`)) {
        alert(`Report ${reportId} deleted successfully.`);
    }
}

function downloadReport(reportId) {
    alert(`Downloading report with ID ${reportId}.`);
}