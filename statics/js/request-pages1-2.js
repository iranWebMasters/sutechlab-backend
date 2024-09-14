// import "./jquery-3.6.0.min.js";
// import "./persian-date.min.js";
// import "./persian-datepicker.min.js";

// (function () {

var startPage = 1;
var activePage = 1;
var lastCompletedPage = 0;

var requestInfo = {
  customerName: "",
  requestType: "",
  requestDate: "",
  requestDescription: "",
  samples: [
    /*
      {

        sampleType: "",
        sampleName: "",
        sampleCount: 0,
        sample-isPerishable: false,
        sampleExpirationDate: "",
        sampleStorageDuration: "",
        sampleStorageDurationUnit: "", // d m y
        sampleDescription: "",
        sampleStorageConditions: "",
        sampleFile: 
      },
      */
  ],

  tests: [
    {
      sampleId: "",
    },
  ],
};

var requestOptions = undefined;

function updateRequestOptions() {
  $("#customerName").val(requestOptions.full_name);
  $("#requestDate").val(requestOptions.date);
  $("#requestType").val(requestOptions.request_type);

  $("#sampleType").html("");
  $("#sampleType").append(
    '<option value="" selected disabled>انتخاب کنید...</option>'
  );
  for (let sm of requestOptions.samples) {
    $("#sampleType").append(`<option value="${sm.id}">${sm.name}</option>`);
  }
}

// Ensure an element does have a specific class
function ensureClass(element, className) {
  if (!element.classList.contains(className)) {
    element.classList.add(className);
  }
}

// Ensure an element does not have a specific class
function stripClass(element, className) {
  while (element.classList.contains(className)) {
    element.classList.remove(className);
  }
}

function gotoPage(pageNum) {
  activePage = pageNum;
  for (let page of document.querySelectorAll(".request-page")) {
    if (page.dataset.index == activePage) page.style.display = "";
    else page.style.display = "none";
  }
  for (let step of document.querySelectorAll(".stepper .step")) {
    if (step.dataset.index == activePage) ensureClass(step, "active");
    else stripClass(step, "active");
  }
}

