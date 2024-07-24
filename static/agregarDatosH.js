document.addEventListener('DOMContentLoaded', () => {
    const cycleInputs = document.querySelectorAll('.cycle');
    const totalInputs = document.querySelectorAll('.total');

    const selectPeriodo = document.getElementById('selectPeriodo');
    const btnSeleccionarPeriodo = document.getElementById('btnSeleccionarPeriodo');
    const tablaDatos = document.getElementById('tablaDatos');
    const btnGuardarCambios = document.getElementById('btnGuardarCambios');

    // Función para cargar datos del periodo seleccionado
    btnSeleccionarPeriodo.addEventListener('click', async () => {
        const periodoId = selectPeriodo.value;
        if (periodoId) {
            try {
                const response = await fetch(`/cargarDatos/${periodoId}/`);
                if (response.ok) {
                    const data = await response.json();
                    populateTable(data);
                } else {
                    console.error('Error status:', response.status);
                    alert('Error al cargar los datos.');
                }
            } catch (error) {
                console.error('Fetch error:', error);
                alert('Error al cargar los datos.');
            }
        } else {
            alert('Por favor, selecciona un periodo.');
        }
    });

    // Función para llenar la tabla con los datos obtenidos
    function populateTable(data) {
        const tableBody = document.getElementById('tablaDatos');
        if (!tableBody) {
            console.error('Element with ID "tablaDatos" not found.');
            return;
        }

        const dataFields = ['matriculados', 'aprobados', 'reprobados', 'desertores', 'foraneos'];

        // Llenar los totales del periodo
        dataFields.forEach(field => {
            document.getElementById(`total_${field}`).textContent = data[`total_${field}`];
        });

        // Llenar los datos de cada ciclo
        for (let i = 1; i <= 8; i++) {
            dataFields.forEach(field => {
                const input = document.querySelector(`input[data-field="${field}_${i}"]`);
                if (input) {
                    input.value = data[`ciclo_${i}`][field];
                }
            });
        }
    }

    // Función para guardar los cambios
    btnGuardarCambios.addEventListener('click', async () => {
        const periodoId = selectPeriodo.value;
        if (!periodoId) {
            alert('Por favor, selecciona un periodo.');
            return;
        }

        const data = {
            periodo_id: periodoId,
            total_matriculados: document.getElementById('total_matriculados').textContent,
            total_aprobados: document.getElementById('total_aprobados').textContent,
            total_reprobados: document.getElementById('total_reprobados').textContent,
            total_desertores: document.getElementById('total_desertores').textContent,
            total_foraneos: document.getElementById('total_foraneos').textContent,
            ciclos: []
        };

        for (let i = 1; i <= 8; i++) {
            data.ciclos.push({
                ciclo: i,
                matriculados: document.querySelector(`input[data-field="matriculados_${i}"]`).value,
                aprobados: document.querySelector(`input[data-field="aprobados_${i}"]`).value,
                reprobados: document.querySelector(`input[data-field="reprobados_${i}"]`).value,
                desertores: document.querySelector(`input[data-field="desertores_${i}"]`).value,
                foraneos: document.querySelector(`input[data-field="foraneos_${i}"]`).value
            });
        }

        try {
            const response = await fetch(`/guardarDatos/${periodoId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    alert('Datos guardados exitosamente.');
                    window.location.reload();
                } else {
                    alert('Error al guardar los datos.');
                }
            } else {
                console.error('Error status:', response.status);
                alert('Error al guardar los datos.');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert('Error al guardar los datos.');
        }
    });

    // Obtener el CSRF token para las peticiones POST
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

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
                cell.classList.toggle('d-none'); // Usar la clase de Bootstrap para ocultar/mostrar
            });
        });
    });
});
