// document.getElementById('isCorruptible').addEventListener('change', function () {
//     const corruptibleFields = document.getElementById('corruptibleFields');
//     corruptibleFields.classList.toggle('d-none', !this.checked);
// });

// var activePage = 1;
// var lastCompletedPage = 0;

// var requestInfo = {
//     customerName: "",
//     requestType: "",
//     date: "",
//     description: "",
//     samples: [
//         {
//             type: "",
//             name: "",
//             count: 0,
//             is_perishable: false,
//             expirationDate: "",

//         },
//     ],

// }

// // Ensure an element does have a specific class
// function ensureClass(element, className) {
//     if (!element.classList.contains(className)) {
//         element.classList.add(className);
//     }
// }

// // Ensure an element does not have a specific class
// function stripClass(element, className) {
//     while (element.classList.contains(className)) {
//         element.classList.remove(className);
//     }
// }

// // function gotoPage(pageNum) {
// //     activePage = pageNum
// //     for (let page of document.querySelectorAll(".request-page")) {
// //         if (page.dataset.index == activePage)
// //             page.style.display = "";
// //         else
// //             page.style.display = "none";
// //     }
// //     for (let step of document.querySelectorAll(".stepper .step")) {
// //         if (step.dataset.index == activePage)
// //             ensureClass(step, "active");
// //         else
// //             stripClass(step, "active");
// //     }

// // }

// document.querySelectorAll(".stepper .step").forEach(function (item) {
//     item.addEventListener("click", function () {
//         if (item.dataset.index <= lastCompletedPage+1)
//             gotoPage(item.dataset.index);
//         else {
//             var toast = new bootstrap.Toast(
//                 document.getElementById('step-warning')
//             )
//             toast.show()
//         }
//     });
// })

// document.addEventListener('DOMContentLoaded', function () {
//     gotoPage(1);

//     $('#expirationDate').persianDatepicker({
//         format: 'YYYY/MM/DD',
//         autoClose: true
//     });
// });

// document.querySelectorAll('button.page-btn').forEach(function (btn) {
//     btn.addEventListener("click", function () {
//         let step = document.querySelector(`.stepper .step[data-index='${btn.dataset.index}']`);
//         let line = document.querySelector(`.stepper .line[data-index='${btn.dataset.index}']`);

//         if (btn.classList.contains('forward-btn')) {
//             ensureClass(step, 'completed');
//             ensureClass(line, 'completed');
//             if (Number(btn.dataset.index) > lastCompletedPage)
//                 lastCompletedPage = Number(btn.dataset.index);
//             gotoPage(Number(btn.dataset.index) + 1);
//         }
//         else if (btn.classList.contains('backward-btn')) {
//             gotoPage(Number(btn.dataset.index) - 1);
//         }
//         else if (btn.classList.contains('complete-btn')) {
//             ensureClass(step, 'completed');
//         }
//     });
// });

// document.addEventListener("DOMContentLoaded", function () {
//     const testRadios = document.querySelectorAll('input[name="testType"]');
//     const parametersTableBody = document.querySelector('#parametersTableBody');
    
//     testRadios.forEach(radio => {
//         radio.addEventListener('change', function () {
//             const testId = this.value; // دریافت شناسه تست از رادیو
//             const url = "{% url 'orders:get_test_parameters' test_id=0 %}".replace(/0/, testId); // جایگزینی شناسه تست در URL
//             fetch(url) // استفاده از URL داینامیک
//                 .then(response => {
//                     if (!response.ok) {
//                         throw new Error('Network response was not ok');
//                     }
//                     return response.json();
//                 })
//                 .then(data => {
//                     parametersTableBody.innerHTML = ''; // پاک کردن پارامترهای فعلی
//                     data.parameters.forEach(parameter => {
//                         const row = `
//                             <tr>
//                                 <td class="text-center">
//                                     <input class="form-check-input" name="parameter" type="radio" value="${parameter.id}">
//                                 </td>
//                                 <td>${parameter.name}</td>
//                             </tr>
//                         `;
//                         parametersTableBody.innerHTML += row;
//                     });
//                 })
//                 .catch(error => {
//                     console.error('Error fetching parameters:', error);
//                 });
//         });
//     });
// });
