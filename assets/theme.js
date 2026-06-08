window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_theme: function(theme) {
            if (theme === "dark") {
                document.body.classList.remove("theme-light");
                document.body.classList.add("theme-dark");
            } else {
                document.body.classList.remove("theme-dark");
                document.body.classList.add("theme-light");
            }
            return "theme-" + theme;
        }
    }
});
