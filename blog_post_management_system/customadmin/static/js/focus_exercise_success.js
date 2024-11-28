const createAccordion = (counter) => {
  return `
  <div class="accordion-item custom-accordion-item " id="exer-accordion-${counter}">
  <h2 class="accordion-header">
    <button
      class="accordion-button collapsed"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#exer-${counter}"
      aria-expanded="true"
      aria-controls="collapseOne"
    >
      Exercise
    </button>
  </h2>
  <div
    id="exer-${counter}"
    class="accordion-collapse collapse"
    aria-labelledby="headingOne"
    data-bs-parent="#accordionExample"
  >
    <div class="accordion-body">
      <div class="row">
        <div class="col-lg-12 col-md-12">
          <div class="rw_form_inputs">
            <label class="rw_form_label">Name</label>
            <div class="rw_input">
            <input type="text" name="form-${
              counter - 1
            }-name" maxlength="15" id="id_form-${counter}-name">
              <span class="text-danger"></span>
            </div>
          </div>
        </div>
        <div class="col-lg-6 col-md-6">
          <div class="rw_form_inputs trigger">
            <label class="rw_form_label" for="ex-image-${counter}"
              >Image &nbsp; (only jpeg, png, jpg allowed)</label
            >
            <div
              class="rw_input img-preview-div"
              id="${counter}"
              onclick="triggerInput(this,'ex-image-${counter}')"
            >
              <input
                type="file"
                hidden
                name="form-${counter - 1}-image"
                accept=".png, .jpg, .jpeg"
                id="ex-image-${counter}"
                onchange="handleChange(this)"
              />
              <img
                id="image-div-input-preview"
                src="{{ex_forms.image.value.url}}"
                alt=""
              />
            </div>
            <span id="image-error" class="text-danger">
              
            </span>
          </div>
          <span id="image-error-1" class="text-danger"> </span>
        </div>
        <div class="col-lg-6 col-md-6">
          <div class="rw_form_inputs">
            <label class="rw_form_label">Description</label>
            <div class="rw_input">
            <textarea class="form-control w-100" name="form-${
              counter - 1
            }-description" cols="65" rows="10" id="id_form-${
    counter - 1
  }-description"></textarea>
              <span class="text-danger">  </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div onclick="removeExercise('exer-accordion-${counter}')" class="btn remove-ex-btn"><i class="fa fa-1x fa-circle-xmark" style="color: #ed7844"></i></div>
</div>

    `;
};
