document.addEventListener('DOMContentLoaded', function () {
    const fileNameInput = document.getElementById('fileName');
    const exportBtn = document.getElementById('exportBtn');
    const exportContainer = document.getElementById('exportContainer');

    const initChart = async () => {
        const myChart = echarts.init(document.getElementById('chart'));
    
        const option = await getObtionChart();
    
        option.toolbox = {
            feature: {
                saveAsImage: {
                    show: false 
                }
            }
        };
    
        myChart.setOption(option);
        myChart.resize();
    };

    const captureChart = async () => {
        const chartElement = document.getElementById('chart');
        const canvas = await html2canvas(chartElement);
        const chartImage = canvas.toDataURL('image/png');

        const img = document.createElement('img');
        img.src = chartImage;
        img.style.width = '800px';
        img.style.marginTop = '35px';
        img.style.marginBottom = '25px';
        img.style.marginLeft = '25px';
        img.style.height = '400px' ;

        const chartImageContainer = document.getElementById('chartImageContainer');
        chartImageContainer.innerHTML = ''; 
        chartImageContainer.appendChild(img);
    };

    $('#exportContainer').on('show.bs.modal', async function () {
        await captureChart();
    });

    exportBtn.addEventListener('click', function () {
        const fileName = fileNameInput.value.trim();
        if (fileName) {
            generarPDF(fileName);
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
            $('#exportContainer').modal('hide');
            fileNameInput.value = '';
        }).catch(function (error) {
            console.error('Error al generar el PDF:', error);
        });
    }

    window.addEventListener('load', initChart);
});
