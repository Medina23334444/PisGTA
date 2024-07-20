const getObtionChart = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/get_chart/");
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error al realizar la solicitud fetch:', error);
        alert(error);
    }
};

const initChart=async()=>{
    const myChart=echarts.init(document.getElementById("chart"));
    
    myChart.setOption(await getObtionChart());
    myChart.resize();
};

window.addEventListener("load", async()=>{
    await initChart();
});