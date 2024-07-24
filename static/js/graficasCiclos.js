document.addEventListener('DOMContentLoaded', function() {
    const selectedCycles = JSON.parse(localStorage.getItem('selectedCycles'));
    console.log("JavaScript is running");
    console.log("Selected Cycles from localStorage: ", selectedCycles);

    const getObtionChart = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_chart1/");
            return await response.json();
        } catch (error) {
            console.error("Error fetching chart1 data:", error);
            alert(error);
        }
    };
    
    const getObtionChart2 = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_chart2/");
            return await response.json();
        } catch (error) {
            console.error("Error fetching chart2 data:", error);
            alert(error);
        }
    };
    
    const getObtionChart3 = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_chart3/");
            return await response.json();
        } catch (error) {
            console.error("Error fetching chart3 data:", error);
            alert(error);
        }
    };
    
    const getObtionChart4 = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_chart4/");
            return await response.json();
        } catch (error) {
            console.error("Error fetching chart4 data:", error);
            alert(error);
        }
    };
    const getObtionChart5 = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_chart5/");
            return await response.json();
        } catch (error) {
            console.error("Error fetching chart5 data:", error);
            alert(error);
        }
    };
    
    const getObtionChart6 = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_chart6/");
            return await response.json();
        } catch (error) {
            console.error("Error fetching chart6 data:", error);
            alert(error);
        }
    };

    const getObtionChart7 = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_chart7/");
            return await response.json();
        } catch (error) {
            console.error("Error fetching chart7 data:", error);
            alert(error);
        }
    };
    
    const getObtionChart8 = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_chart8/");
            return await response.json();
        } catch (error) {
            console.error("Error fetching chart8 data:", error);
            alert(error);
        }
    };

    const getObtionChart9 = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_chart9/");
            return await response.json();
        } catch (error) {
            console.error("Error fetching chart9 data:", error);
            alert(error);
        }
    };
    

    const initChart = async () => {
        console.log("Initializing chart1"); // Añade esto para depurar
        const myChart = echarts.init(document.getElementById("chart1"));
        myChart.setOption(await getObtionChart());
        myChart.resize();
    };
    
    const initChart2 = async () => {
        console.log("Initializing chart2"); // Añade esto para depurar
        const myChart = echarts.init(document.getElementById("chart2"));
        myChart.setOption(await getObtionChart2());
        myChart.resize();
    };

    const initChart3 = async () => {
        console.log("Initializing chart3"); // Añade esto para depurar
        const myChart = echarts.init(document.getElementById("chart3"));
        myChart.setOption(await getObtionChart3());
        myChart.resize();
    };
    
    const initChart4 = async () => {
        console.log("Initializing chart4"); // Añade esto para depurar
        const myChart = echarts.init(document.getElementById("chart4"));
        myChart.setOption(await getObtionChart4());
        myChart.resize();
    };

    const initChart5 = async () => {
        console.log("Initializing chart5"); // Añade esto para depurar
        const myChart = echarts.init(document.getElementById("chart5"));
        myChart.setOption(await getObtionChart5());
        myChart.resize();
    };
    
    const initChart6 = async () => {
        console.log("Initializing chart6"); // Añade esto para depurar
        const myChart = echarts.init(document.getElementById("chart6"));
        myChart.setOption(await getObtionChart6());
        myChart.resize();
    };

    const initChart7 = async () => {
        console.log("Initializing chart7"); // Añade esto para depurar
        const myChart = echarts.init(document.getElementById("chart7"));
        myChart.setOption(await getObtionChart7());
        myChart.resize();
    };
    
    const initChart8 = async () => {
        console.log("Initializing chart8"); // Añade esto para depurar
        const myChart = echarts.init(document.getElementById("chart8"));
        myChart.setOption(await getObtionChart8());
        myChart.resize();
    };

    const initChart9 = async () => {
        console.log("Initializing chart9"); // Añade esto para depurar
        const myChart = echarts.init(document.getElementById("chart9"));
        myChart.setOption(await getObtionChart9());
        myChart.resize();
    };
    
    const showCharts = async () => {
        console.log("Showing charts based on selected cycles");
        const chart1Container = document.getElementById("chart1Container");
        const chart2Container = document.getElementById("chart2Container");
        const chart3Container = document.getElementById("chart3Container");
        const chart4Container = document.getElementById("chart4Container");
        const chart5Container = document.getElementById("chart5Container");
        const chart6Container = document.getElementById("chart6Container");
        const chart7Container = document.getElementById("chart7Container");
        const chart8Container = document.getElementById("chart8Container");
        const chart9Container = document.getElementById("chart9Container");
        const chartsRow = document.getElementById("chartsRow");
    
        // Oculta todos los contenedores primero
        chart1Container.style.display = "none";
        chart2Container.style.display = "none";
        chart3Container.style.display = "none";
        chart4Container.style.display = "none";
        chart5Container.style.display = "none";
        chart6Container.style.display = "none";
        chart7Container.style.display = "none";
        chart8Container.style.display = "none";
        chart9Container.style.display = "none";
        
        let visibleCharts = 0;
    
        if (selectedCycles && selectedCycles.includes('Ciclo 1')) {
            console.log("Showing chart1");
            chart1Container.style.display = "flex";
            await initChart();
            visibleCharts++;
        }
    
        if (selectedCycles && selectedCycles.includes('Ciclo 2')) {
            console.log("Showing chart2");
            chart2Container.style.display = "flex";
            await initChart2();
            visibleCharts++;
        }

        if (selectedCycles && selectedCycles.includes('Ciclo 3')) {
            console.log("Showing chart3");
            chart3Container.style.display = "flex";
            await initChart3();
            visibleCharts++;
        }
    
        if (selectedCycles && selectedCycles.includes('Ciclo 4')) {
            console.log("Showing chart4");
            chart4Container.style.display = "flex";
            await initChart4();
            visibleCharts++;
        }

        if (selectedCycles && selectedCycles.includes('Ciclo 5')) {
            console.log("Showing chart5");
            chart5Container.style.display = "flex";
            await initChart5();
            visibleCharts++;
        }
    
        if (selectedCycles && selectedCycles.includes('Ciclo 6')) {
            console.log("Showing chart6");
            chart6Container.style.display = "flex";
            await initChart6();
            visibleCharts++;
        }

        if (selectedCycles && selectedCycles.includes('Ciclo 7')) {
            console.log("Showing chart7");
            chart7Container.style.display = "flex";
            await initChart7();
            visibleCharts++;
        }
    
        if (selectedCycles && selectedCycles.includes('Ciclo 8')) {
            console.log("Showing chart8");
            chart8Container.style.display = "flex";
            await initChart8();
            visibleCharts++;
        }

        if (selectedCycles && selectedCycles.includes('Ciclo 9')) {
            console.log("Showing chart9");
            chart9Container.style.display = "flex";
            await initChart9();
            visibleCharts++;
        }
    
        // Ajusta el ancho de los contenedores visibles
        const width = visibleCharts === 1 ? '100%' : '50%';
        if (chart1Container.style.display !== 'none') chart1Container.style.width = width;
        if (chart2Container.style.display !== 'none') chart2Container.style.width = width;
        if (chart3Container.style.display !== 'none') chart1Container.style.width = width;
        if (chart4Container.style.display !== 'none') chart2Container.style.width = width;
        if (chart5Container.style.display !== 'none') chart1Container.style.width = width;
        if (chart6Container.style.display !== 'none') chart2Container.style.width = width;
        if (chart7Container.style.display !== 'none') chart1Container.style.width = width;
        if (chart8Container.style.display !== 'none') chart2Container.style.width = width;
        if (chart9Container.style.display !== 'none') chart1Container.style.width = width;
    
        // Fuerza un reflow para que los cambios surtan efecto
        chartsRow.offsetHeight;
    };
    
    window.addEventListener("load", async () => {
        console.log("Page loaded, executing showCharts"); // Añade esto para depurar
        await showCharts();
    });
});


