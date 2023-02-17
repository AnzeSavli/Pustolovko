document.querySelectorAll("#level-button").forEach((val) => {
    console.log("TEST");
    val.onclick = (e) => {
        window.location.href = "/" + val.value;
    };
});
