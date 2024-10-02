// import "./jquery-3.6.0.min.js";
// import "./persian-date.min.js";
// import "./persian-datepicker.min.js";

// (function () {

var startPage = 1;
var activePage = 1;
var lastCompletedPage = 0;

var samples = [];

var requestOptions = undefined;

function updateRequestInfo() {
	$("#customerName").val(requestOptions.userName);
	$("#requestDate").val(requestOptions.currentDate);
	$("h5.lab-name").text(`آزمایشگاه : ${requestOptions.labName}`);

	$("#sampleType").html(`
    <option value="" selected disabled> انتخاب کنید...</option>
    `);
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
			var toast = new bootstrap.Toast(
				document.getElementById("step-warning")
			);
			toast.show();
		}
	});
});

document.addEventListener("DOMContentLoaded", function () {
	gotoPage(startPage);
	// setTimeout(function () {
	// 	$(".request-page[data-index='1'] .page-btn.forward-btn").click();
	// }, 200);

	$("#sampleExpirationDate").persianDatepicker({
		format: "YYYY/MM/DD",
		autoClose: true,
	});

	$.ajax({
		method: "get",
		// url: `${window.location.origin}/services/services-api/${experimentId}?format=json`,
		url: `/static/dummy-json-data/0.json`,
		success: function (data, textStatus, xhr) {
			requestOptions = data;
			requestOptions["requestId"] = requestOptions["newRequestId"];
			delete requestOptions["newRequestId"];
			updateRequestInfo();
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

function pageCompleteRoutine() {
	switch (activePage) {
		case 1:
			if (requestOptions == undefined) return false;
			else {
				loadSampleTypes();
				return true;
			}
			break;
		case 2:
			return samples.length > 0;
			break;
		case 3:
			break;
		case 4:
			break;
	}
}
$("button.page-btn").each(function (index, btn) {
	$(btn).on("click", function () {
		const I = Number(btn.dataset.index);
		let step = $(`.stepper .step[data-index='${I}']`);
		let line = $(`.stepper .line[data-index='${I}']`);

		if ($(btn).hasClass("forward-btn")) {
			if (!pageCompleteRoutine()) {
				new bootstrap.Toast($("#no-sample-warning")).show();
				return;
			}

			$(step).addClass("completed");
			$(line).addClass("completed");
			if (I > lastCompletedPage) lastCompletedPage = Number(I);
			gotoPage(I + 1);
		} else if (btn.classList.contains("backward-btn")) {
			gotoPage(I - 1);
		} else if (btn.classList.contains("complete-btn")) {
			$(step).addClass("completed");
		}
	});
});

function loadSampleTypes() {
	$.ajax({
		method: "get",
		url: `/static/dummy-json-data/1.json`,
		success: function (data, textStatus, xhr) {
			$("#sampleType").html(`
        <option value="" selected disabled>انتخاب کنید...</option>
        `);
			for (sampleType of data) {
				$("#sampleType").append(`
          <option value="${sampleType.Id}">${sampleType.Name}</option>
          `);
			}
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
}

// sample creation
$("#save-button").on("click", function () {
	var sampleFields = document.querySelectorAll(
		"form#sample-form *[data-field]:not([data-conditionalvalidate='false'])"
	);
	let vwt = new bootstrap.Toast(document.getElementById("validation-warning"));
	let dfet = new bootstrap.Toast(document.getElementById("data-fetch-error"));
	let newSample = {};
	let validationResult = true;
	for (let field of sampleFields) {
		if (validateField(field) !== true) {
			validationResult = false;
		}
	}
	if (!validationResult) {
		vwt.show();
		return;
	}

	var formData = new FormData();
	for (let field of sampleFields) {
		if (field.type == "file") newSample[field.id] = field.files[0];
		else if (field.type == "checkbox") newSample[field.id] = field.checked;
		else newSample[field.id] = field.value;
		formData.append(field.id, newSample[field.id]); // String field
	}

	// console.log(Array.from(formData.entries()));
	// return;
	// console.log("check 1");
	$.ajax({
		url: `/static/dummy-json-data/2.json`,
		type: "POST",
		data: formData,
		processData: false, // Important to avoid jQuery processing the data
		contentType: false, // Important to avoid jQuery setting content type
		success: function (response) {
			if (response.sampleId) {
				newSample.sid = response.sampleId;
			} else {
				dfet.show()
			}
		},
		error: function (xhr, status, error) {
			dfet.show()
		},
	}).then(function(){
		samples.push(newSample);
		resetSampleForm();
		updateSamplesView();
	});

	
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
	samples.forEach((sample) => {
		$("#samples-table tbody").append(`
        <tr>
            <td>${sample.sid}</td>
            <td>${getSampleTypeByTypeId(sample.sampleType)}</td>
            <td>${sample.sampleName}</td>
            <td>${sample.sampleCount}</td>
            <td>${sample["sample-isPerishable"] ? "بله" : "خیر"}</td>
            <td></td>
            <td>
                <button type="button" class="btn btn-danger rounded" onclick='deleteSample(${
					sample.sid
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
	samples.forEach((sample) => {
		$("#samples-dropdown").append(
			`<option value="${sample.sid}" >${
				sample.sampleName +
				" _ " +
				getSampleTypeByTypeId(sample.sampleType)
			}</option>`
		);
	});
}

function getSampleTypeByTypeId(id) {
	return $(`select#sampleType option[value=${id}]`).text();
}

function deleteSample(sampleId) {
	let contin = true;
	samples.forEach((sample, index) => {
		if (contin && sample.sid == sampleId) {
			samples.splice(index);
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
	console.log("samples:", samples);
	console.log("options:", requestOptions);
});

// })();
