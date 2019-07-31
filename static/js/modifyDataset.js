handleUploadButton = function () {
    let label;
    let labelVal;
    let fileName = "";

    const inputs = document.querySelectorAll('.inputfile');

    Array.prototype.forEach.call(inputs, function (input) {
        label = input.nextElementSibling;
        labelVal = label.innerHTML;

        input.addEventListener('change', function (e) {
            fileName = '';
            if (this.files && this.files.length > 1) {
                fileName = (this.getAttribute('data-multiple-caption') || '').replace(
                    '{count}',
                    this.files.length);
            } else
                fileName = e.target.value.split('\\').pop();

            if (fileName) {
                label.innerHTML = fileName;
            } else
                label.innerHTML = labelVal;
        });
    });

    const wrapper = document.querySelector("#uploadBtnWrapper");
    wrapper.onclick = function () {
        inputs[0].click();
    }

};

window.onload = handleUploadButton;