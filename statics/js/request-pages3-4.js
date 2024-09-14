const testsData = [
    {
        id: 1,
        name: 'آون',
        standards: [
            {
                id: 1,
                name: 'DIN 7-1214-3004',
                parameters: [
                    { id: 1, name: 'دما', unit: 'درجه سانتی گراد ( C )', testUnit: 'دقیقه ( min )', tariff: '10000 (ریال)' },
                    { id: 2, name: 'زمان', unit: 'ساعت ( h )', testUnit: 'دقیقه ( min )', tariff: '5000 (ریال)' }
                ]
            },
            {
                id: 2,
                name: 'ISO 1234-5678',
                parameters: [
                    { id: 3, name: 'رطوبت', unit: 'درصد ( % )', testUnit: 'ساعت ( h )', tariff: '15000 (ریال)' }
                ]
            }
        ]
    },
    // Add more tests as needed
];

function createTestElement(test) {
    const testDiv = document.createElement('div');
    testDiv.className = 'mb-4';
    testDiv.innerHTML = `
            <div class="form-check">
                <input class="form-check-input" type="checkbox" id="test${test.id}" onchange="toggleStandards(${test.id})">
                <label class="form-check-label" for="test${test.id}">${test.name}</label>
            </div>
            <div id="standards${test.id}" class="ms-4 mt-2" style="display: none;">
                ${test.standards.map(standard => `
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="standard${test.id}" id="standard${standard.id}" onchange="showParameters(${test.id}, ${standard.id})">
                        <label class="form-check-label" for="standard${standard.id}">${standard.name}</label>
                    </div>
                `).join('')}
            </div>
            <div id="parameters${test.id}" class="ms-5 mt-2"></div>
        `;
    return testDiv;
}

function toggleStandards(testId) {
    const standardsDiv = document.getElementById(`standards${testId}`);
    standardsDiv.style.display = standardsDiv.style.display === 'none' ? 'block' : 'none';
    if (standardsDiv.style.display === 'none') {
        document.getElementById(`parameters${testId}`).innerHTML = '';
    }
}

function showParameters(testId, standardId) {
    const test = testsData.find(t => t.id === testId);
    const standard = test.standards.find(s => s.id === standardId);
    const parametersDiv = document.getElementById(`parameters${testId}`);
    parametersDiv.innerHTML = `
            <h6 class="mb-2">پارامتر های آزمون</h6>
            <table class="table table-bordered">
                <thead class="table-primary">
                    <tr>
                        <th>انتخاب</th>
                        <th>نام پارامتر</th>
                        <th>واحد اندازه گیری پارامتر</th>
                        <th>نوع واحد آزمون</th>
                        <th>تعرفه واحد آزمون</th>
                    </tr>
                </thead>
                <tbody>
                    ${standard.parameters.map(param => `
                        <tr>
                            <td><input type="checkbox" class="form-check-input" onchange="updateSelectedTests()"></td>
                            <td>${param.name}</td>
                            <td>${param.unit}</td>
                            <td>${param.testUnit}</td>
                            <td>${param.tariff}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
}

function updateSelectedTests() {
    const selectedTestsTable = document.getElementById('selectedTestsTable');
    selectedTestsTable.innerHTML = '';
    testsData.forEach(test => {
        const testCheckbox = document.getElementById(`test${test.id}`);
        if (testCheckbox.checked) {
            const selectedStandard = test.standards.find(s => document.querySelector(`input[name="standard${test.id}"]:checked`));
            if (selectedStandard) {
                const selectedParams = selectedStandard.parameters.filter((_, index) =>
                    document.querySelector(`#parameters${test.id} input[type="checkbox"]:nth-of-type(${index + 1})`).checked
                );
                selectedParams.forEach(param => {
                    const row = selectedTestsTable.insertRow();
                    row.innerHTML = `
                            <td></td>
                            <td>${test.name}</td>
                            <td>${selectedStandard.name}</td>
                            <td>${param.name}</td>
                            <td></td>
                            <td>${param.tariff}</td>
                            <td></td>
                            <td>${param.testUnit}</td>
                            <td></td>
                            <td><button class="btn btn-sm btn-danger">حذف</button></td>
                        `;
                });
            }
        }
    });
}

// Initialize the tests
const testsContainer = document.getElementById('testsContainer');
testsData.forEach(test => {
    testsContainer.appendChild(createTestElement(test));
});