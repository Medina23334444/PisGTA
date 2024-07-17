document.addEventListener('DOMContentLoaded', () => {
    const cycleInputs = document.querySelectorAll('.cycle');
    const totalInputs = document.querySelectorAll('.total');

    cycleInputs.forEach(input => {
        input.addEventListener('input', () => {
            const type = input.dataset.type;
            const relatedCycleInputs = document.querySelectorAll(`.cycle[data-type="${type}"]`);
            const totalInput = document.querySelector(`.total[data-type="${type}"]`);

            let sum = 0;
            relatedCycleInputs.forEach(cycleInput => {
                sum += Number(cycleInput.value || 0);
            });
            totalInput.value = sum;
        });
    });

    totalInputs.forEach(input => {
        input.addEventListener('input', () => {
            const type = input.dataset.type;
            const relatedCycleInputs = document.querySelectorAll(`.cycle[data-type="${type}"]`);

            relatedCycleInputs.forEach(cycleInput => {
                cycleInput.value = '';
            });
        });
    });

    const importExcelButton = document.getElementById('importExcel');
    const fileInput = document.getElementById('fileInput');

    importExcelButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            importFromExcel(file);
        }
    });

    async function importFromExcel(file) {
        const reader = new FileReader();
        reader.onload = async (event) => {
            const data = new Uint8Array(event.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];
            const jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

            populateFields(jsonData);
        };
        reader.readAsArrayBuffer(file);
    }

    function populateFields(data) {
        const headers = data[0].map(header => typeof header === 'string' ? header.toLowerCase() : header);
        const rows = data.slice(1);

        rows.forEach(row => {
            if (row.length > 1) { // Verificar que haya datos en la fila
                const type = (row[0] && typeof row[0] === 'string') ? row[0].toLowerCase() : ''; // Tipo de dato (matriculados, aprobados, etc.)
                row.forEach((value, index) => {
                    if (index > 0 && index < headers.length) { // Ignorar la columna de 'Ciclo' y 'Total'
                        const cycleInput = document.querySelector(`.cycle[data-type="${type}"][data-cycle="${index}"]`);
                        if (cycleInput) {
                            cycleInput.value = value;
                        }
                    }
                });
            }
        });

        // Actualizar los totales después de llenar los ciclos
        cycleInputs.forEach(input => {
            const event = new Event('input');
            input.dispatchEvent(event);
        });
    }

    const toggleColumnsButton = document.getElementById('toggleColumns');
    toggleColumnsButton.addEventListener('click', () => {
        const cycleColumns = document.querySelectorAll('.cycle-col');
        cycleColumns.forEach(column => {
            const cycle = column.getAttribute('data-cycle');
            const cycleCells = document.querySelectorAll(`.cycle[data-cycle="${cycle}"]`);
            cycleCells.forEach(cell => {
                cell.classList.toggle('hidden');
            });
        });
    });
});
