// vars

const dataTransfer = new DataTransfer();
if (
  ["company", "level", "focus", "device", "events", "challenge"].includes(window.thisPage)
) {
  let result = document.querySelector(".result"),
    img_result = document.querySelector(".img-result"),
    img_w = document.querySelector(".img-w"),
    img_h = document.querySelector(".img-h"),
    options = document.querySelector(".options"),
    save = document.querySelector(".save"),
    preview = document.querySelector(".preview"),
    cropped = document.querySelector("#image-div-input-preview"),
    dwn = document.querySelector(".download"),
    upload = document.querySelector("#file-input"),
    cropper = "";

  // on change show image with crop options
  upload.addEventListener("change", (e) => {
    if (e.target.files.length) {
      // start file reader
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target.result) {
          // create new image
          let img = document.createElement("img");
          img.id = "image";
          img.src = e.target.result;
          // clean result before
          result.innerHTML = "";
          // append new image
          result.appendChild(img);
          // show save btn and options
          save.classList.remove("hide");
          options.classList.remove("hide");
          // init cropper
          if (window.thisPage === "company") {
            cropper = new Cropper(img, {
              aspectRatio: 1, // Change this to your desired aspect ratio
              viewMode: 1, // Optional: You can set the view mode as needed
              autoCropArea: 1,
            });
          } else {
            cropper = new Cropper(img, {
              // NOTE: To provide a free cropping option, set aspectRatio to NaN.
              // aspectRatio: 343 / 110, // Change this to your desired aspect ratio
              viewMode: 1, // Optional: You can set the view mode as needed
            });
          }
        }
      };
      reader.readAsDataURL(e.target.files[0]);
    }
  });

  // save on click
  save.addEventListener("click", (e) => {
    e.preventDefault();
    // get result to data uri
    let imgSrc = cropper.getCroppedCanvas().toDataURL();
    cropper.getCroppedCanvas().toBlob((blob) => {
      if (blob) {
        // Create a File object from the Blob
        const file = new File([blob], "cropped-image.jpg", {
          type: "image/jpeg",
        });

        dataTransfer.items.add(file);
        upload.files = dataTransfer.files;
        if (dataTransfer1) {
          dataTransfer1.items.add(file);
        }

        // You can upload or do further processing with the "file" object
      }
    }, "image/jpeg");
    // remove hide class of img
    cropped.classList.remove("hide");
    img_result.classList.remove("hide");
    // show image cropped
    cropped.src = imgSrc;
    if (window.challengeFeature) {
      window.imageSelected += 1;
      $("#image-counter").html(
        window.imageSelected > 0 ? window.imageSelected : 0
      );
    }

    $(".image-cropper-popup").removeClass("model-open");
  });

  preview?.addEventListener("click", (e) => {
    e.preventDefault();
    // get result to data uri
    let imgSrc = cropper.getCroppedCanvas().toDataURL();
    cropper.getCroppedCanvas().toBlob((blob) => {
      if (blob) {
        // Create a File object from the Blob
        const file = new File([blob], "cropped-image.jpg", {
          type: "image/jpeg",
        });

        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        upload.files = dataTransfer.files;

        // You can upload or do further processing with the "file" object
      }
    }, "image/jpeg");
    // remove hide class of img
    cropped.classList.remove("hide");
    img_result.classList.remove("hide");
    // show image cropped
    cropped.src = imgSrc;
  });
}
