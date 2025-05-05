function uploadImage(files) {
    if (!files.length) return;

    const preview = document.getElementById("preview");
    const result = document.getElementById("resultImage");
    const colorInfo = document.getElementById("colorInfo");

    preview.src = URL.createObjectURL(files[0]);
    preview.style.display = "block";

    const formData = new FormData();
    formData.append("image", files[0]);

    fetch("/analyze", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const color = data.dominant_color;
        const colorName = data.color_name;
        const [r, g, b] = color;

        colorInfo.textContent = `Dominante Farbe (RGB): (${r}, ${g}, ${b}) – ${colorName}`;

        const colorImg = `/colorbox?r=${r}&g=${g}&b=${b}`;
        result.src = colorImg;
        result.style.display = "block";
    })
    .catch(error => {
        console.error("Fehler:", error);
    });
}