document.querySelectorAll(".stepper .step").forEach(function (step) {
  step.addEventListener("click", function () {
    if (step.dataset.index <= lastCompletedPage + 1)
      gotoPage(step.dataset.index);
    else {
      var toast = new bootstrap.Toast(document.getElementById("step-warning"));
      toast.show();
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  gotoPage(startPage);

  $("#sampleExpirationDate").persianDatepicker({
    format: "YYYY/MM/DD",
    autoClose: true,
  });

  $.ajax({
    method: "get",
    url: `${window.location.origin}/services/services-api/${experimentId}?format=json`,
    data: { experimentId: experimentId },
    success: function (data, textStatus, xhr) {
      requestOptions = data;
      updateRequestOptions();
    },
    error: function (xhr, textStatus, errorThrown) {
      var toastElement = $("#data-fetch-error");
      var toast = new bootstrap.Toast(toastElement);
      toast.show();
    },
    complete: function (xhr, textStatus) {
      // console.log("Request completed:", textStatus);
    },
  });

  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

function completePage() {
  switch (activePage) {
    case 1:
      let inputs = document.querySelectorAll(
        ".request-page[data-index='1'] *[data-field]"
      );
      for (let field of inputs) {
        requestInfo[field.id] = field.value;
      }
      return true;
      break;
    case 2:
      return requestInfo.samples.length;
      break;
    case 3:
      break;
    case 4:
      break;
  }
}
document.querySelectorAll("button.page-btn").forEach(function (btn) {
  btn.addEventListener("click", function () {
    const I = Number(btn.dataset.index);
    let step = document.querySelector(`.stepper .step[data-index='${I}']`);
    let line = document.querySelector(`.stepper .line[data-index='${I}']`);

    if (btn.classList.contains("forward-btn")) {
      if (!completePage()) {
        new bootstrap.Toast($("#no-sample-warning")).show();
        return;
      }

      ensureClass(step, "completed");
      ensureClass(line, "completed");
      if (I > lastCompletedPage) lastCompletedPage = Number(I);
      gotoPage(I + 1);
    } else if (btn.classList.contains("backward-btn")) {
      gotoPage(I - 1);
    } else if (btn.classList.contains("complete-btn")) {
      ensureClass(step, "completed");
    }
  });
});

// sample creation
document.querySelector("#save-button").addEventListener("click", function () {
  var sampleFields = document.querySelectorAll(
    "form#sample-form *[data-field]:not([data-conditionalvalidate='false'])"
  );
  let newSample = {};
  let validationResult = true;
  for (let field of sampleFields) {
    if (validateField(field) !== true) {
      let t = new bootstrap.Toast(
        document.getElementById("validation-warning")
      );
      t.show();
      validationResult = false;
    }
  }
  if (!validationResult) return;
  for (let field of sampleFields) {
    if (field.type == "file") newSample[field.id] = field.files[0];
    else if (field.type == "checkbox") newSample[field.id] = field.checked;
    else newSample[field.id] = field.value;
  }
  let i = 1;
  while (requestInfo.samples[i] !== undefined) i++;
  newSample.id = i;
  requestInfo.samples.push(newSample);
  resetSampleForm();
  updateSamplesView();
});

function validateField(field) {
  if (
    [
      "sampleType",
      "sampleName",
      "sampleDescription",
      "sampleStorageConditions",
      "sampleExpirationDate",
    ].includes(field.id)
  ) {
    if (field.value === "") {
      setFieldErrorMessage(field, "این فیلد را پر کنید");
      return false;
    } else clearValidationErrors(field);
  } else if (["sampleCount", "sampleStorageDuration"].includes(field.id)) {
    if (isNaN(field.value) || Number(field.value) <= 0) {
      setFieldErrorMessage(field, "مقدار فیلد صحیح نیست");
    } else clearValidationErrors(field);
  } else if (["sampleStorageDurationUnit"].includes(field.id)) {
    if (!["روز", "ماه", "سال"].includes(field.value))
      setFieldErrorMessage(field, "مقدار فیلد صحیح نیست");
  }
  return true;
}

$("#sample-isPerishable").on("change", function () {
  $("[data-conditionalvalidate]")
    .toArray()
    .forEach((field) => {
      field.dataset.conditionalvalidate = this.checked ? "true" : "false";
    });
  const corruptibleFields = $("#corruptibleFields")[0];
  if (!this.checked) ensureClass(corruptibleFields, "d-none");
  else stripClass(corruptibleFields, "d-none");
});

function updateSamplesView() {
  $("#samples-table tbody").html("");
  requestInfo.samples.forEach((sample) => {
    $("#samples-table tbody").append(`
        <tr>
            <td>${sample.id}</td>
            <td>${getSampleTypeByTypeId(sample.sampleType)}</td>
            <td>${sample.sampleName}</td>
            <td>${sample.sampleCount}</td>
            <td>${sample["sample-isPerishable"] ? "بله" : "خیر"}</td>
            <td></td>
            <td>
                <button type="button" class="btn btn-danger rounded" onclick='deleteSample(${
                  sample.id
                })' data-bs-toggle="tooltip" data-bs-placement="top" title="حذف نمونه">
                    <span class="item-delete"></span>
                </button>
            </td>
        </tr>
        `);
  });

  $("#samples-dropdown").html(
    '<option value="" selected disabled>انتخاب کنید...</option>'
  );
  requestInfo.samples.forEach((sample) => {
    $("#samples-dropdown").append(
      `<option value="${sample.id}" >${
        sample.sampleName + " _ " + getSampleTypeByTypeId(sample.sampleType)
      }</option>`
    );
  });
}

function getSampleTypeByTypeId(id) {
  return $(`select#sampleType option[value=${id}]`).text();
}

function deleteSample(sampleId) {
  let contin = true;
  requestInfo.samples.forEach((sample, index) => {
    if (contin && sample.id == sampleId) {
      requestInfo.samples.splice(index);
      contin = false;
    }
  });
  updateSamplesView();
}

function clearValidationErrors(field) {
  field.nextElementSibling.innerHTML = "";
}

function setFieldErrorMessage(field, message) {
  field.nextElementSibling.innerHTML = `<li class="text-danger"><strong>${message}</strong></li>`;
}

function resetSampleForm() {
  $("form#sample-form")[0].reset();
  $("#sample-isPerishable").prop("checked", false).trigger("change");
}

$(document).dblclick(function (event) {
  console.log(requestInfo);
});

// })();
