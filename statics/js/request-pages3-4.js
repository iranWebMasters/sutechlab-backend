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
    {
        id: 2,
        name: 'کوره',
        standards: [
            {
                id: 3,
                name: 'ASTM D1234',
                parameters: [
                    { id: 4, name: 'دمای بالا', unit: 'درجه سانتی گراد ( C )', testUnit: 'ساعت ( h )', tariff: '20000 (ریال)' }
                ]
            }
        ]
    }
];

function createRadioButtons(items, name, onChange) {
    return items.map(item => `
            <div class="form-check">
                <input class="form-check-input" type="radio" name="${name}" id="${name}${item.id}" value="${item.id}" onchange="${onChange}(${item.id})">
                <label class="form-check-label" for="${name}${item.id}">${item.name}</label>
            </div>
        `).join('');
}

function showStandards(testId) {
    const test = testsData.find(t => t.id === testId);
    const standardsContainer = document.getElementById('standardsContainer');
    standardsContainer.innerHTML = createRadioButtons(test.standards, 'standard', 'showParameters');
    document.getElementById('parametersContainer').innerHTML = '';
}

function showParameters(standardId) {
    const test = testsData.find(t => t.standards.some(s => s.id === standardId));
    const standard = test.standards.find(s => s.id === standardId);
    const parametersContainer = document.getElementById('parametersContainer');
    parametersContainer.innerHTML = `
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
    const selectedTestId = document.querySelector('input[name="test"]:checked')?.value;
    const selectedStandardId = document.querySelector('input[name="standard"]:checked')?.value;
    if (selectedTestId && selectedStandardId) {
        const test = testsData.find(t => t.id === parseInt(selectedTestId));
        const standard = test.standards.find(s => s.id === parseInt(selectedStandardId));
        const selectedParams = standard.parameters.filter((_, index) =>
            document.querySelector(`#parametersContainer input[type="checkbox"]:nth-of-type(${index + 1})`).checked
        );
        selectedParams.forEach((param, index) => {
            const row = selectedTestsTable.insertRow();
            row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${test.name}</td>
                    <td>${standard.name}</td>
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

// Initialize the tests
const testsContainer = document.getElementById('testsContainer');
testsContainer.innerHTML = createRadioButtons(testsData, 'test', 'showStandards');