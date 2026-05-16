// Show selected file name and preview image
document.getElementById("fileInput").addEventListener("change", function () {
    const fileInput = this;
    const fileName = fileInput.files[0]?.name || "No file chosen";
    document.getElementById("fileName").textContent = fileName;

    const previewContainer = document.getElementById("livePreview");
    const previewImage = document.getElementById("imagePreview");
    const file = fileInput.files[0];

    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;
            previewContainer.style.display = "block";
        };
        reader.readAsDataURL(file);
    } else {
        previewImage.src = "#";
        previewContainer.style.display = "none";
    }
});