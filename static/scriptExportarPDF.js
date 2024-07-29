document.addEventListener("DOMContentLoaded", function () {
    const showContainerBtn = document.getElementById("showContainerBtn");
    const closeContainerBtn = document.getElementById("cancelBtn");
    const exportContainer = document.getElementById("exportContainer");
    const fileName = document.getElementById("fileName");

    showContainerBtn.addEventListener("click", function () {
        exportContainer.style.display = "block";
        fileName.value = ''; 
        fileName.placeholder = "Ingrese el nombre del archivo";
    });

    closeContainerBtn.addEventListener("click", function () {
        exportContainer.style.display = "none";
        fileName.value = ''; 
        fileName.placeholder = "Ingrese el nombre del archivo";
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const fileNameInput = document.getElementById('fileName');
    const exportBtn = document.getElementById('exportBtn');
    const exportContainer = document.getElementById('exportContainer');
    const iframe = document.getElementById('datosHistoricosIframe');
    let myChart; // Declarar la variable myChart en un scope más amplio.

    const initChart = async () => {
        myChart = echarts.init(document.getElementById('chart'));

        const option = {
            title: {
                text: 'Predicción'
            },
            tooltip: {},
            xAxis: {
                type: 'category',
                data: [] // Se llenará con las fechas obtenidas de la tabla
            },
            yAxis: {},
            series: [{
                name: 'Matriculados',
                type: 'bar',
                data: [] // Se llenará con los datos de matriculados obtenidos de la tabla
            }, {
                name: 'Aprobados',
                type: 'bar',
                data: [] // Se llenará con los datos de aprobados obtenidos de la tabla
            }, {
                name: 'Reprobados',
                type: 'bar',
                data: [] // Se llenará con los datos de reprobados obtenidos de la tabla
            }, {
                name: 'Desertores',
                type: 'bar',
                data: [] // Se llenará con los datos de desertores obtenidos de la tabla
            }, {
                name: 'Foraneos',
                type: 'bar',
                data: [] // Se llenará con los datos de foraneos obtenidos de la tabla
            }],
            toolbox: {
                feature: {
                    saveAsImage: {
                        show: true
                    }
                }
            }
        };

        myChart.setOption(option);
        myChart.resize();
    };

    const captureChart = async () => {
        // Modificar las opciones antes de capturar
        myChart.setOption({
            title: {
                text: ''
            },
            toolbox: {
                feature: {
                    saveAsImage: {
                        show: false
                    }
                }
            }
        });

        const chartElement = document.getElementById('chart');
        const canvas = await html2canvas(chartElement);
        const chartImage = canvas.toDataURL('image/png');

        const img = document.createElement('img');
        img.src = chartImage;
        img.style.width = '800px';
        img.style.marginTop = '35px';
        img.style.marginBottom = '25px';
        img.style.height = '400px';

        const chartImageContainer = document.getElementById('chartImageContainer');
        chartImageContainer.innerHTML = '';
        chartImageContainer.appendChild(img);

        // Restaurar las opciones después de capturar
        myChart.setOption({
            title: {
                text: 'Predicción'
            },
            toolbox: {
                feature: {
                    saveAsImage: {
                        show: true
                    }
                }
            }
        });
    };

    const captureTable = async () => {
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        const tableSection = iframeDoc.querySelector('.datosHistoricos .section.tabla .contenedorTablas .table');

        const clonedTable = tableSection.cloneNode(true);
        const tableContainer = document.getElementById('tableContainer');
        tableContainer.innerHTML = '';
        tableContainer.appendChild(clonedTable);

        // Obtener los datos de la tabla para el gráfico
        const rows = tableSection.querySelectorAll('tbody tr');
        const fechas = [];
        const matriculados = [];
        const aprobados = [];
        const reprobados = [];
        const desertores = [];
        const foraneos = [];

        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            fechas.push(cells[0].innerText);
            matriculados.push(parseInt(cells[1].innerText, 10));
            aprobados.push(parseInt(cells[2].innerText, 10));
            reprobados.push(parseInt(cells[3].innerText, 10));
            desertores.push(parseInt(cells[4].innerText, 10));
            foraneos.push(parseInt(cells[5].innerText, 10));
        });

        // Actualizar los datos del gráfico
        myChart.setOption({
            xAxis: {
                data: fechas
            },
            series: [{
                name: 'Matriculados',
                data: matriculados
            }, {
                name: 'Aprobados',
                data: aprobados
            }, {
                name: 'Reprobados',
                data: reprobados
            }, {
                name: 'Desertores',
                data: desertores
            }, {
                name: 'Foraneos',
                data: foraneos
            }]
        });
    };

    exportBtn.addEventListener('click', function () {
        const fileName = fileNameInput.value.trim();
        if (fileName) {
            Promise.all([captureChart(), captureTable()]).then(() => {
                generarPDF(fileName);
            });
        } else {
            alert('Por favor, ingrese un nombre de archivo.');
        }
    });

    function generarPDF(fileName) {
        if (!fileName) {
            alert("Por favor, ingrese un nombre al archivo.");
            return;
        }

        const content = document.getElementById('docPDF');
        const opt = {
            margin: 0.5,
            filename: `${fileName}.pdf`,
            image: {
                type: 'jpeg',
                quality: 0.95
            },
            html2canvas: {
                scale: 4,
                useCORS: true
            },
            jsPDF: {
                unit: 'in',
                format: 'a4',
                orientation: 'portrait'
            }
        };

        html2pdf().set(opt).from(content).save().then(function () {
            console.log('PDF generado y guardado');
            fileNameInput.value = '';
        }).catch(function (error) {
            console.error('Error al generar el PDF:', error);
        });
    }

    window.addEventListener('load', initChart);
});

