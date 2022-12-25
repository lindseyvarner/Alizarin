(function () {

    const form = document.getElementById("task-add");
    const textarea = document.getElementById("description");
    const description = document.getElementById("editable-description");

    form.onsubmit = (e) => {
       textarea.value = description.innerHTML;
    };

    form.onkeyup = ((e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
             e.preventDefault();
             textarea.value = description.innerHTML;
             form.submit()
        }
    })
})();

